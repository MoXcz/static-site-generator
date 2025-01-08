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


def block_to_block_type(block):
    # Note that this could be achieved using the "startswith()" method for
    # strings
    line_blocks = block.split("\n")
    counter = 0
    if len(block.split("# ")) > 1 and len(block.split("#")) <= 7:
        return "heading"
    if len(block.split("```")) > 2:
        return "code"
    for line in line_blocks:
        if line.split(" ")[0] == ">":
            counter += 1
    if counter == len(line_blocks):
        return "quote"
    counter = 0
    for line in line_blocks:
        if line.split(" ")[0] == "*" or block.split(" ")[0] == "-":
            counter += 1
    if counter == len(line_blocks):
        return "unordered_list"
    counter = 0
    for i in range(len(line_blocks)):
        if line_blocks[i].split(" ")[0] == f"{i+1}.":
            counter += 1
    if counter == len(line_blocks):
        return "ordered_list"

    return "paragraph"
