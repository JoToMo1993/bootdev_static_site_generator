import unittest

from htmlnode import ParentNode, LeafNode
from markdown_converters.markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType, TextBlock, \
    block_to_text_block, markdown_to_html_nodes
from textnode import TextNode, TextType


class MarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        test_cases = [
            ('', []),
            ('\n', []),
            ('\n\n', []),
            ('\n\n\n', []),
            ('a', ['a']),
            ('a\nb', ['a\nb']),
            ('a\n\nb', ['a', 'b']),
            ('a\n\n\nb', ['a', 'b']),
            ("""
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
                """, [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ])
        ]

        for test_case in test_cases:
            text = test_case[0]
            expected = test_case[1]

            self.assertEqual(markdown_to_blocks(text), expected)

    def test_block_to_block_type(self):
        test_cases = [
            ('', BlockType.PARAGRAPH),
            ('just some text', BlockType.PARAGRAPH),
            ('just\nsome\nmulti\nline\ntext', BlockType.PARAGRAPH),
            ('#not a heading', BlockType.PARAGRAPH),
            ('# first level heading', BlockType.HEADING),
            ('## second level heading', BlockType.HEADING),
            ('### third level heading', BlockType.HEADING),
            ('#### fourth level heading', BlockType.HEADING),
            ('##### fifth level heading', BlockType.HEADING),
            ('###### sixth level heading', BlockType.HEADING),
            ('####### not a heading anymore', BlockType.PARAGRAPH),
            ('```single line code block```', BlockType.CODE),
            ('```\nmulti\n\rline\rcode\r\nblock\n```', BlockType.CODE),
            ('>not a proper quote', BlockType.PARAGRAPH),
            ('> single line quote', BlockType.QUOTE),
            ('> multi\n> line\n> quote', BlockType.QUOTE),
            ('> multi\r\n> line\r> quote', BlockType.QUOTE),
            ('> quote\n> block\n> with\n> a\n>problem\n> in the middle', BlockType.PARAGRAPH),
            (' > queue block with additional space', BlockType.PARAGRAPH),
            ('*not a list', BlockType.PARAGRAPH),
            ('* single item list', BlockType.UNORDERED_LIST),
            ('- single item list', BlockType.UNORDERED_LIST),
            ('* multi\n* item\n* list', BlockType.UNORDERED_LIST),
            ('- multi\n- item\n- list', BlockType.UNORDERED_LIST),
            ('- mixed\n* item\n* list', BlockType.UNORDERED_LIST),
            ('* list\n* with\n*problem', BlockType.PARAGRAPH),
            ('1.not a list', BlockType.PARAGRAPH),
            ('1. single item list', BlockType.ORDERED_LIST),
            ('1. multi\n2. item\n3. list', BlockType.ORDERED_LIST),
            ('006. any\n007. order\n1. list', BlockType.ORDERED_LIST),
        ]

        for test_case in test_cases:
            text = test_case[0]
            expected = test_case[1]

            self.assertEqual(block_to_block_type(text), expected)

    def test_block_to_text_block(self):
        test_cases = [
            ('',
             TextBlock(BlockType.PARAGRAPH, [])),
            ('just some text',
             TextBlock(BlockType.PARAGRAPH, [TextNode("just some text", TextType.NORMAL)])),
            ('just\nsome\nmulti\nline\ntext',
             TextBlock(BlockType.PARAGRAPH, [TextNode("just\nsome\nmulti\nline\ntext", TextType.NORMAL)])),
            ('# first level heading',
             TextBlock(BlockType.HEADING, [TextNode("first level heading", TextType.NORMAL)], 1)),
            ('## second level heading',
             TextBlock(BlockType.HEADING, [TextNode("second level heading", TextType.NORMAL)], 2)),
            ('### third level heading',
             TextBlock(BlockType.HEADING, [TextNode("third level heading", TextType.NORMAL)], 3)),
            ('#### fourth level heading',
             TextBlock(BlockType.HEADING, [TextNode("fourth level heading", TextType.NORMAL)], 4)),
            ('* single item list',
             TextBlock(BlockType.UNORDERED_LIST, [
                 [TextNode('single item list', TextType.NORMAL)]
             ])),
            ('- single item list',
             TextBlock(BlockType.UNORDERED_LIST, [
                 [TextNode('single item list', TextType.NORMAL)]
             ])),
            ('* multi\n* item\n* list',
             TextBlock(BlockType.UNORDERED_LIST, [
                 [TextNode('multi', TextType.NORMAL)],
                 [TextNode('item', TextType.NORMAL)],
                 [TextNode('list', TextType.NORMAL)],
             ])),
            ('- multi\n- item\n- list',
             TextBlock(BlockType.UNORDERED_LIST, [
                 [TextNode('multi', TextType.NORMAL)],
                 [TextNode('item', TextType.NORMAL)],
                 [TextNode('list', TextType.NORMAL)],
             ])),
            ('- mixed\n* item\n* list',
             TextBlock(BlockType.UNORDERED_LIST, [
                 [TextNode('mixed', TextType.NORMAL)],
                 [TextNode('item', TextType.NORMAL)],
                 [TextNode('list', TextType.NORMAL)],
             ])),
            ('1. single item list',
             TextBlock(BlockType.ORDERED_LIST, [
                 [TextNode('single item list', TextType.NORMAL)]
             ])),
            ('1. multi\n2. item\n3. list',
             TextBlock(BlockType.ORDERED_LIST, [
                 [TextNode('multi', TextType.NORMAL)],
                 [TextNode('item', TextType.NORMAL)],
                 [TextNode('list', TextType.NORMAL)],
             ])),
            ('006. any\n007. order\n1. list',
             TextBlock(BlockType.ORDERED_LIST, [
                 [TextNode('any', TextType.NORMAL)],
                 [TextNode('order', TextType.NORMAL)],
                 [TextNode('list', TextType.NORMAL)],
             ])),
        ]

        for test_case in test_cases:
            block = test_case[0]
            expected = test_case[1]

            res = block_to_text_block(block)

            self.assertEqual(res, expected)

    def test_text_block_to_html(self):
        test_cases = [
            (TextBlock(BlockType.PARAGRAPH, [
                TextNode("some text", TextType.NORMAL)
            ]), ParentNode('p', [LeafNode(tag='', value="some text")])),
            (TextBlock(BlockType.HEADING, [
                TextNode("some heading", TextType.NORMAL)
            ], 1), ParentNode('h1', [LeafNode(tag='', value="some heading")])),
            (TextBlock(BlockType.HEADING, [
                TextNode("some heading", TextType.NORMAL)
            ], 2), ParentNode('h2', [LeafNode(tag='', value="some heading")])),
            (TextBlock(BlockType.HEADING, [
                TextNode("some heading", TextType.NORMAL)
            ], 3), ParentNode('h3', [LeafNode(tag='', value="some heading")])),
            (TextBlock(BlockType.HEADING, [
                TextNode("some heading", TextType.NORMAL)
            ], 4), ParentNode('h4', [LeafNode(tag='', value="some heading")])),
            (TextBlock(BlockType.UNORDERED_LIST, [
                [TextNode('item 1', TextType.NORMAL)],
                [TextNode('item 2', TextType.NORMAL)]
            ]), ParentNode('ul', [
                ParentNode('li', [
                    LeafNode(tag='', value='item 1')
                ]),
                ParentNode('li', [
                    LeafNode(tag='', value='item 2')
                ])
            ])),
            (TextBlock(BlockType.ORDERED_LIST, [
                [TextNode('item 1', TextType.NORMAL)],
                [TextNode('item 2', TextType.NORMAL)]
            ]), ParentNode('ol', [
                ParentNode('li', [
                    LeafNode(tag='', value='item 1')
                ]),
                ParentNode('li', [
                    LeafNode(tag='', value='item 2')
                ])
            ])),
        ]

        for test_case in test_cases:
            text_block = test_case[0]
            expected = test_case[1]

            self.assertEqual(text_block.to_html_node(), expected)

    def test_markdown_to_html_nodes(self):
        test_cases = [
            (
                '',
                []
            ),
            (
                '\n\n\n',
                []
            ),
            (
                '# header1\n\n## header2',
                [
                    ParentNode('h1', [LeafNode(tag='', value="header1")]),
                    ParentNode('h2', [LeafNode(tag='', value="header2")]),
                ]
            )
        ]

        for test_case in test_cases:
            markdown_text = test_case[0]
            html_nodes = test_case[1]

            res = markdown_to_html_nodes(markdown_text)

            self.assertEqual(len(res), len(html_nodes))
            for actual, expected in zip(res, html_nodes):
                self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
