import re
from enum import Enum
from functools import reduce

from htmlnode import ParentNode
from markdown_converters.markdown_to_text_node import textnodes_from_markdown
from textnode import TextNode


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown_text):
    return list(
        filter(
            lambda block: block != '',
            map(
                lambda block: re.sub(r'^\s+|\s+$', '', block),
                markdown_text.split('\n\n')
            )
        )
    )

_block_type_identifiers = {
    # (regex, line by line)
    BlockType.HEADING: ('^#{1,6} ', False),
    BlockType.CODE: ('^```.*\r\n(?P<content>(?:.|\n|\r)*)```$', False),
    BlockType.QUOTE: ('^> ', True),
    BlockType.UNORDERED_LIST: ('^[*-] ', True),
    BlockType.ORDERED_LIST: ('^[0-9]+\\. ', True),
    BlockType.PARAGRAPH: ('.*', False)
}

def block_to_block_type(block):
    for block_type, identifier in _block_type_identifiers.items():
        if identifier[1]:
            if len(block) == 0:
                continue
            # Line by Line evaluation
            if reduce(lambda a,b: a and b, map(lambda line: re.match(identifier[0], line), block.splitlines())):
                return block_type
        else:
            # Whole block at once
            if re.match(identifier[0], block):
                return block_type
    return None

def block_to_text_block(block):
    block_type = block_to_block_type(block)
    identifier = _block_type_identifiers[block_type]
    children = []
    additional_info = None
    if len(block) > 0:
        if identifier[1]:
            # line by line
            for line in block.splitlines():
                match = re.match(identifier[0], line)
                line_without_prefix = line[match.end():]
                children.append(textnodes_from_markdown(line_without_prefix))
        elif block_type == BlockType.PARAGRAPH:
            children = textnodes_from_markdown(block)
        elif block_type == BlockType.HEADING:
            match = re.match(identifier[0], block)
            block_without_prefix = block[match.end():]
            children = textnodes_from_markdown(block_without_prefix)
            additional_info = match.end() - 1
        elif block_type == BlockType.CODE:
            match = re.match(identifier[0], block)
            code_content = match.group('content')
            children = textnodes_from_markdown(code_content)
        else:
            raise Exception(f'Unsupported block type: {block_type}')

    return TextBlock(block_type, children, additional_info)

def markdown_to_text_blocks(markdown_text):
    return list(map(block_to_text_block, markdown_to_blocks(markdown_text)))

def markdown_to_html_nodes(markdown_text):
    return ParentNode(tag='div', children=list(map(lambda block: block.to_html_node(), markdown_to_text_blocks(markdown_text))))

def extract_title(markdown_text):
    return list(filter(
        lambda tb: tb.block_type == BlockType.HEADING and tb.additional_info == 1,
        markdown_to_text_blocks(markdown_text)))[0].children[0].text

_block_type_to_html_tag = {
    BlockType.PARAGRAPH: 'p',
    BlockType.HEADING: 'h',
    BlockType.CODE: 'code',
    BlockType.QUOTE: ['blockquote', ''],
    BlockType.UNORDERED_LIST: ['ul', 'li'],
    BlockType.ORDERED_LIST: ['ol', 'li'],
}

def _children_as_html(children, tags):
    tag = None
    remaining_tags = []
    if len(tags) > 0:
        tag = tags[0]
        remaining_tags = tags[1:]

    as_html = []

    for child in children:
        if isinstance(child, TextNode):
            as_html.append(child.to_html_node())
        else:
            as_html.append(ParentNode(tag=tag, children=_children_as_html(child, remaining_tags)))

    return as_html

class TextBlock:
    def __init__(self, block_type, children, additional_info=None):
        self.block_type = block_type
        self.children = children
        self.additional_info = additional_info

    def __str__(self):
        return f'TextBlock({self.block_type}, {self.children}, {self.additional_info})'

    def __eq__(self, other):
        return self.block_type == other.block_type and self.children == other.children and self.additional_info == other.additional_info

    def to_html_node(self):
        if self.block_type not in _block_type_to_html_tag:
            raise Exception(f'Unknown block type: {self.block_type}')

        children_as_html = []
        tag = _block_type_to_html_tag[self.block_type]

        children = self.children
        if self.block_type == BlockType.QUOTE:
            children = [x for xs in children for x in xs]

        if _block_type_identifiers[self.block_type][1]:
            children_as_html = _children_as_html(children, tag[1:])
            tag = tag[0]
        else:
            children_as_html = list(map(lambda c: c.to_html_node(), children))

        if self.block_type == BlockType.HEADING:
            tag += str(self.additional_info)

        return ParentNode(tag, children_as_html)