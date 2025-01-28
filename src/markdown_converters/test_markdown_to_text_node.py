import unittest

from markdown_converters.markdown_to_text_node import textnodes_from_markdown, extract_markdown_images, \
    extract_markdown_links
from textnode import TextNode, TextType


class TestMarkdownToTextNode(unittest.TestCase):

    def test_textnodes_from_markdown(self):
        test_cases = [
            ('This is text with a **bolded phrase** in the middle', [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.NORMAL),
            ]),
            ('Just some text', [
                TextNode("Just some text", TextType.NORMAL),
            ]),
            ('**Just some bold text**', [
                TextNode("Just some bold text", TextType.BOLD),
            ]),
            ('**Some bold text****more bold text**', [
                TextNode("Some bold text", TextType.BOLD),
                TextNode("more bold text", TextType.BOLD),
            ]),
            ('*italic*other**bold**', [
                TextNode("italic", TextType.ITALIC),
                TextNode("other", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
            ]),
            ('This is text with a `code block` word', [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ]),
            ('Some text [link text](url) other text', [
                TextNode("Some text ", TextType.NORMAL),
                TextNode("link text", TextType.LINKS, 'url'),
                TextNode(" other text", TextType.NORMAL),
            ]),
            ('Some text [link text](url) other text [other link text](other.url)', [
                TextNode("Some text ", TextType.NORMAL),
                TextNode("link text", TextType.LINKS, 'url'),
                TextNode(" other text ", TextType.NORMAL),
                TextNode("other link text", TextType.LINKS, 'other.url'),
            ]),
            ('Some text ![alt text](url) other text', [
                TextNode("Some text ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGES, 'url'),
                TextNode(" other text", TextType.NORMAL),
            ]),
            # Testcase from website
            ('This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)', [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ])
        ]

        for test_case in test_cases:
            text = test_case[0]
            expected = test_case[1]

            res = textnodes_from_markdown(text)

            self.assertEqual(len(expected), len(res))
            for expected, actual in zip(expected, res):
                self.assertEqual(expected, actual)

    def test_extract_markdown_images(self):
        test_cases = [
            ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]),
            ("empty", [])
        ]

        for test_case in test_cases:
            text = test_case[0]
            expected = test_case[1]

            res = extract_markdown_images(text)

            self.assertEqual(len(expected), len(res))
            for expected, actual in zip(expected, res):
                self.assertEqual(expected, actual)

    def test_extract_markdown_links(self):
        test_cases = [
            ("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]),
            ("empty", [])
        ]

        for test_case in test_cases:
            text = test_case[0]
            expected = test_case[1]

            res = extract_markdown_links(text)

            self.assertEqual(len(expected), len(res))
            for expected, actual in zip(expected, res):
                self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
