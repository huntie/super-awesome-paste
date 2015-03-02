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

    def is_markdown(self):
        return re.search(r'^md|markdown$', self.file_type)

    def is_txt_or_md(self):
        return re.search(r'^txt|md|markdown$', self.file_type)

    def is_stylesheet(self):
        return re.search(r'^css|less|scss|sass$', self.file_type)

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
    # Match a hex colour code of the form #aaaaaa or #aaa
    hex_color = re.compile(r'^#?((?:[A-Fa-f0-9]{2}){3}|[A-Fa-f0-9]{3})$')

    # Match a preceding section back to and including an opening HTML inline content tag such as
    # <h1> or <strong>
    html_opening_content_tag = re.compile(r'<(p|h[1-6]|span|em|strong|a|small|td)[^<>]*?>[^<>]*$')
