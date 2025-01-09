import re
from enum import Enum

from block_markdown import block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


# Decided to use an Enum to structure the different "types" an HTML block could have
# so that the "block_node_to_html_node()" function could accept a class structure
class BlockType(Enum):
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"
    CODE = "code"
    H = "heading"
    P = "paragraph"


# The class used in the aforementioned function
class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = BlockType(block_type)

    # Used for Debugging
    def __eq__(self, node):
        if self.text != node.text:
            return False
        if self.block_type != node.block_type:
            return False
        return True

    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type.value})"


def markdown_to_html_node(markdown):
    children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            children.append(block_node_to_html_node(BlockNode(block, BlockType.H)))
        if block_type == "code":
            children.append(block_node_to_html_node(BlockNode(block, BlockType.CODE)))
        if block_type == "paragraph":
            children.append(block_node_to_html_node(BlockNode(block, BlockType.P)))
        if block_type == "quote":
            children.append(block_node_to_html_node(BlockNode(block, BlockType.QUOTE)))
        if block_type == "unordered_list":
            children.append(block_node_to_html_node(BlockNode(block, BlockType.UL)))
        if block_type == "ordered_list":
            children.append(block_node_to_html_node(BlockNode(block, BlockType.OL)))

    return ParentNode("div", children, None)


# This class receives a "BlockNode' instance with some text and type to "match"
# the different cases and parse the "text" field into its assigned "block_type"
# field of HTML (returned as a "ParentNode" instance
def block_node_to_html_node(block_node):
    match block_node.block_type:
        case BlockType.QUOTE:
            return ParentNode(
                "blockquote",
                text_to_children(process_blockquote_text(block_node.text)),
            )
        case BlockType.UL:
            line_blocks = block_node.text.split("\n")
            list_items = []
            for item in line_blocks:
                # First get all list items
                list_items.append(
                    ParentNode(
                        "li",
                        text_to_children(
                            markdown_block_node_to_text(item, "unordered_list_item"),
                        ),
                    )
                )
            # And then add them as children of the parent element
            return ParentNode("ul", list_items, None)
        case BlockType.OL:
            line_blocks = block_node.text.split("\n")
            list_items = []
            for item in line_blocks:
                # First get all list items
                list_items.append(
                    ParentNode(
                        "li",
                        text_to_children(
                            markdown_block_node_to_text(item, "ordered_list_item")
                        ),
                    )
                )
            # And then add them as children of the parent element
            return ParentNode("ol", list_items, None)
        case BlockType.CODE:
            code_node = ParentNode(
                "code",
                text_to_children(markdown_block_node_to_text(block_node.text, "code")),
            )
            return ParentNode("pre", [code_node])
        case BlockType.H:
            # Match any hashes #
            match = re.match(r"^(#+) ", block_node.text)
            if match:
                num_hashes = len(match.group(1))
                # Remove all hashes by returning the string without them
                text = block_node.text[num_hashes + 1 :]  # +1 because of " "
                return ParentNode(f"h{num_hashes}", text_to_children(text))
        case BlockType.P:
            return ParentNode(
                "p",
                # Remove new lines from text
                text_to_children(" ".join(block_node.text.split("\n"))),
            )


# In the beginning was going to be used to remove all Markdown syntax from the
# text, but ended up being quite cumbersome. Decided not to refactor it to leave
# traces of my thought process
def markdown_block_node_to_text(markdown, block_type):
    match block_type:
        case "code":
            return markdown.replace("```", "").strip()
        case "quote":
            return markdown[2:]  # Remove "> " from text
        case "unordered_list_item":
            return markdown[2:]  # Remove any "* " and "- " from text
        case "ordered_list_item":
            return markdown[3:]  # Remove any index "n. " where "n" is a number
        case _:  # In case it's used in a paragraph it return the same text
            return markdown


# This helper function is used to convert Markdown quote lines (">") into a
# single string of text so that it can be used in "text_to_children()"
def process_blockquote_text(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if line.strip() != "":
            new_lines.append(markdown_block_node_to_text(line, "quote"))
    return " ".join(new_lines)


# This helper function is used to convert text (without Markdown characters)
# into instances of "LeafNode"s (which are inline HTML elements)
# This facilitates having to write a specific conversion for each "match" by
# receiving only the text
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
