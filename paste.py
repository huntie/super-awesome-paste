import sublime
import html
import re
from .util import RegexPatterns

class Paste:
    def __init__(self, view, file_info, preferences):
        self.view = view
        self.file = file_info
        self.preferences = preferences

        # Load current text from clipboard, clear if empty
        self.text = sublime.get_clipboard()
        if re.match(r'^$|\s+', self.text): self.text.strip()

    def get_text(self):
        return self.text

    def is_empty(self):
        return not len(self.text)

    def length(self):
        return len(self.text)

    def line_count(self):
        return len(self.text.splitlines())

    def normalise_line_endings(self):
        # Reset line ending characters
        self.text = re.sub(r'\r\n?', '\n', self.text)
        # Strip trailing whitespace
        self.text = re.sub(r'[ \t]*\n', '\n', self.text)

    def apply_line_endings(self):
        # Get user line ending preference
        line_endings = self.view.settings().get('default_line_ending')

        # Use preference to adjust line ending characters
        if line_endings == 'windows':
            self.text =  self.text.replace('\n', '\r\n')
        elif line_endings == 'mac':
            self.text =  self.text.replace('\n', '\r')

    def clean_formatting(self):
        # Strip bullet symbol when pasting in an HTML list item
        if re.search(r'<li[^<>]*?>[^<>]*$', self.file.get_contents_before()):
            self.text = re.sub(r'(^|\n)•\t? ?', '', self.text)

        if not self.file.is_txt_or_md() and self.file.is_type_defined():
            # Normalise any found smart quotes
            self.text = re.sub(r'[‘’]', '\'', self.text)
            self.text = re.sub(r'[“”]', '"', self.text)

    def markdown_formatting(self):
        if self.file.is_markdown():
            # Convert bullet symbols to markdown list items
            self.text = re.sub(r'(^|\n)•\t? ?', '\n+ ', self.text)

    def strip_line_numbers(self):
        # If enough preceding line numbers are found (more than half of all lines)
        if (len(re.findall('\n', self.text)) > 2 and
            len(re.findall(r'\n[ \t]*\d+\:?', self.text)) > len(self.text.splitlines()) / 2 - 2):
            # Remove line number from first line
            self.text = re.sub(r'^[ \t]*\d+\:?[ \t]*\n?', '', self.text)

            # If a preceding line number is found on every line
            if len(re.findall(r'\n[ \t]*\d+\:?', self.text)) > len(self.text.splitlines()) - 2:
                # Remove preceding numbers from subsequent lines
                self.text = re.sub(r'\n[ \t]*\d+\:?', '\n', self.text)
            else:
                # Remove preceding numbers and extra lines from subsequent lines
                self.text = re.sub(r'\n[ \t]*\d+\:?', '', self.text)

    def split_or_merge_lines(self):
        if len(re.findall(r';[ \t]*\n', self.file.get_contents())) > self.file.line_count() / 4:
            # If there are enough existing semicolon-separated lines on the page,
            # split lines with multiple phrases by semicolons
            self.text = re.sub(r';[ \t]*(\w)', r';\n\1', self.text)

        if re.search(r'[\'\"][ \t]*$', self.file.get_contents_before()):
            # If the file content precedes with a quote, merge lines separated by semicolons
            self.text = re.sub(r';\n[ \t]*(\w)', r'; \1', self.text)

    def html_encode(self):
        self.text = html.escape(self.text)

    def format_hex_colors(self):
        if re.match(RegexPatterns.hex_color, self.text):
            # If paste content matches a hex triplet, remove or add a preceding hash as needed
            if re.search(r'#$', self.file.get_contents_before()):
                self.text = self.text.replace('#', '')
            elif not '#' in self.text:
                if self.file.is_stylesheet():
                    self.text = '#' + self.text

            # Convert to preferred case
            if self.preferences.get_option('format_hex_colors') == 'lowercase':
                self.text = self.text.lower()
            elif self.preferences.get_option('format_hex_colors') == 'uppercase':
                self.text = self.text.upper()

            # If possible, shorten to a three digit colour code
            if self.file.is_stylesheet():
                self.text = re.sub(r'(\w)\1(\w)\2(\w)\3', r'\1\2\3', self.text)
