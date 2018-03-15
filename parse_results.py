"""
Usage:
    parse_results.py [--output=<output_file>] <results_file>
"""
from os.path import basename
import docopt
import re
import pandas as pd

HEADING = re.compile(r"^.* \((?P<pis>\d+) pis; (?P<files>\d+) audio files\):$")
DATA = re.compile(r"^Finished all runs at (?P<timestamp>\d+\.\d+) \((?P<time>\d+\.\d+) total time\)$")


def parse_results(input_file):
    pi_count = 0
    file_count = 0
    results = []
    with open(input_file) as io:
        for l in io:
            if HEADING.match(l):
                match = HEADING.match(l)
                pi_count = match.group('pis')
                file_count = match.group('files')
            elif DATA.match(l):
                match = DATA.match(l)
                result = {
                        "pi_count": pi_count,
                        "file_count": file_count,
                        "timestamp": match.group('timestamp'),
                        "time": match.group('time')
                }
                results.append(result)

    return results

def main(infile, outfile):
    results = parse_results(infile)
    data = pd.DataFrame(results)
    data.to_csv(outfile)



if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    input_file = options['<results_file>']
    if options['--output']:
        output_file = options['--output']
    else:
        output_file = basename(input_file)+'.csv'
    main(input_file, output_file)

