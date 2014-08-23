# Intelligent paste handling for Sublime.
# @author Alex Hunt <https://github.com/huntie>

import sublime, sublime_plugin
import re
import html

class SuperAwesomePasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        # Get current document contents
        body = self.view.substr(sublime.Region(0, self.view.size()))

        # Get content that precedes the selection
        preceding_text = body[:self.view.sel()[0].begin()]

        # Get current file type
        file_type = self.view.file_name().split('.')[-1] if self.view.file_name() else ''

        def get_clipboard():
            clipboard = sublime.get_clipboard()
            return clipboard.strip() if ('\n' in clipboard) else clipboard

        def get_option(key):
            return self.view.settings().get('super_awesome_paste.' + key)

        def normalise_line_endings(string):
            # Reset line ending characters
            string = re.sub(r'\r\n?', '\n', string)
            # Strip trailing whitespace
            string = re.sub(r'[ \t]*\n', '\n', string)

            return string

        def apply_line_endings(string):
            line_endings = self.view.settings().get('default_line_ending')

            if line_endings == 'windows':
                string = string.replace('\n', '\r\n')
            elif line_endings == 'mac':
                string = string.replace('\n', '\r')

            return string

        def clean_formatting(string):
            if '•' in string:
                if re.search(r'^md|markdown$', file_type):
                    # Convert bullet symbols to markdown list items
                    string = re.sub(r'(^|\n)•\t? ?', '\n+ ', string)
                else:
                    # Strip bullet symbol when pasting in an HTML list item
                    if re.search(r'<li[^<>]*?>[^<>]*$', preceding_text):
                        string = re.sub(r'(^|\n)•\t? ?', '', string)

            return string

        def strip_line_numbers(string):
            # If enough preceding line numbers are found (more than half of all lines)
            if (len(re.findall('\n', string)) > 2 and
                len(re.findall(r'\n[ \t]*\d+\:?', string)) > len(string.splitlines()) / 2 - 2):
                # Remove line number from first line
                string = re.sub(r'^[ \t]*\d+\:?[ \t]*\n?', '', string)

                # If a preceding line number is found on every line
                if len(re.findall(r'\n[ \t]*\d+\:?', string)) > len(string.splitlines()) - 2:
                    # Remove preceding numbers from subsequent lines
                    string = re.sub(r'\n[ \t]*\d+\:?', '\n', string)
                else:
                    # Remove preceding numbers and extra lines from subsequent lines
                    string = re.sub(r'\n[ \t]*\d+\:?', '', string)

            return string

        def split_or_merge_lines(string):
            # If there are enough existing semicolon-separated lines on the page
            if len(re.findall(r';[ \t]*\n', body)) > len(body.splitlines()) / 4:
                # Split lines with multiple phrases by semicolons
                string = re.sub(r';[ \t]*(\w)', r';\n\1', string)

            # If the file content precedes with a quote
            if re.search(r'[\'\"][ \t]*$', preceding_text):
                # Merge lines separated by semicolons
                string = re.sub(r';\n[ \t]*(\w)', r'; \1', string)

            return string

        def html_escape(string):
            # When pasting inside a content element
            if re.search(r'<(p|h[1-6]|span|em|strong|small|td)[^<>]*?>[^<>]*$', preceding_text):
                # If there are no tags or existing escaped entities present in the paste content
                if not re.search(r'[<>]|&[^\s]+;', string):
                    # Replace special characters with their HTML entity
                    string = html.escape(string)

            return string

        def format_urls(string):
            # Regex to match URLs adapted from Matthew O'Riordan <http://bit.ly/1mlEHm8>
            url = re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)'     # Match protocol
                                '([A-Za-z0-9\.\-]+)'            # domain
                                '|(?:www\.)[A-Za-z0-9\.\-]+)'   # OR www.domain
                                '((?:\/[\+~%\/\.\w\-_]*)'       # path
                                '?\??(?:[\-\+=&;%@\.\w_]*)'     # query string
                                '#?(?:[\.\!\/\\\w]*))?)')       # anchor

            if re.search(url, string):
                for this_url, start, protocol, domain, path in re.findall(url, string):
                    if not protocol:
                        if not (re.search(r'\/$', preceding_text) or not re.search(r'^\/', this_url)):
                            # Add a protocol to the start of the url if missing
                            string = string.replace(this_url, 'http://' + this_url)
                    if re.search(r'[A-Z]', start):
                        # If any uppercase characters are found, make the domain lowercase
                        string = string.replace(this_url, start.lower() + path)

            return string

        def format_hex_colors(string):
            hex_color = re.compile(r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

            # If paste content matches a hex triplet, deal with preceding hash or lack of appropriately
            if re.match(hex_color, string):
                if re.search(r'#$', preceding_text):
                    # Remove hash if present in file
                    string = string.replace('#', '')
                elif not '#' in string:
                    if re.search(r'^css|less|scss|sass$', file_type):
                        # Add hash if not included already
                        string = '#' + string
                # Convert to preferred case
                string = string.lower() if get_option('format_hex_colors') == 'lowercase' else string.upper()

            return string

        def show_message(string):
            if not string:
                sublime.status_message('Nothing to paste')
            elif '\n' in string:
                sublime.status_message('Pasted {} lines'.format(len(string.splitlines())))
            else:
                sublime.status_message('Pasted {0} character{1}'
                    .format(len(string), 's' if len(string) != 1 else ''))

        # Assign clipboard contents to paste_content
        paste_content = get_clipboard()

        if paste_content:
            # Apply corrections to paste content
            paste_content = normalise_line_endings(paste_content)
            paste_content = strip_line_numbers(paste_content)
            paste_content = split_or_merge_lines(paste_content)
            paste_content = clean_formatting(paste_content)

            if get_option('escape_html'):
                paste_content = html_escape(paste_content)

            if get_option('format_urls'):
                paste_content = format_urls(paste_content)

            paste_content = format_hex_colors(paste_content)
            paste_content = apply_line_endings(paste_content)

            for region in self.view.sel():
                # Insert final clipboard content into currently selected regions
                self.view.replace(edit, region, paste_content)

                # Reindent selected regions if pasted content spans multiple lines
                if ('\n' in paste_content) and file_type:
                    self.view.run_command('reindent', {'single_line': False})

            # Move caret to the right
            self.view.run_command('move', {'by': 'characters', 'forward': True})

        # Show status bar completion message
        show_message(paste_content)
