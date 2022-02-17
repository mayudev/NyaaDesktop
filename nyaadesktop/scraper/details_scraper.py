from bs4 import BeautifulSoup
from requests import get
from nyaadesktop.scraper.nyaa import USER_AGENT, Details, NewItemModel

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

            # File tree
            try:
                parent = parser.select(".torrent-file-list")[0].ul.li
                parentFolder = parent.findChildren("a", recursive=False)
                if len(parentFolder) == 0:
                    tree = NewItemModel("file", parent.i.next_sibling.string.strip(), size=parent.span.string[1:-1])
                else:
                    folderName = parentFolder[0].i.next_sibling.string.strip()
                    tree = NewItemModel("folder", folderName)

                    # DIRECT CHILDREN
                    children = parentFolder[0].next_sibling.next_sibling.findChildren("li", recursive=False)
                    for child in children:
                        # CHILD IS A FOLDER
                        if len(child.findChildren("a", recursive=False)):
                            item = parseFolder(child)
                            tree.children.append(item)
                        else: # CHILD IS A FILE
                            name = child.i.next_sibling.string.strip()
                            size = child.span.string[1:-1] # stripping parenthesis
                            item = NewItemModel("file", name, size=size)
                            tree.children.append(item)

                files = [tree]
            except:
                raise

            return Details(files, title, "Category", submitter, information, description)

    except:
        raise

def parseFolder(element):
    folderName = element.i.next_sibling.string.strip()
    folder = NewItemModel("folder", folderName)

    children = element.findChildren("a", recursive=False)[0].next_sibling.next_sibling.findChildren("li", recursive=False)
    for child in children:
        # CHILD IS A FOLDER
        if len(child.findChildren("a", recursive=False)):
            item = parseFolder(child)
            folder.children.append(item)
        else: # CHILD IS A FILE
            name = child.i.next_sibling.string.strip()
            size = child.span.string[1:-1] # stripping parenthesis
            item = NewItemModel("file", name, size=size)
            folder.children.append(item)

    return folder