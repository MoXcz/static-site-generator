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
        for key, value in self.props.items():
            prop_text += f' {key}="{value}"'

        return prop_text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"