from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINKS = 'links'
    IMAGES = 'images'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def to_html_node(self):
        text_type_to_html_tag = {
            TextType.NORMAL: '',
            TextType.BOLD: 'b',
            TextType.ITALIC: 'i',
            TextType.CODE: 'code',
            TextType.LINKS: 'a',
            TextType.IMAGES: 'img',
        }

        text = self.text
        props = None
        if self.text_type == TextType.LINKS:
            props = {'href': self.url}
        elif self.text_type == TextType.IMAGES:
            props = {'src': self.url, 'alt': self.text}
            text = ''

        if self.text_type not in text_type_to_html_tag:
            raise Exception(f'text_type {self.text_type} is not supported')
        return LeafNode(text_type_to_html_tag[self.text_type], text, props)