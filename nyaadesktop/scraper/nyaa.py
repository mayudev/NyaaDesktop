# Miscellaneous things used in scraper module
from __future__ import annotations
from dataclasses import dataclass, field
from urllib import parse
from nyaadesktop.__init__ import __version__


@dataclass
class NewItemModel:
    kind: str
    name: str
    children: list = field(default_factory=list)
    size: str = ""


BASE_URL = "https://nyaa.si"
USER_AGENT = "NyaaDesktop/" + __version__


class Category:
    def __init__(self, name, id, subid):
        self.name: str = name
        self.id: int = id
        self.subid: int = subid


categories = [
    Category("All categories", 0, 0),
    Category("Anime", 1, 0),
    Category("- Anime Music Video", 1, 1),
    Category("- English-translated", 1, 2),
    Category("- Non-English-translated", 1, 3),
    Category("- Raw", 1, 4),
    Category("Audio", 2, 0),
    Category("- Lossless", 2, 1),
    Category("- Lossy", 2, 2),
    Category("Literature", 3, 0),
    Category("- English-translated", 3, 1),
    Category("- Non-English-translated", 3, 2),
    Category("- Raw", 3, 3),
    Category("Live Action", 4, 0),
    Category("- English-translated", 4, 1),
    Category("- Idol/Promotional Video", 4, 2),
    Category("- Non-English-translated", 4, 3),
    Category("- Raw", 4, 4),
    Category("Pictures", 5, 0),
    Category("- Graphics", 5, 1),
    Category("- Photos", 5, 2),
    Category("Software", 6, 0),
    Category("- Applications", 6, 1),
    Category("- Games", 6, 2),
]


@dataclass
class File:
    kind: str  # folder or file
    name: str
    size: str


@dataclass
class Details:
    files: list[NewItemModel] = field(default_factory=list)
    title: str = ""
    category: str = ""
    submitter: str = ""
    submitter_badge: str = ""
    information: str = ""
    description: str = ""
    comments: list[Comment] = field(default_factory=list)


@dataclass
class Comment:
    author: str
    comment: str
    date: str


class ScraperError(Exception):
    """
    An exception has occured that made the scraper fail.
    """

    pass


class ScraperParseError(Exception):
    """
    An exception while parsing a single element has occured.
    Scraper may continue working, but the element will be skipped.
    """

    pass


class ScraperNoResults(Exception):
    pass


def url_builder(
    query, category_id, filter_id=0, page=1, sort="id", order="desc", user=None
):
    params = {"f": filter_id, "c": category_id, "p": page, "s": sort, "o": order}

    if query:
        params["q"] = query

    if user is None:
        url = BASE_URL + "/?" + parse.urlencode(params)
    else:
        url = BASE_URL + "/user/" + user + "?" + parse.urlencode(params)

    return url


def details_url_builder(path):
    return BASE_URL + path
