"""
Usage:
    distributor.py <directory> <hosts_file>
"""
import requests
from functools import partial
import docopt
import re
from pathlib import Path
import asyncio
import logging
from itertools import cycle
import socket
import time

GROUP = re.compile(r"\[(\S+)\]")


loop = asyncio.get_event_loop()
loop.set_debug(True)
logging.getLogger('asyncio').setLevel(logging.WARNING)


def combine(lfut):
    fut = loop.create_future()
    fut.set_result([])
    for f in lfut:
        fut = tie(fut, f)
    return fut


def tie(fut1, fut2):
    fut = loop.create_future()

    def finish_all(f1, f2):
        fut.set_result(f1 + [f2.result()])

    def setup_2(f1):
        func = partial(finish_all, f1.result())
        fut2.add_done_callback(func)

    fut1.add_done_callback(setup_2)
    return fut


def handle(fut1, fut2, func):
    fut = loop.create_future()

    def fire(f2):
        fut.set_result(f2.result())
        func(f2.result())

    def setup_2(f1):
        fut2.add_done_callback(fire)

    fut1.add_done_callback(setup_2)
    return fut


def sequence(lfut, func):
    last = loop.create_future()
    last.set_result(None)
    for fut in lfut:
        last = handle(last, fut, func)
    return last


def check(seen, text, watchable, hosts, active):
    futures = []
    #loop.call_later(.25, check, seen, text, watchable, hosts, active)
    start = time.time()
    print(start)
    for f in watchable.glob('*'):
        if f not in seen:
            print(f)
            seen.add(f)
            host = next(hosts)
            active[host] = True
            fut = loop.run_in_executor(None, send, host, f)
            futures.append(fut)

    def result(r):
        print(r)
        print("Finished all runs at {} ({} total time)".format(time.time(), time.time()-start))
        active[r[0]] = False

    sequence(futures, result)


def send(host, audio):
    print("Sending {} to {}".format(audio, host))
    f = open(audio, "rb")
    files = {'file': f}

    r = requests.post("http://{}:5000/".format(host), files=files)
    f.close()
    audio.unlink()
    return (host, audio, r.text.strip())


def watch(directory, hosts):
    print(loop)
    seen = set()
    text = []
    watchable = Path(directory)
    active = {}
    loop.call_soon(check, seen, text, watchable, hosts, active)
    loop.run_forever()


def parse_hosts(hostfile):
    hosts = []
    group = None
    with open(hostfile) as f:
        for line in f:
            if GROUP.match(line):
                group = line[1:-2]
            else:
                pieces = line.split()
                if len(pieces) > 0:
                    if group == "main":
                        hosts.append(pieces[0])
    valid_hosts = []
    for host in hosts:
        print("Checking {}...".format(host))
        try:
            socket.getaddrinfo(host, 5000)
            valid_hosts.append(host)
            print("Live.")
        except socket.gaierror as e:
            # These errors happen if a server is not live
            print("Missing.")
    return valid_hosts


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    hosts = parse_hosts(args['<hosts_file>'])
    print(hosts)
    watch(args['<directory>'], cycle(hosts))
