![](logo.png)

# WebSFCL 🌎

WebSCFL stands for *Web Sectioned Command First Language*. It's a programming language
designed to make simple [Prof. Dr. Style](http://contemporary-home-computing.org/prof-dr-style/)
websites. The websites can be later customized further configured using CSS. I designed it
because I always end up fighting against CSS and changing the style of my sites and I'd like
to actually focus on the content instead of the styling.

## Usage

### Directory Setup

WebSCFL expects the project directory to be configured with four foulders and the WebSCFL build
file:

```
/images
/include
/other
/src
scfl_build.py
```

Each folder plays a different role in building your webpage.
- The `src` folder should only contain `.scfl` files. A file called `x.scfl` will be compiled to `x.html` when building your webpage.
- The `images` folder should include the images you'll use in your `.scfl` files. WebSCFL only looks for images in this directory and only copies the images that are actually used to the final built webpage.
- The `include` folder may include your stylesheet file and any other `.html` files you want to include verbatim into your built pages using the `INCLUDE` command.
- The `other` folder includes files used by WebSCFL when compiling your webpage. You might edit them, but make sure not to remove any of these files.

## WebSCFL Files
WebSCFL turns `.scfl` files into `.html` files that can be displayed on your browser.
Any `.scfl` files that you want to include in your webpage must be added to the `src` folder.
Basic `.scfl` files must contain two sections, a HEAD and a BODY:

```
HEAD:
...

BODY:
...

```

Each section accepts different commands. A command is a word written in a line, followed by
a linespace and any arguments the command might accept. If a command accepts multiple arguments,
they must be separated using a `,` character. For example:

```
PAGETITLE My wonderful site!
```

Will set the title displayed by the browser when visiting that page to *My wonderful site!*.

## Example WebSCFL Page
Here's a very basic example WebSCFL page.

```
HEAD:
PAGETITLE    My amazing website!
DESCRIPTION  This is my amazing website.
BACKGROUND   pagebackground.png
STYLE        style.css

BODY:
TITLE        Hello
WRITE        Welcome to my amazing website!
LINK         Visit Github!, https://github.com/

```

That will generate a website that looks like this (depending, obviously on the contents
of your stylesheet file (in this case `style.css`, to be found in the `include` folder):

![](example.png)

## WebSCFL Commands

This section lists the commands that can be used in each section, along with their arguments.

### HEAD Section Commands
These commands must be in the section defined by the `HEAD:` section separator.

- `PAGETITLE`
   - Sets the title of the page to be displayed by the browser when visiting it.
   - Example: `PAGETITLE my great page`
- `DESCRIPTION`
   - Sets the description of your website, to be displayed by, for example, search engines.
   - Example: `DESCRIPTION this site contains all my amazing stuff`
- `STYLE`
   - Sets the stylesheet file for the page. The file is expected to be found in the `include` folder.
   - Example: `STYLE mystyles.css`
- `BACKGROUND`
   - Sets the tiled page background image. The image is expected to be found in the `images` folder.
   - Example: `BACKGROUND mybackground.gif`

### BODY Section Commands
These commands must be in the section defined by the `BODY:` section separator.

- `TITLE`
   - Adds big title text to the page.
   - Example: `TITLE Welcome!`
- `HEADER`
   - Adds mid title text to the page.
   - Example: `HEADER A section!`
- `SUBHEADER`
   - Adds small title text to the page.
   - Example: `SUBHEADER A section within a section!`
- `WRITE`
   - Adds text to the page. Text added is appended to previous text added using `WRITE` unless another element such as an image or a break have been added in the middle.
   - Example: `WRITE Welcome to my website! Here you'll find amazing stuff!`
- `LINK`
   - Adds a link to another website or page within your site. Optionally, you can specify some text to be appended to the link (but not to be a link) immediately after it.
   - Example for a link without appended text: `LINK Google, https://www.google.com`
   - Example for a link to another page within your site: `LINK About Me, about.html`
   - Example for a link with appended text: `LINK Google, https://www.google.com, ; the famous search engine.`
- `IMAGE`
   - Adds an image to your page. The image will be displayed on its own line. Optionally, you can specify any CSS classes to be used to style this image. These classes should be defined within your used stylesheet file.
   - Example without CSS styling: `IMAGE mypicture.png`
   - Example with CSS styling: `IMAGE mypicture.png, bigpicture, shadowed`
- `LINKIMAGE`
   - Adds an image to your page that, when clicked, will take the user to another page or website. Optionally, you can specify any CSS classes to be used to style this image. These classes should be defined within your used stylesheet file.
   - Example without CSS styling: `LINKIMAGE lartu.png, https://www.lartu.net/`
- `FOOTNOTE`
   - Adds small text to your page. This text is displayed on its own and it's used to add notes to paragraphs or footers to images.
   - Example: `FOOTNOTE This is a picture of me at the beach.`
- `BREAK`
   - Adds spacing to break text added via `WRITE` into paragraphs.
   - Example: `BREAK`
- `LISTITEM`
   - Adds a bulleted list element to the page.
   - Example: `LISTITEM element1`
   - Example: `LISTITEM element2`
   - Example: `LISTITEM element3`

### Any Section Commands
- `INCLUDE`
   - Copies the contents of another file verbatim into the generated `.html` file. The other file is expected to be foun in the `include` folder.
   - Example: `INCLUDE somecontent.html`
- `COPY`
   - Copies a file from a directory into the `docs` (build) directory.
   - Example: `COPY awonderfulapp.exe downloads/awonderfulapp.exe`

# License
WebSCFL is released under the Apache 2 license. Copyright © Lartu, 2024.
