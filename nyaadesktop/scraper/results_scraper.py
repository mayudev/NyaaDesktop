from bs4 import BeautifulSoup
from requests import get
from nyaadesktop.item import Item

from nyaadesktop.scraper.nyaa import USER_AGENT, ScraperError, ScraperNoResults

def result_scraper(url) -> tuple[list[Item], int]:
    try:
        # Send a request to nyaa
        response = get(url, headers={'User-Agent': USER_AGENT})
        if response.ok:
            # Initialize BeautifulSoup
            parser = BeautifulSoup(response.content, 'lxml')
            results = parser.findAll('tr')

            if len(results) == 0:
                # No results found
                raise ScraperNoResults("No results")

            found_items: list[Item] = []
            
            # Excluding the first element, since it's the header.
            for result in results[1:]:

                # Those are pretty much guaranteed
                category = result.select('a')[0]['title']
                details_url = result.select('a')[1]['href'].replace("#comments", "")
                size = result.select('td')[3].string
                date = result.select('td')[4].string
                seeders = result.select('td')[5].string
                leechers = result.select('td')[6].string
                completed = result.select('td')[7].string

                # Those are tricky, so we perform additional checks
                
                # Torrent URL
                # This also sometimes is not available
                try:
                    torrent_url = result.select('a i.fa-download')[0].parent['href']
                except:
                    torrent_url = None

                # Magnet
                # This is an extermely rare situation, but sometimes happens with really old torrents.
                try:
                    magnet_parent = result.select('a i.fa-magnet')
                    magnet = magnet_parent[0].parent['href']
                except:
                    magnet = None

                # Comments... well, most torrent don't have any comments
                try:
                    # Also, the order of the element with torrent name depends
                    # whether there are comments or not.
                    # This doesn't really make sense, I guess
                    name = result.select('a')[2].string
                    comment_count = list(result.select('a.comments')[0].descendants)[2].string
                except:
                    name = result.select('a')[1].string
                    comment_count = 0

                # Trusted/Remake property
                try:
                    badge_class = result['class'][0]
                    if badge_class == "success":
                        badge = "trusted"
                    elif badge_class == "danger":
                        badge = "remake"
                    else:
                        badge = "none"
                except:
                    badge = "none"

                item = Item(
                    category,
                    name,
                    torrent_url,
                    details_url,
                    magnet,
                    size,
                    date,
                    seeders,
                    leechers,
                    completed,
                    comment_count,
                    badge
                )

                found_items.append(item)

            try:
                pages_count = int(parser.select(".pagination a")[-2].string)
            except:
                pages_count = 1

            return found_items, pages_count

        else:
            raise ScraperError("Something went wrong with the request")
    except:
        raise