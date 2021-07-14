from requests import get, Response


def getFTPRoot() -> str:
    html: Response = get(url="https://www.python.org/ftp/python/")
    return html.text


def getAText():
    pass


def getAHREF():
    pass


print(getFTPRoot())


if __name__ == "__main__":
    pass
