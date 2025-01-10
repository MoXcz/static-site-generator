import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_header(self):
        text = """
# This is the header

A new line"""
        title = extract_title(text)
        self.assertEqual(title, "This is the header")
