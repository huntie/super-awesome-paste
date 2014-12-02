"""
Intelligent paste handling for Sublime

Copyright (c) 2014 Alex Hunt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import sublime
import sublime_plugin
from .util import FileInfo, Preferences
from .paste import Paste

class SuperAwesomePasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get current file context
        file = FileInfo(self.view)
        # Get user preferences
        preferences = Preferences(self.view)
        # Create new paste instance
        paste = Paste(self.view, file, preferences)

        # Apply transformations to paste content and insert into file
        if not paste.is_empty():
            paste.normalise_line_endings()
            paste.strip_line_numbers()
            paste.split_or_merge_lines()
            paste.clean_formatting()
            paste.markdown_formatting()

            if preferences.get_option('escape_html'):
                paste.html_escape()

            if preferences.get_option('format_urls'):
                paste.format_urls()

            paste.format_hex_colors()
            paste.apply_line_endings()

            for region in self.view.sel():
                # Insert final clipboard content into currently selected regions
                self.view.replace(edit, region, paste.get_text())

                # Reindent selected regions if pasted content spans multiple lines
                if ('\n' in paste.text) and file.get_file_type():
                    self.view.run_command('reindent', {'single_line': False})

            # Move caret to the right
            self.view.run_command('move', {'by': 'characters', 'forward': True})

        # Show status bar completion message
        self.show_message(paste)

    def show_message(self, paste):
        if paste.is_empty():
            sublime.status_message('Nothing to paste')
        elif '\n' in paste.text:
            sublime.status_message('Pasted {} lines'.format(paste.line_count()))
        else:
            sublime.status_message('Pasted {0} character{1}'
                .format(paste.length(), 's' if paste.length() != 1 else ''))
