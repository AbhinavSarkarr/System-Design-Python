class HtmlElement:
    # Default indentation size for nested elements
    indent_size = 2

    def __init__(self, name="", text=""):
        self.name = name          # e.g., "ul", "li", "p"
        self.text = text          # text inside the element
        self.elements = []        # list of child elements

    # Internal method to recursively build string with indentation
    def __str(self, indent):
        lines = []
        i = ' ' * (indent * self.indent_size)  # indentation for current level
        lines.append(f'{i}<{self.name}>')      # opening tag

        # Add text if present
        if self.text:
            i1 = ' ' * ((indent + 1) * self.indent_size)
            lines.append(f'{i1}{self.text}')

        # Recursively add children
        for e in self.elements:
            lines.append(e.__str(indent + 1))

        lines.append(f'{i}</{self.name}>')     # closing tag
        return '\n'.join(lines)

    # Entry point to generate string (starts with indent = 0)
    def __str__(self):
        return self.__str(0)

    # Helper method to start a builder
    @staticmethod
    def create(name):
        return HtmlBuilder(name)


class HtmlBuilder:
    __root = HtmlElement()  # placeholder root element

    def __init__(self, root_name):
        self.root_name = root_name
        self.__root.name = root_name  # initialize root tag

    # Adds a child (not fluent, doesn't allow chaining)
    def add_child(self, child_name, child_text):
        self.__root.elements.append(
            HtmlElement(child_name, child_text)
        )

    # Adds a child (fluent, allows chaining)
    def add_child_fluent(self, child_name, child_text):
        self.__root.elements.append(
            HtmlElement(child_name, child_text)
        )
        return self  # return self to allow chaining

    # Reset the builder to start fresh
    def clear(self):
        self.__root = HtmlElement(name=self.root_name)

    # Return final HTML as string
    def __str__(self):
        return str(self.__root)


# ----------------------------------------
# Usage Examples
# ----------------------------------------

# Simple paragraph construction without a builder
hello = 'hello'
parts = ['<p>', hello, '</p>']
print(''.join(parts))

# Constructing an unordered list manually
words = ['hello', 'world']
parts = ['<ul>']
for w in words:
    parts.append(f'  <li>{w}</li>')
parts.append('</ul>')
print('\n'.join(parts))


# Using ordinary (non-fluent) builder
builder = HtmlElement.create('ul')
builder.add_child('li', 'hello')
builder.add_child('li', 'world')
print('Ordinary builder:')
print(builder)


# Using fluent builder (method chaining)
builder.clear()
builder.add_child_fluent('li', 'hello') \
       .add_child_fluent('li', 'world')
print('Fluent builder:')
print(builder)
