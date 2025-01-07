def markdown_to_blocks(markdown):
    # Trim whitespace of blocks
    markdown = list(map(lambda x: x.strip(), markdown.split("\n\n")))
    markdown_blocks = []
    # Pop any empty string (usually extra spaces at the end)
    for block in markdown:
        if block == "":
            continue
        markdown_blocks.append(block)
    return markdown_blocks
