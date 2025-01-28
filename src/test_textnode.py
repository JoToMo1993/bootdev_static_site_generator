import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, 'url')
        node2 = TextNode("This is a text node", TextType.BOLD, 'url')
        self.assertEqual(node, node2)

    def test_ne_text(self):
        node = TextNode("This is a text node1", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ne_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_ne_url(self):
        node = TextNode("This is a text node", TextType.BOLD, 'some')
        node2 = TextNode("This is a text node", TextType.BOLD, 'other')
        self.assertNotEqual(node, node2)

    def test_to_html(self):
        node_tuples = [
            (TextNode("This is a text node", TextType.NORMAL), LeafNode(''    , "This is a text node", None)),
            (TextNode("This is a text node", TextType.BOLD)  , LeafNode('b'   , "This is a text node", None)),
            (TextNode("This is a text node", TextType.ITALIC), LeafNode('i'   , "This is a text node", None)),
            (TextNode("This is a text node", TextType.CODE)  , LeafNode('code', "This is a text node", None)),
            (TextNode("This is a text node", TextType.LINKS  , 'url'), LeafNode('a'  , "This is a text node", {'href': 'url'})),
            (TextNode("This is a text node", TextType.IMAGES , 'url'), LeafNode('img', "", {'src': 'url', 'alt': 'This is a text node'})),
        ]

        for node_tuple in node_tuples:
            self.assertEqual(node_tuple[0].to_html_node(), node_tuple[1])

    def test_to_html_missing_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node.text_type = 'other'

        try:
            node.to_html_node()
            self.fail()
        except Exception as e:
            self.assertEqual(e.args[0], 'text_type other is not supported')


if __name__ == "__main__":
    unittest.main()