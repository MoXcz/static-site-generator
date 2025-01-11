# Static Site Generator

This program converts Markdown documents into static web pages.

The static files (like images, CSS files, etc) must be inside the `static/`
directory. In the example provided it has an `index.css` for the styling and
an `images/` directory for all images used.

The generation is done following these steps:
1. Copy all static files inside `static/` to `public/`
2. *Recursively* generate `html` files from `md` files inside `content/` to `public/`:
    1. Divide Markdown file contents into *blocks*
    2. Convert *blocks* into `ParentNode`s (header, paragraph, lists, code,
       ordered list, unordered list and quote)
    3. Convert text content into `TextNode`s (italic, bold, inline code, image,
       link and normal text)
    4. Add the utmost `ParentNode` inside a `<div>` element
    5. Replace `<div>` element inside `template.html`
    6. Replace page title with the header 1 (`<h1>` or `#`)

Note that the *order* of files is preserved, so `content/` must be nested
exactly as the files are referred to inside the Markdown files.

## Installation

- This project uses Python and thus the Python interpreter is needed, click
  [here](https://www.python.org/downloads/) for more information on how to install
  it.

To start first clone the repository:

```sh
git clone https://github.com/MoXcz/static-site-generator.git --depth 1
```

After that just run the program using `main.sh`:

```sh
./main.sh
```

## Use

1. Copy all your Markdown files inside `content/` and all your static files
inside `static/`.
2. Run the program.
