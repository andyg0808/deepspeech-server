import requests
def ask():
    files = {'file': open("file16000.wav", "rb")}
    r = requests.post("http://localhost:5000/", files=files)
    print(r.text, end="")

if __name__ == "__main__":
    ask()
