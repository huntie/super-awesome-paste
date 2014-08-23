# Super-Awesome Paste

*A Sublime Text plugin that tidies up and contextually formats pasted content.*

Super-Awesome Paste aims to intelligently integrate copied text into your code, and currently normalises line endings and whitespace, removes copied line numbers & extra formatting and automatically indents the result. In addition, fixes such as URL tidying and HTML character escaping are applied depending on the paste context. More features are planned soon, and you can read more about the project in this [blog post](//hunt.ghost.io/improving-paste-formatting-in-sublime-text/).

**Requirements:** Sublime Text 3

## Getting started

The plugin is now available through [Package Control](//sublime.wbond.net/packages/Super-Awesome%20Paste), but can also be installed manually by adding the [latest version](//github.com/huntie/super-awesome-paste/releases) to your Sublime Text 3 packages directory. You should then open Sublime to find the command added to your context menu. By default, the `super_awesome_paste` command is bound to `Ctrl+Alt+V`, but you may want to change this to something more convenient or to override the regular paste shortcut.

## Options

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

**format_hex_colors**  
Normalise capitalisation of hex colour triplets to `"uppercase"` or `"lowercase"`.

## Contributing

If you discover a problem or have a feature request, please [create an issue](//github.com/huntie/super-awesome-paste/issues) or feel free to fork this repository and make improvements.
