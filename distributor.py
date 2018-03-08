"""
Usage:
    distributor.py <directory> <hosts_file>
"""
import requests
from functools import partial
import docopt
import re
from pathlib import Path
import time
import asyncio
import logging
import redf

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
        fut2.add_done_callback(finish_all)

    fut1.add_done_callback(setup_2)
    return fut


def check(seen, text, watchable, hosts):
    print("Checking...")
    futures = []
    for f in watchable.glob('*'):
        if f not in seen:
            print(f)
            seen.add(f)
            coro = loop.run_in_executor(None, send, 'localhost', f)
            fut = loop.create_task(coro)
            futures.append(fut)

    def printout(f):
        lst = f.result()
        print(lst)

    fut = combine(futures)
    fut.add_done_callback(printout)
    loop.call_later(.25, check, seen, text, watchable, hosts)


def send(host, audio):
    print("Sending {} to {}".format(audio, host))
    f = open(audio, "rb")
    files = {'file': f}

    r = requests.post("http://{}:8035/test".format(host), files=files)
    f.close()
    return r.text.strip()


def watch(directory, hosts):
    print(loop)
    seen = set()
    text = []
    watchable = Path(directory)
    loop.call_soon(check, seen, text, watchable, hosts)
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
                print(group)
                print(pieces)
                if len(pieces) > 0:
                    if group == "main":
                        hosts.append(pieces[0])
    return hosts


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    hosts = parse_hosts(args['<hosts_file>'])
    watch(args['<directory>'], hosts)
