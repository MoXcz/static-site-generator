from copy_static_files import src_to_dir
from generate_webpage import generate_pages_recursive
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    dir_public = "docs/"  # delete this one
    dir_static = "static/"  # copy to this one
    src_to_dir(dir_static, dir_public)
    content_path = "content/"
    template_file = "template.html"
    public_path = "docs/"
    generate_pages_recursive(content_path, template_file, public_path, basepath)


if __name__ == "__main__":
    main()
