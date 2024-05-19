!()[logo.png]

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
a linespace and any arguments the command might accept. For example:

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

```

That will generate a website that looks like this (depending, obviously on the contents
of your stylesheet file (in this case `style.css`, to be found in the `include` folder):

![](example.png)
