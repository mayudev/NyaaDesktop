from __future__ import annotations
import sys, os, subprocess
from requests import get

from nyaadesktop.scraper.nyaa import BASE_URL


def open_links(links: list[str]):
    # Windows
    if sys.platform == "win32" or sys.platform == "cygwin":
        for link in links:
            windows_exec(link)
    elif sys.platform == "darwin":
        for link in links:
            link_exec("open", link)
    else:
        for link in links:
            link_exec("xdg-open", link)


def windows_exec(dest):
    os.startfile(dest)


def link_exec(fn, dest):
    subprocess.Popen([fn, dest], stderr=subprocess.DEVNULL)


def save_torrents(torrents: list[str]):
    for torrent in torrents:
        filename = torrent.split("/")[-1]
        r = get(BASE_URL + torrent, stream=True)

        # TODO customize directory
        open(filename, "wb").write(r.content)

    return len(torrents)
