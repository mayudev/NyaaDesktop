from dataclasses import dataclass

@dataclass
class Item:
    category: str
    name: str
    torrent_url: str
    details_url: str
    magnet: str
    size: str
    date: str
    seeders: int
    leechers: int
    completed: int
    comment_count: int