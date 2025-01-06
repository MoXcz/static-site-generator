import re


def extract_markdown_images(text):
    # Pattern extract markdown images in the following format:
    # [("alt text", "image url"), ]
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # Pattern extract markdown links in the following format:
    # [("alt text", "link url"), ]
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
