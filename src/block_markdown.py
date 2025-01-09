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


# Note that this could be achieved using the "startswith()" method for strings
def block_to_block_type(block):
    line_blocks = block.split("\n")
    counter = 0

    # Make sure that there's at least one #, and that there's no more than 6
    if len(block.split("# ")) > 1 and len(block.split("#")) <= 7:
        return "heading"

    # Make sure there are at least two ``` pairs
    if len(block.split("```")) > 2:
        return "code"

    for line in line_blocks:
        # Make sure the first character in each line is ">"
        if line.split(" ")[0] == ">":
            # by counting each line
            counter += 1
    # And only returning if every line in the quote starts with ">"
    if counter == len(line_blocks):
        return "quote"

    counter = 0  # Restart counter
    for line in line_blocks:
        # Make sure the first character in each line is "*" or "-"
        if line.split(" ")[0] == "*" or block.split(" ")[0] == "-":
            # by counting each line
            counter += 1
    # And only returning if every line in the quote starts with "*" or "-"
    if counter == len(line_blocks):
        return "unordered_list"

    counter = 0  # Restart counter
    for i in range(len(line_blocks)):
        # Make sure that each subsequent element in the list has "i + 1" as its index
        if line_blocks[i].split(" ")[0] == f"{i+1}.":
            # by counting each line
            counter += 1
    # And returning only if every line starts with a number and follows the appropriate index
    if counter == len(line_blocks):
        return "ordered_list"

    return "paragraph"


# I decided to not refactor this to show how I essentially reinvented the
# "startswith()" method for each case
