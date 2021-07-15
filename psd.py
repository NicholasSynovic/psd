from requests import get, Response
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag


def getFTPRoot() -> str:
    html: Response = get(url="https://www.python.org/ftp/python/")
    return html.text


def getLinks(soup: BeautifulSoup) -> dict:
    links: dict = {}
    tags: ResultSet = soup.find_all(name="a")

    tag: Tag
    for tag in tags:
        key: str = tag.text.replace("/", "")
        value: str = "https://www.python.org/ftp/python/" + tag.get("href")

        try:
            int(key[0])
            links[key] = value
        except ValueError:
            pass

    return links


def getUserSelection(choices: list) -> str:
    pass


if __name__ == "__main__":
    site = getFTPRoot()
    soup: BeautifulSoup = BeautifulSoup(markup=site, features="html.parser")
    links: dict = getLinks(soup)
    getUserSelection(list(links.keys()))
