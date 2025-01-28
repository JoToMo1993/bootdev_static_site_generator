import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_none_value(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_single_value(self):
        node = HTMLNode(props={'dummy':'prop'})
        self.assertEqual(node.props_to_html(), ' dummy="prop"')

    def test_props_to_html_multi_value(self):
        node = HTMLNode(props={'dummy':'prop', 'other':'prop2'})
        self.assertEqual(node.props_to_html(), ' dummy="prop" other="prop2"')

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(value='value')
        self.assertEqual(node.to_html(), 'value')

    def test_to_html_empty_tag(self):
        node = LeafNode(value='value', tag='')
        self.assertEqual(node.to_html(), 'value')

    def test_to_html_tag(self):
        node = LeafNode(value='value', tag='p')
        self.assertEqual(node.to_html(), '<p>value</p>')

    def test_to_html_tag_and_props(self):
        node = LeafNode(value='value', tag='p', props={'dummy':'prop'})
        self.assertEqual(node.to_html(), '<p dummy="prop">value</p>')

    def test_to_html_no_value(self):
        node = LeafNode(value=None, tag='tag', props={'dummy':'prop'})
        try:
            node.to_html()
            self.fail()
        except ValueError as e:
            self.assertEqual(e.args[0], 'value cannot be None')

class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode(tag=None, children=[LeafNode(), LeafNode()], props={'dummy':'prop'})
        try:
            node.to_html()
            self.fail()
        except ValueError as e:
            self.assertEqual(e.args[0], 'tag cannot be None or empty')

    def test_to_html_empty_tag(self):
        node = ParentNode(tag='', children=[LeafNode(), LeafNode()], props={'dummy':'prop'})
        try:
            node.to_html()
            self.fail()
        except ValueError as e:
            self.assertEqual(e.args[0], 'tag cannot be None or empty')

    def test_to_html_no_children(self):
        node = ParentNode(tag='tag', children=None, props={'dummy':'prop'})
        try:
            node.to_html()
            self.fail()
        except ValueError as e:
            self.assertEqual(e.args[0], 'children cannot be None or empty')

    def test_to_html_empty_children(self):
        node = ParentNode(tag='tag', children=[], props={'dummy':'prop'})
        try:
            node.to_html()
            self.fail()
        except ValueError as e:
            self.assertEqual(e.args[0], 'children cannot be None or empty')

    def test_to_html_no_props(self):
        node = ParentNode(
            'p',
            [
                LeafNode('b', 'Bold text'),
                LeafNode(None, 'Normal text'),
                LeafNode('i', 'Italic text'),
                LeafNode(None, 'Normal text'),
             ])
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>')

if __name__ == "__main__":
    unittest.main()