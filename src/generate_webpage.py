from os import makedirs, path

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
