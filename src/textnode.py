from enum import Enum

from extract_markdown import extract_markdown_images, extract_markdown_links
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if not extracted_images:
            new_nodes.append(node)
            continue
        for image in extracted_images:
            text_list = node.text.split(f"![{image[0]}]({image[1]})")
            if text_list[0] != "":
                new_nodes.append(TextNode(text_list[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node.text = text_list[1]

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue
        for link in extracted_links:
            text_list = node.text.split(f"[{link[0]}]({link[1]})")
            if text_list[0] != "":
                new_nodes.append(TextNode(text_list[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node.text = text_list[1]
        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.NORMAL_TEXT))

    return new_nodes
