from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, node):
        if self.text != node.text:
            return False
        if self.text_type != node.text_type:
            return False
        if self.url != node.url:
            return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode(
                "a",
                text_node.text,
                {"href": text_node.url},
            )
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError(f"Invalid text node type: {text_node.text_type}")
