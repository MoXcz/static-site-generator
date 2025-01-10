from block_markdown import markdown_to_blocks
from block_to_html import process_heading_text


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        text, num_hashes = process_heading_text(block)
        if num_hashes == 1:
            return text
    raise ValueError(f"No valid h1 header in: {markdown}")
