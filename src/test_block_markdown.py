import unittest

from block_markdown import block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_extract_images(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

    """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        markdown = "## Hi, I'm a heading"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, "heading")

    def test_code(self):
        markdown = "```This is a block\nof code```"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, "code")

    def test_paragraph(self):
        markdown = "##Hi, this is a paragraph with *italics*"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, "paragraph")

    def test_quote(self):
        markdown = "> This\n> is\n> a quote"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, "quote")

    def test_unordered_list(self):
        markdown = "* This\n* is\n* an unordered list"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, "unordered_list")

    def test_ordered_list(self):
        markdown = "1. This is\n2. An ordered\n3. list"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, "ordered_list")

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")


if __name__ == "__main__":
    unittest.main()
