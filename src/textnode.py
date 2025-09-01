from enum import Enum
import re

class TextType(Enum):
    TEXT = "Text (plain)" #no tag
    BOLD = "**Bold text**" #b tag
    ITALIC = "_Italic text_" #i tag
    CODE = "`Code text`" #code tag
    LINK = "[anchor text](url)" #a tag, anchor text, and "href" prop
    IMAGE = "![alt text](url)" #img tag, empty string value, "src" and "alt" props

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return isinstance(other, TextNode) and self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split = node.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("No closing delimiter found")
            for i, text in enumerate(split):
                if i % 2 != 0:
                    new_nodes.append(TextNode(text, text_type))
                else:
                    if text != "":
                        new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    links = []
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            running_split = node.text
            for extracted_image in extract_markdown_images(node.text):
                split_image = running_split.split(f"![{extracted_image[0]}]({extracted_image[1]})")
                if split_image[0] != "":
                    new_nodes.append(TextNode(split_image[0], TextType.TEXT))
                new_nodes.append(TextNode(f"{extracted_image[0]}", TextType.IMAGE, f"{extracted_image[1]}"))
                running_split = split_image[1]
            if running_split != "":
                new_nodes.append(TextNode(running_split, TextType.TEXT))
    return new_nodes
                             
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            running_split = node.text
            for extracted_link in extract_markdown_links(node.text):
                split_link = running_split.split(f"[{extracted_link[0]}]({extracted_link[1]})")
                if split_link[0] != "":
                    new_nodes.append(TextNode(split_link[0], TextType.TEXT))
                new_nodes.append(TextNode(f"{extracted_link[0]}", TextType.LINK, f"{extracted_link[1]}"))
                running_split = split_link[1]
            if running_split != "":
                new_nodes.append(TextNode(running_split, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    new_nodes = list(split_nodes_image(split_nodes_link(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE))))
    return new_nodes