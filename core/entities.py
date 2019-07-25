from core.utils import get_file_lines


class Blog:
    def __init__(self, filepath="") -> None:
        super().__init__()
        self.filepath = filepath

    def line_start_with_pattern(self, pattern):
        for line in get_file_lines(self.filepath):
            if line.startswith(pattern):
                return line[len(pattern):].strip()
        return ''

    def id(self):
        return self.filepath.split('/')[-1].replace('.md', '').strip()

    def title(self):
        pattern = '# '
        return self.line_start_with_pattern(pattern)

    def content(self):
        return ''.join(get_file_lines(self.filepath))

    def date(self):
        pattern = '> date:'
        return self.line_start_with_pattern(pattern)

    def date_rss(self):
        regular_date = self.date()
        if regular_date == '':
            return ''
        return '%sT12:00:00+00:00'.format(self.date())

    def author(self):
        pattern = '> author:'
        return self.line_start_with_pattern(pattern)

    def link(self):
        return 'https://portfolio.florentpastor.com/blog/' + self.id()

    def is_valid(self):
        return self.id() != '' and self.title() != '' and self.date() != ''
