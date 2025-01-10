from os import listdir, makedirs, path

from block_markdown import markdown_to_blocks
from block_to_html import markdown_to_html_node, process_heading_text


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        text, num_hashes = process_heading_text(block)
        if num_hashes == 1:
            return text
    raise ValueError(f"No valid h1 header in: {markdown}")


def genereate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if path.exists(from_path):
        markdown_file = open(from_path).read()
        template_file = open(template_path).read()
        html_content = markdown_to_html_node(markdown_file).to_html()
        title = extract_title(markdown_file)
        template_file = template_file.replace("{{ Title }}", title).replace(
            "{{ Content }}", html_content
        )
        if not path.exists(dest_path):
            makedirs(path.dirname(dest_path), exist_ok=True)
            open(dest_path, "x").write(template_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for dir in listdir(dir_path_content):
        content_dir = path.join(dir_path_content, dir)
        dest_dir = path.join(dest_dir_path, dir).replace(".md", ".html")
        if path.isfile(content_dir):
            genereate_page(content_dir, template_path, dest_dir)
        else:
            if not path.exists(dest_dir):
                makedirs(dest_dir)
            generate_pages_recursive(content_dir, template_path, dest_dir)
