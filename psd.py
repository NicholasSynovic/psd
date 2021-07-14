from requests import get, Response


def getFTPRoot() -> str:
    html: Response = get(url="https://www.python.org/ftp/python/")
    return html.text


print(getFTPRoot())
