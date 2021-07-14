from requests import get, Response


def getFTPRoot() -> str:
    html: Response = get(url="https://www.python.org/ftp/python/")
    return html.text


def getAText():
    pass


def getAHREF():
    pass


if __name__ == "__main__":
