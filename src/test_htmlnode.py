import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.tag, node2.tag)

    def test_not_eq(self):
        node = HTMLNode("p", "this is a paragraph", None, {"class": "paragraph"})
        node2 = HTMLNode("h1", "this is a header", None, {"class": "header"})
        self.assertNotEqual(node, node2)

    def test_props(self):
        node = HTMLNode(
            "p",
            "this is a paragraph",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )


if __name__ == "__main__":
    unittest.main()
