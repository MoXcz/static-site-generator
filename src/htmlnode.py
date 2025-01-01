class HTMLNode:
    # Props are HTML attributes
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("The method was not implemented")

    def props_to_html(self):
        prop_text = ""
        if self.props is None:
            return prop_text
        for key, value in self.props.items():
            prop_text += f' {key}="{value}"'

        return prop_text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Missing value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Parent node needs to have at least one children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"Parent Node({self.tag}, {self.children}, {self.props})"
