import sublime
import sublime_plugin
from .util import FileInfo, Preferences
from .paste import Paste

class SuperAwesomePasteCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
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

            if preferences.get_option('format_hex_colors'):
                paste.format_hex_colors()

            if 'html_encode' in args:
                paste.html_encode()

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
