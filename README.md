# NyaaDesktop

![License](https://img.shields.io/github/license/mayudev/NyaaDesktop)
![Version](https://img.shields.io/github/v/release/mayudev/NyaaDesktop)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple desktop app for nyaa.si

You can use this app, for example, to download multiple torrents at once if batches are not available, from for example SubsPlease or HorribleSubs (as long as the torrents themselves are not dead, this app will work, because it uses nyaa.si instead of HS site which is long dead [*])

Also, one other thing I find this app is better than just using the website is when you have to quickly peek at the description.

## Requirements
- Python 3.8+
- A torrent client (e.g. **Transmission**, **qBittorrent**. DON'T USE μTORRENT)

## Installation

### Windows
Just grab the zip from [releases](https://github.com/mayudev/NyaaDesktop/releases/latest)

### Linux

#### PySide6

This app requires PySide6 (Qt6 bindings for Python) installed in your system. It's recommended that you use the package provided by your distribution for best results.

Unfortunately, Qt 6 is fairly recent and it seems only Arch provides one for now.
- Arch Linux: `pacman -S pyside6`

On other distributions, you can use pip: `pip install pyside6` *but it looks ugly...*

```sh
git clone https://github.com/mayudev/NyaaDesktop
cd NyaaDesktop
pip install -r requirements.txt
# To run the app without installation do:
python -m nyaadesktop
# If you want to install, do:
pip install .
# Then you should be able to run the app with:
nyaadesktop
```
There is a desktop entry (`nyaadesktop.desktop`) you can copy to `~/.local/share/applications` and it should work if you've installed it.

## Screenshot
![Screenshot](https://raw.githubusercontent.com/mayudev/NyaaDesktop/main/screenshot.png)

## Known issues
- Freeze when trying to load a torrent with a lot of files
- There is no icon
- This app looks ugly pretty much everywhere other than Windows
