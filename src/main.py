from copy_static_files import src_to_dir
from generate_webpage import generate_pages_recursive
import sys


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    public_path = "docs/"
    dir_static = "static/"  # copy to this one
    src_to_dir(dir_static, public_path)
    content_path = "content/"
    template_file = "template.html"
    generate_pages_recursive(content_path, template_file, public_path, basepath)


if __name__ == "__main__":
    main()
