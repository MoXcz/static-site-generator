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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type is TextType.NORMAL_TEXT:
        return old_nodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise Exception(
                f"Delimter Error: The text could not be delmited with the provided delimiter: {delimiter}"
            )
        for i in range(len(text_list)):
            if text_list[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text_list[i], TextType.NORMAL_TEXT))
            else:
                new_nodes.append(TextNode(text_list[i], text_type))
    return new_nodes
