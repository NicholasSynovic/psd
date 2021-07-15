from requests import get, Response
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
from requests.api import options
from simple_term_menu import TerminalMenu
import re
from re import Pattern
from progress.spinner import MoonSpinner


def getHTML(url: str = "https://www.python.org/ftp/python/") -> str:
    html: Response = get(url)
    return html.text


def getLinks(soup: BeautifulSoup, version: str = "", filter: str = "") -> dict:
    links: dict = {}
    regex: Pattern = re.compile(f"\\b{filter}\\b$")
    tags: ResultSet = soup.find_all(name="a")

    tag: Tag
    for tag in tags:
        key: str = tag.text.replace("/", "")
        value: str = "https://www.python.org/ftp/python/" + version + tag.get("href")

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


def download(filename: str, url: str) -> bool:
    with MoonSpinner(f"Downloading {filename}... ") as spinner:
        with get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    spinner.next()
    return filename


if __name__ == "__main__":
    site = getHTML()
    soup: BeautifulSoup = BeautifulSoup(markup=site, features="html.parser")
    links: dict = getLinks(soup, "")
    links = removeExtras(data=links, removeNonVersions=True)

    pythonVersion: str = getUserSelection(list(links.keys()))

    site = getHTML(url=links[pythonVersion])
    soup: BeautifulSoup = BeautifulSoup(markup=site, features="html.parser")
    links: dict = getLinks(soup, version=pythonVersion + "/", filter=".tgz")

    if len(links) == 0:
        links: dict = getLinks(soup, version=pythonVersion + "/", filter=".gz")
        links = removeExtras(data=links, removeNonVersions=False, filter=".gz")
    else:
        links = removeExtras(data=links, removeNonVersions=False, filter=".tgz")

    downloadKey: str = getUserSelection(list(links.keys()))

    download(filename=downloadKey, url=links[downloadKey])
