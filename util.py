import sublime
import re

class FileInfo:
    def __init__(self, view):
        self.view = view
        # Get current file extension
        self.file_type = self.view.file_name().split('.')[-1] if self.view.file_name() else ''
        # Get current document body
        self.contents = view.substr(sublime.Region(0, view.size()))

    def get_file_type(self):
        return self.file_type.lower()

    def is_type_defined(self):
        return len(self.file_type) > 0

    def get_contents(self):
        return self.contents

    def get_contents_before(self):
        # Get content that precedes the current selection
        return self.contents[:self.view.sel()[0].begin()]

    def line_count(self):
        return len(self.contents.splitlines())

class Preferences:
    def __init__(self, view):
        self.settings = view.settings()

    def get_option(self, key):
        return self.settings.get('super_awesome_paste.' + key)

class RegexPatterns:
    # Match a hex colour code of the form #AAAAAA or #AAA
    hex_color = re.compile(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

    # Match a web URL - adapted from Matthew O'Riordan (http://bit.ly/1mlEHm8)
    url = re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)'     # protocol
                        '([A-Za-z0-9\.\-]+)'            # domain
                        '|(?:www\.)[A-Za-z0-9\.\-]+)'   # or 'www.domain'
                        '((?:\/[\+~%\/\.\w\-_]*)'       # path
                        '?\??(?:[\-\+=&;%@\.\w_]*)'     # query string
                        '#?(?:[\.\!\/\\\w]*))?)')       # anchor

    # Match a preceding section back to and including an opening HTML inline content tag such as
    # <h1> or <strong>
    html_opening_content_tag = re.compile(r'<(p|h[1-6]|span|em|strong|a|small|td)[^<>]*?>[^<>]*$')
