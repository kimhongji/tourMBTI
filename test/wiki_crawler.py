import wikipediaapi


class WiKiCrawler:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('ko')

    def is_exist(self, word):
        page_py = self.wiki.page(word)
        if page_py.exists():
            return True
        else:
            return False

    def search(self, word):
        page_py = self.wiki.page(word)
        return page_py.summary
