"""
Usage:
    distributor.py <directory> <hosts_file>
"""
import requests
import docopt
import re
from pathlib import Path
import time
import asyncio
import logging

GROUP = re.compile(r"\[(\S+)\]")


class Looper:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        logging.getLogger('asyncio').setLevel(logging.WARNING)

    def check(self, seen, text, watchable, hosts):
        print("Checking...")
        for f in watchable.glob('*'):
            if f not in seen:
                print(f)
                seen.add(f)
                fut = self.send('localhost', f)

                def callback(fut):
                    print("abc")
                    print(fut)
                    text.append(fut.result())
                    print(text)

                fut.add_done_callback(callback)
                while not fut.done():
                    print("waiting for future...")
                    time.sleep(.01)
                for i in range(10):
                    time.sleep(.1)
                    print(' '.join(text))
        if len(list(watchable.glob('*'))) == 0:
            text = []
        self.loop.call_later(.25, self.check, seen, text, watchable, hosts)
        
    def send(self, host, audio):
        future = asyncio.Future()
        print("Sending {} to {}".format(audio, host))
        f = open(audio, "rb")
        files = {'file': f}

        def hook(r, *args, **kwargs):
            f.close()
            future.set_result(r.text.strip())

        hooks = {'response': hook}
        requests.post("http://{}:8035/test".format(host), files=files,
                      hooks=hooks)
        return future

    def watch(self, directory, hosts):
        print(self.loop)
        seen = set()
        text = []
        watchable = Path(directory)
        self.loop.call_soon(self.check, seen, text, watchable, hosts)
        self.loop.run_forever()


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
    looper = Looper()
    looper.watch(args['<directory>'], hosts)
