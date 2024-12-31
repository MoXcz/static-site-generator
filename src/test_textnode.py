import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a link node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://g.com")
        node2 = TextNode("This is an image node", TextType.IMAGE, "http://g.com")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a link node", TextType.LINK)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
