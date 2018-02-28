"""
Usage:
    client.py <file> <destination>
"""
import requests
import docopt
def ask(audio, destination):
    files = {'file': open(audio, "rb")}
    r = requests.post("http://{}/".format(destination), files=files)
    print(r.text, end="")

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    ask(args['<file>'], args['<destination>'])
