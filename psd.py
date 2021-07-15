from requests import get, Response
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
from requests.api import options
from simple_term_menu import TerminalMenu


def getHTML(url: str = "https://www.python.org/ftp/python/") -> str:
    html: Response = get(url)
    return html.text


def getLinks(soup: BeautifulSoup, filter: str = "") -> dict:
    links: dict = {}
    tags: ResultSet = soup.find_all(name="a")

    tag: Tag
    for tag in tags:
        key: str = tag.text.replace("/", "")
        value: str = "https://www.python.org/ftp/python/" + tag.get("href")

        if key.find(filter) != -1:
            try:
                int(key[0])
                links[key] = value
            except ValueError:
                pass

    return links


def getUserSelection(options: list) -> str:
    terminal_menu = TerminalMenu(
        options,
        title="Python Version",
        status_bar='Use "/" to search for a specific version. ENTER to select.',
        status_bar_style=("fg_black", "bg_blue"),
    )
    menu_entry_index = terminal_menu.show()
    print(options[menu_entry_index])


if __name__ == "__main__":
    site = getHTML()
    soup: BeautifulSoup = BeautifulSoup(markup=site, features="html.parser")
    links: dict = getLinks(soup)
    print(links.keys())
    pythonVersion: str = getUserSelection(list(links.keys()))
