# Static Site Generator

This program converts Markdown documents into static web pages.

The static files (like images, CSS files, etc) must be inside the `static/`
directory. In the example provided it has an `index.css` for the styling and
an `images/` directory for all images used.

The generation is done following these steps:
1. Copy all static files inside `content_path` to `public_path`
2. *Recursively* generate `html` files from `md` files inside `content_path` to `public_path`:
    1. Divide Markdown file contents into *blocks*
    2. Convert *blocks* into `ParentNode`s (header, paragraph, lists, code,
       ordered list, unordered list and quote)
    3. Convert text content into `TextNode`s (italic, bold, inline code, image,
       link and normal text)
    4. Add the utmost `ParentNode` inside a `<div>` element
    5. Replace `<div>` element inside `template.html`
    6. Replace page title with the header 1 (`<h1>` or `#`)

Note that the *order* of files is preserved, so `content_path` must be nested
exactly as the files are referred to inside the Markdown files.

## Installation

- This project uses Python and thus the Python interpreter is needed, click
  [here](https://www.python.org/downloads/) for more information on how to install
  it.

To start first clone the repository:

```sh
git clone https://github.com/MoXcz/static-site-generator.git --depth 1
```

This program can be uploated both in local or with GitHub pages (have not tested
using any other hosting services, but I assume it would work more or less the
same).

`main.sh` will run the program so that the generated content can be viewed in `http://localhost:8888/`:

```sh
./main.sh
```

`build.sh` will run the program so that the generate content can be viewed in `https://<user>.github.io/<repo>/`:
```sh
./build.sh
```

## Use

1. Copy all your Markdown files inside `content_path` and all your static files
inside `static/`.
2. Run the program.
