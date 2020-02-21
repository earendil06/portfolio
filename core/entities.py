import urllib.request


class Blog:
    def __init__(self, title, date, filename) -> None:
        super().__init__()
        self.filename = filename
        self.date = date
        self.title = title

    def id(self):
        return self.filename.split('/')[-1].replace('.md', '').strip()

    def content(self):
        url = "https://raw.githubusercontent.com/earendil06/blog/master/{filename}".format(filename=self.filename)
        stream = urllib.request.urlopen(url)
        data = stream.read()
        stream.close()
        return data.decode("utf-8")

    def date_rss(self):
        if self.date == '':
            return self.date
        return '{date}T12:00:00+00:00'.format(date=self.date)

    def link(self):
        return 'https://portfolio.florentpastor.com/blog/' + self.id()


class Picture:
    def __init__(self, title, url):
        self.url = url
        self.title = title
