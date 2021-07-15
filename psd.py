from requests import get, Response
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
from requests.api import options
from simple_term_menu import TerminalMenu
import re
from re import Pattern


def getHTML(url: str = "https://www.python.org/ftp/python/") -> str:
    html: Response = get(url)
    return html.text


def getLinks(soup: BeautifulSoup, filter: str = "") -> dict:
    links: dict = {}
    regex: Pattern = re.compile(f"\\b{filter}\\b$")
    tags: ResultSet = soup.find_all(name="a")

    tag: Tag
    for tag in tags:
        key: str = tag.text.replace("/", "")
        value: str = "https://www.python.org/ftp/python/" + tag.get("href")

        if re.search(regex, key) is not None:
            links[key] = value
    return links


def removeExtras(data: dict, removeNonVersions: bool, filter: str = "") -> dict:
    temp: dict = {}
    regex: Pattern = re.compile(f"\\b{filter}\\b$")
    if removeNonVersions:
        for key in data.keys():
            try:
                int(key[0])
                if re.search(regex, key) is not None:
                    temp[key] = data[key]
            except ValueError:
                pass
    else:
        for key in data.keys():
            if re.search(regex, key) is not None:

                temp[key] = data[key]
    return temp


def getUserSelection(options: list) -> str:
    terminal_menu = TerminalMenu(
        options,
        title="Python Version",
        status_bar='Use "/" to search for a specific version. ENTER to select.',
        status_bar_style=("fg_black", "bg_blue"),
    )
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]


if __name__ == "__main__":
    site = getHTML()
    soup: BeautifulSoup = BeautifulSoup(markup=site, features="html.parser")
    links: dict = getLinks(soup, "")
    links = removeExtras(data=links, removeNonVersions=True)

    pythonVersion: str = getUserSelection(list(links.keys()))

    site = getHTML(url=links[pythonVersion])
    soup: BeautifulSoup = BeautifulSoup(markup=site, features="html.parser")
    links: dict = getLinks(soup, filter=".tgz")
    links = removeExtras(data=links, removeNonVersions=False, filter=".tgz")

    downloadKey: str = getUserSelection(list(links.keys()))
    print(links[downloadKey])
