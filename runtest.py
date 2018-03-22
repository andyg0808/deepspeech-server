#!/usr/bin/env python
"""
Usage:
    runtest [options] <filecount> <hostfile>

Options:
    --outputfile=<filename>  Write output into specified file [Default: outputfile]
    --hosts=<count>          Use exactly <count> hosts to run the files
"""
import shutil
import tempfile
import docopt
import distributor
import subprocess
import re
import sys
import time
import datetime


def run_with_hosts(files, hosts):
    hostfile = tempfile.NamedTemporaryFile(mode='w+')
    hostfile.write("[main]\n")
    for host in hosts:
        hostfile.write(host+"\n")
    hostfile.flush()
    tempdir = tempfile.TemporaryDirectory()
    for i in range(files):
        fname = "pieces/sentences{:03d}.wav".format(i+1)
        shutil.copy(fname, tempdir.name)
    print("Running {} files on {} Pis:".format(files, len(hosts)))
    command = "python ./distributor.py --maxfiles={} {} {}".format(files, tempdir.name, hostfile.name)
    print("Running", command, "on", hosts)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    return (process, hostfile, tempdir)


DATA = re.compile(r"^Finished all runs at \d+\.\d+ \(\d+\.\d+ total time\)$", re.MULTILINE)


def interpret_process(results, hosts, files, process):
    output = process.communicate()[0]
    times = DATA.findall(output)
    if len(times) < files:
        print("Too few results; expected {}; got {}.\n".format(files, times), output)
        sys.exit(2)
    results.write("runtest.py {} ({} pis; {} audio files):\n".format(datetime.datetime.now(), hosts, files))
    results.write(times[-1]+"\n")
    results.flush()


def main(output_file, files, hostfile, host_count=0, repeats=3):
    hosts = distributor.parse_hosts(hostfile)

    with open(output_file, "a") as results:
        if len(hosts) == 1:
            for x in range(repeats):
                process, *handles = run_with_hosts(files, hosts)
                process.wait()
                interpret_process(results, len(hosts), files, process)
        elif host_count != 0:
            for x in range(repeats):
                process, *handles = run_with_hosts(files, hosts[0:host_count])
                process.wait()
                interpret_process(results, host_count, files, process)
        else:
            for i in range(len(hosts)//2+1):
                used_hosts = hosts[i:len(hosts)]
                used_hosts2 = hosts[0:i]
                for x in range(repeats):
                    # Tempfiles are destroyed when the objects in handles are
                    # garbage collected. So we only need to keep them alive for the
                    # duration of the distributor process. That's the job of the
                    # handles variable
                    process, *handles = run_with_hosts(files, used_hosts)
                    # This will sometimes be empty
                    if used_hosts2:
                        time.sleep(5)
                        process2, *handles2 = run_with_hosts(files, used_hosts2)
                        process2.wait()
                        interpret_process(results, len(used_hosts2), files, process2)
                    process.wait()
                    interpret_process(results, len(used_hosts), files, process)



if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options['--hosts']:
        main(options['--outputfile'], int(options['<filecount>']), options['<hostfile>'], host_count=int(options['--hosts']))
    else:
        main(options['--outputfile'], int(options['<filecount>']), options['<hostfile>'])
