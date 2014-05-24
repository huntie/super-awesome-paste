## Super-Awesome Paste

*A Sublime Text plugin that tidies up and contextually formats pasted content.*

Super-Awesome Paste is at an early stage and currently supports the removal of copied line numbers, basic indentation and whitespace corrections as well as URL formatting and HTML character escaping, plus splitting or merging lines when appropriate - with much more to come soon.

**Requirements:** Sublime Text 3

### Getting started

The plugin will soon be available through [Package Control](https://sublime.wbond.net/), but can also be installed manually by adding the [latest version](https://github.com/huntie/super-awesome-paste/releases) to your Sublime Text 3 packages directory. You should then open Sublime to find the command added to your context menu. By default, the `super_awesome_paste` command is bound to `Ctrl+Alt+V`, but you may want to change this to something more convenient or to override the regular paste shortcut.

### Options

These options can be appended to your `Settings - User` file and are prefixed with the command name to avoid conflicts. For example:

```json
{
    "super_awesome_paste.format_urls": true
}
```

**escape_html**
If set to `true` certain special characters are converted to their equivalent HTML entities when pasted into markup.

**format_urls**
If set to `true` tidies up URLs by adding an HTTP protocol and converting to lowercase when needed.

### Contributing

If you discover a problem or have a feature request, please [create an issue](https://github.com/huntie/super-awesome-paste/issues) or feel free to fork this repository and make improvements.
