class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ''
        return ''.join(list(map(lambda item: f' {item[0]}="{item[1]}"', self.props.items())))

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError('value cannot be None')
        if self.tag is None or self.tag == '':
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == '':
            raise ValueError('tag cannot be None or empty')
        if self.children is None or len(self.children) == 0:
            raise ValueError('children cannot be None or empty')
        return f'<{self.tag}{self.props_to_html()}>{''.join(list(map(lambda child: child.to_html(), self.children)))}</{self.tag}>'

    def __repr__(self):
        return f'ParentNode({self.tag}, {self.children}, {self.props})'

    def __eq__(self, other):
        return self.tag == other.tag and self.children == other.children and self.props == other.props