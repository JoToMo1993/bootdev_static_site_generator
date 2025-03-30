from textnode import TextType, TextNode
import re
from functools import reduce


def extract_markdown_images(text):
    return _extract_markdown_with_url(text, TextType.IMAGES)

def extract_markdown_links(text):
    return _extract_markdown_with_url(text, TextType.LINKS)

def _extract_markdown_with_url(text, text_type):
    return list(
        map(
            lambda node: (node.text, node.url),
            filter(
                lambda node: node.text_type == text_type,
                textnodes_from_markdown(text)
            )
        )
    )

def textnodes_from_markdown(text):
    text_type_to_delimiters = {
        TextType.CODE: '`',
        TextType.BOLD: '\\*\\*',
        TextType.ITALIC: '\\_',
        TextType.IMAGES: '![',
        TextType.LINKS: '[',
    }
    node = TextNode(text, TextType.NORMAL)
    nodes = [node]
    for text_type, delimiter in text_type_to_delimiters.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def regex_extractor():
        def extractor(node):
            split_text = re.split(delimiter, node.text)
            if len(split_text) <= 1:
                return [node]
            nodes = []
            for i in range(0, len(split_text)):
                if split_text[i] == '':
                    continue
                if i % 2 == 0:
                    nodes.append(TextNode(split_text[i], TextType.NORMAL))
                else:
                    nodes.append(TextNode(split_text[i], text_type))
            return nodes
        return extractor

    def url_based_extractor(node, pattern, inner_text_type, func):
        match = re.search(pattern, node.text)
        if match:
            text = match.group('text')
            url = match.group('url')

            pre_text = node.text[:match.start()]
            pre_text_nodes = []
            if pre_text != '':
                pre_text_nodes.append(TextNode(pre_text, TextType.NORMAL))
            link_node = TextNode(text, inner_text_type, url)
            post_text = node.text[match.end():]
            post_text_nodes = []
            if post_text != '':
                post_text_nodes = func(TextNode(post_text, TextType.NORMAL))
            return pre_text_nodes + [link_node] + post_text_nodes
        else:
            return [node]

    def link_extractor(node):
        return url_based_extractor(node, r"\[(?P<text>.*?)]\((?P<url>[^) ]*)\)", TextType.LINKS, link_extractor)

    def image_extractor(node):
        return url_based_extractor(node, r"!\[(?P<text>.*?)]\((?P<url>[^) ]*)(?: \"(?P<title>.*)\")?\)", TextType.IMAGES, image_extractor)

    extractor = {
        TextType.BOLD: regex_extractor(),
        TextType.ITALIC: regex_extractor(),
        TextType.CODE: regex_extractor(),
        TextType.LINKS: link_extractor,
        TextType.IMAGES: image_extractor,
    }

    def split(node):
        if node.text_type != TextType.NORMAL:
            return [node]
        return extractor[text_type](node)

    return reduce(lambda x,y: x+y, map(split, old_nodes), [])
