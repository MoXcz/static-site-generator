from copy_static_files import src_to_dir
from generate_webpage import genereate_page


def main():
    dir_public = "public/"  # delete this one
    dir_static = "static/"  # copy to this one
    src_to_dir(dir_static, dir_public)
    markdown_file = "content/index.md"
    template_file = "template.html"
    destionation_path = "public/index.html"
    genereate_page(markdown_file, template_file, destionation_path)


if __name__ == "__main__":
    main()
