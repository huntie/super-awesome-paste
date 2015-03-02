# Super-Awesome Paste

Super-Awesome Paste is a Sublime Text 3 plugin which aims to intelligently integrate copied text into your code. Currently this includes normalising line endings and whitespace, auto-indentation, and cleaning up copied line numbers and unwanted formatting, including smart quotes. In addition, small contextual fixes such as HTML character escaping and hex colour formatting are applied when needed. Hopefully this plugin will save developers many keystrokes, and more features are always on the way.

## Getting started

The plugin is available through [Package Control](//sublime.wbond.net/packages/Super-Awesome%20Paste), but can also be installed manually by adding the [latest version](//github.com/huntie/super-awesome-paste/releases) to your Sublime Text 3 packages directory. By default, the `super_awesome_paste` command can be found in your context menu and is bound to `Ctrl+Alt+V`, but you may want to change this to something more convenient or to override the regular paste shortcut.

## Options

These options can be appended to your `Settings - User` file and are prefixed with the command name to avoid conflicts. For example:

```json
{
    "super_awesome_paste.escape_html": true
}
```

**escape_html**  
Type: `Boolean`  
Default: `true`

Convert certain special characters to their escaped HTML entities when pasted into a content tag within an HTML page.

**format_hex_colors**  
Type: `String`  
Default: `"lowercase"`

Specify preferred capitalisation for pasted hex colours - `"lowercase"` or `"uppercase"`. Set `false` to disable.

## Contributing

If you discover a problem or have a feature request, please [create an issue](//github.com/huntie/super-awesome-paste/issues) or feel free to fork this repository and make improvements.
