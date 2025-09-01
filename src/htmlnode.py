from textnode import TextNode, TextType, text_to_textnodes
from block import BlockType, block_to_block_type, markdown_to_blocks


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        all_props = ""
        if self.props is not None:
            for item, value in self.props.items():
                all_props += f' {item}="{value}"'
        return all_props
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        

    def to_html(self):
        if self.value == None:
            raise ValueError("Node has no value")
        elif self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is missing")
        if self.children == None:
            raise ValueError("Child node is missing")
        html_children_string = ""
        for child in self.children:
            html_children_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_children_string}</{self.tag}>"


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("Invalid text type")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    title_found = False
    title = ""
    for block in markdown_blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block.startswith("# "):
                title_found = True
                title = block.lstrip("# ")
    if not title_found:
        raise Exception("No title found in markdown")
    return title


def markdown_to_html_node(markdown):
    def get_html_tag(block):
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                return "p"
            case BlockType.CODE:
                return "pre"
            case BlockType.QUOTE:
                return "blockquote"
            case BlockType.UNORDERED_LIST:
                return "ul"
            case BlockType.ORDERED_LIST:
                return "ol"
            case BlockType.HEADING:
                for i in range(0, 7):
                    if block[i] == " ":
                        break
                return f"h{i}" #h1-h6

    def text_to_children(text):
        html_nodes_list = []
        text_nodes = text_to_textnodes(text)
        for node in text_nodes:
            html_nodes_list.append(text_node_to_html_node(node))
        return html_nodes_list

    def get_children_nodes(block): #Do not use on code block.
        new_lines_removed = block.replace("\n", " ")
        children_nodes = text_to_children(new_lines_removed)
        return children_nodes
    
    def get_block_html_node(block):
        if get_html_tag(block) == "pre":
            split_new_lines = block.split("\n")
            return_content = "\n".join(split_new_lines[1:-1]) + "\n"
            block_into_textnode = TextNode(text=return_content, text_type=TextType.CODE, url=None)
            code_htmlnode = text_node_to_html_node(block_into_textnode)
            return ParentNode(tag=get_html_tag(block), children=[code_htmlnode] ,props=None)
        elif get_html_tag(block) == "blockquote":
            split_new_lines = block.split("\n")
            cleaned_list = []
            for line in split_new_lines:
                cleaned_list.append(line.lstrip("> "))
            result = "\n".join(cleaned_list)
            return ParentNode(tag=get_html_tag(block), children=text_to_children(result), props=None)
        elif get_html_tag(block).startswith("h"):
            # Remove all # characters and spaces from the beginning
            heading_text = block.lstrip("# ")
            return ParentNode(tag=get_html_tag(block), children=text_to_children(heading_text), props=None)
        elif get_html_tag(block) == "ul":
            split_new_lines = block.split("\n")
            list_items = []
            for line in split_new_lines:
                # Clean the line and create an <li> node for each item
                item_text = line.lstrip("- ")
                li_node = ParentNode(tag="li", children=text_to_children(item_text), props=None)
                list_items.append(li_node)
            return ParentNode(tag="ul", children=list_items, props=None)
        elif get_html_tag(block) == "ol":
            split_new_lines = block.split("\n")
            list_items = []
            for line in split_new_lines:
                # Clean the line and create an <li> node for each item
                item_text = line.lstrip("0123456789. ")
                li_node = ParentNode(tag="li", children=text_to_children(item_text), props=None)
                list_items.append(li_node)
            return ParentNode(tag="ol", children=list_items, props=None)
        return ParentNode(tag=get_html_tag(block), children=get_children_nodes(block), props=None)
   
    def get_blocks_html(markdown):
        markdown_blocks = markdown_to_blocks(markdown)
        html_nodes = []
        for block in markdown_blocks:  
            html_nodes.append(get_block_html_node(block))
        return html_nodes

    return ParentNode(tag="div", children=get_blocks_html(markdown), props=None)
