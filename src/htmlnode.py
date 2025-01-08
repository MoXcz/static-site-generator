import re
from enum import Enum

from block_markdown import block_to_block_type, markdown_to_blocks


class HTMLNode:
    # Props are HTML attributes
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("The method was not implemented")

    def props_to_html(self):
        prop_text = ""
        if self.props is None:
            return prop_text
        for key, value in self.props.items():
            prop_text += f' {key}="{value}"'

        return prop_text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Missing value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Parent node needs to have at least one children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"Parent Node({self.tag}, {self.children}, {self.props})"


def markdown_to_html_node(markdown):
    parent_list = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            parent_list.append(block_node_to_html_node(BlockNode(block, BlockType.H)))
        if block_type == "code":
            parent_list.append(
                block_node_to_html_node(BlockNode(block, BlockType.CODE))
            )
        if block_type == "paragraph":
            parent_list.append(block_node_to_html_node(BlockNode(block, BlockType.P)))
        if block_type == "quote":
            parent_list.append(
                block_node_to_html_node(BlockNode(block, BlockType.QUOTE))
            )
        if block_type == "unordered_list":
            parent_list.append(block_node_to_html_node(BlockNode(block, BlockType.UL)))
        if block_type == "ordered_list":
            parent_list.append(block_node_to_html_node(BlockNode(block, BlockType.OL)))

    return parent_list


class BlockType(Enum):
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"
    CODE = "code"
    H = "heading"
    P = "paragraph"


class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = BlockType(block_type)

    def __eq__(self, node):
        if self.text != node.text:
            return False
        if self.block_type != node.block_type:
            return False
        return True

    def __repr__(self):
        return f"BLockNode({self.text}, {self.block_type.value})"


def block_node_to_html_node(block_node):
    match block_node.block_type:
        case BlockType.QUOTE:
            children = process_blockquote_text(block_node.text)
            return HTMLNode("blockquote", None, children)
        case BlockType.UL:
            line_blocks = block_node.text.split("\n")
            list_items = []
            for item in line_blocks:
                list_items.append(
                    HTMLNode(
                        "li", markdown_block_node_to_text(item, "unordered_list_item")
                    )
                )
            return HTMLNode(
                "ul",
                None,
                list_items,
            )
        case BlockType.OL:
            line_blocks = block_node.text.split("\n")
            list_items = []
            for item in line_blocks:
                list_items.append(
                    HTMLNode(
                        "li", markdown_block_node_to_text(item, "ordered_list_item")
                    )
                )
            return HTMLNode(
                "ol",
                None,
                list_items,
            )
        case BlockType.CODE:
            code_node = HTMLNode(
                "code", markdown_block_node_to_text(block_node.text, "code")
            )
            return HTMLNode("pre", None, [code_node])
        case BlockType.H:
            match = re.match(r"^(#+) ", block_node.text)
            if match:
                num_hashes = len(match.group(1))
                text = block_node.text[num_hashes + 1 :]
                return HTMLNode(f"h{num_hashes}", text)
        case BlockType.P:
            return HTMLNode("p", block_node.text)


def markdown_block_node_to_text(markdown, block_type):
    match block_type:
        case "code":
            return markdown.replace("```", "")
        case "quote":
            return markdown.replace("> ", "")
        case "unordered_list_item":
            return markdown.replace("* ", "").replace("- ", "")
        case "ordered_list_item":
            match = re.match(r"^\d+\.\s", markdown)
            if match:
                return markdown[match.end() :]
        case _:
            return markdown


def process_blockquote_text(text):
    lines = text.split("\n")
    children = []
    for line in lines:
        if line.strip() != "":
            children.append(HTMLNode("p", markdown_block_node_to_text(line, "quote")))
    return children


# TODO: This is how the end result should look like for a node:
# HTMLNode("p", None, [
#     TextNode("This is a "),  # TextNode for plain text
#     HTMLNode("strong", "bold", None),  # HTMLNode for bold text
#     TextNode(" and "),  # TextNode for plain text
#     HTMLNode("em", "italic", None),  # HTMLNode for italicized text
#     TextNode(" text."),  # TextNode for plain text
# ])
