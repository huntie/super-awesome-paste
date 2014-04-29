# Intelligent paste handling for Sublime.
# @author Alex Hunt <https://github.com/huntie>

import sublime, sublime_plugin
import re

class SuperAwesomePasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        def get_file_type():
            if isinstance(self.view.file_name(), str):
                return self.view.file_name().split('.')[-1]

        def get_file_content():
            return self.view.substr(sublime.Region(0, self.view.size()));

        def strip_line_numbers(string):
            # If enough preceding line numbers are found (more than half of all lines)
            if len(re.findall(r'\n[ \t]*\d+\:?', string)) > len(string.splitlines()) / 2 - 2:
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
            body = get_file_content()
            preceding_text = body[:self.view.sel()[0].begin()]

            # If there existing semicolon-separated lines on the page
            if len(re.findall(r';[ \t]*\n', body)) > 1:
                # Split lines with multiple phrases by semicolons
                string = re.sub(r';[ \t]*(\w)', r';\n\1', string)

            # If the file content precedes with a quote
            if re.search(r'[\'\"][ \t]*$', preceding_text):
                # Merge lines separated by semicolons
                string = re.sub(r';[ \t]*\n[ \t]*(\w)', r'; \1', string)

            return string

        def normalise_line_endings(string):
            line_endings = self.view.settings().get('default_line_ending')

            # Reset line ending character
            string = string.replace('\r\n', '\n').replace('\r', '\n')
            # Strip trailing whitespace
            string = re.sub(r'[ \t]*\n', '\n', string)

            # Apply line endings of the current file
            if line_endings == 'windows':
                string = string.replace('\n', '\r\n')
            elif line_endings == 'mac':
                string = string.replace('\n', '\r')

            return string

        # Assign clipboard contents to paste_content
        paste_content = sublime.get_clipboard().strip()

        # Apply corrections to paste content
        paste_content = strip_line_numbers(paste_content)
        paste_content = normalise_line_endings(paste_content)
        paste_content = split_or_merge_lines(paste_content)

        # Make this command a single edit to undo
        self.edit = edit

        for region in self.view.sel():
            # Insert final clipboard content into currently selected regions
            self.view.replace(edit, region, paste_content)
            self.view.run_command('reindent', {'single_line': False})
            self.view.run_command('move', {'by': 'characters', 'forward': True})
