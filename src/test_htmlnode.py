import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.tag, node2.tag)

    def test_not_eq(self):
        node = HTMLNode("p", "this is a paragraph", None, {"class": "paragraph"})
        node2 = HTMLNode("h1", "this is a header", None, {"class": "header"})
        self.assertNotEqual(node.value, node2.value)

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

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "lazy"},
        )
        self.assertEqual(
            "HTMLNode(p, What a strange world, None, {'class': 'lazy'})", repr(node)
        )

    def test_to_html_no_children(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )

    def test_to_html_no_children_2(self):
        node = LeafNode("a", "Click me!")
        self.assertEqual("<a>Click me!</a>", node.to_html())

    def test_repr_no_children(self):
        node = LeafNode(
            "p",
            "What a strange world",
            {"class": "way-too-lazy"},
        )
        self.assertEqual(
            "LeafNode(p, What a strange world, {'class': 'way-too-lazy'})", repr(node)
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_children_2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i><p><b>Bold text</b></p></p>",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_repr_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "Parent Node(div, [LeafNode(span, child, None)], None)",
            repr(parent_node),
        )


if __name__ == "__main__":
    unittest.main()
