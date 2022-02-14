from bs4 import BeautifulSoup
from requests import get
from nyaadesktop.scraper.nyaa import USER_AGENT, Details, File


def details_scraper(url) -> Details:
    try:
        response = get(url, headers={'User-Agent': USER_AGENT})
        if response.ok:
            # TODO fix performance issues when the list is very long
            # (which happens)
            # For example just make it give up after a few seconds

            # For some reason, even though it should be done in a seperate thread
            # it makes the gui to lag anyway
            parser = BeautifulSoup(response.content, 'lxml')

            description = parser.find(id="torrent-description").string
            try:
                submitter = parser.select(".row a")[2].string
            except:
                submitter = "Anonymous"

            title = parser.select(".panel-title")[0].string.strip()
            information = parser.select(".row")[2].select('.col-md-5')[0].text.strip()

            # Files
            try:
                files = []
                filelist = parser.select(".torrent-file-list li i.fa-file")
                for file in filelist:
                    size = file.next_sibling.next_sibling.string[1:-1] # stripping parenthesis
                    filename = file.next_sibling.string.strip()

                    files.append(File("file", filename, size))
            except:
                files = []

            return Details(files, title, "Category", submitter, information, description)

    except:
        raise
