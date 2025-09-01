import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node, extract_title
from textnode import TextNode, TextType


childnode = HTMLNode("a", "This is a test child HTML node, without props", None, None)
childnode2 = HTMLNode("p", "This is a test child HTML node, without props", None, None)

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "This is an HTML node, without children", None, {"href": "https://www.testurl.com"})
        node2 = HTMLNode("a", "This is an HTML node, without children", None, {"href": "https://www.testurl.com"})
        self.assertEqual(node, node2)

    def test_tag_not_eq(self):
        node3 = HTMLNode("a", "This is an HTML node, without children", None, {"href": "https://www.testurl.com"})
        node4 = HTMLNode("p", "This is an HTML node, without children", None, {"href": "https://www.testurl.com"})
        self.assertNotEqual(node3, node4)
    
    def test_value_not_eq(self):
        node5 = HTMLNode("a", "This is an HTML node, without children", None, {"href": "https://www.testurl.com"})
        node6 = HTMLNode("a", "This is a different value HTML node, without children", None, {"href": "https://www.testurl.com"})
        self.assertNotEqual(node5, node6)

    def test_children_not_eq(self):
        node7 = HTMLNode("a", "This is an HTML node, with children", [childnode], {"href": "https://www.testurl.com"})
        node8 = HTMLNode("a", "This is an HTML node, with children", [childnode2], {"href": "https://www.testurl.com"})
        self.assertNotEqual(node7, node8)

    def test_props_not_eq(self):
        node9 = HTMLNode("a", "This is an HTML node, with children", [childnode], {"href": "https://www.testurl.com"})
        node10 = HTMLNode("a", "This is an HTML node, with children", [childnode], {"target": "_blank"})
        self.assertNotEqual(node9, node10)
    
    def test_no_tags(self):
        node11 = HTMLNode(None, "This is an HTML node, without a tag", [childnode], {"href": "https://www.testurl.com"})
        self.assertIs(node11.tag, None)

    def test_no_value(self):
        node12 = HTMLNode("a", None, [childnode], {"href": "https://www.testurl.com"})
        self.assertIs(node12.value, None)

    def test_no_children(self):
        node13 = HTMLNode("a", "This is an HTML node, without a tag", None, {"href": "https://www.testurl.com"})
        self.assertIs(node13.children, None)

    def test_no_props(self):
        node14 = HTMLNode("a", "This is an HTML node, without a tag", [childnode], None)
        self.assertIs(node14.props, None)
    
    def test_props_to_html(self):
        node15 = HTMLNode("a", "This is an HTML node, without a tag", [childnode], {"href": "https://www.testurl.com", "target": "_blank"})
        self.assertEqual(node15.props_to_html(), ' href="https://www.testurl.com" target="_blank"')

    def test_LeafNode_to_html(self):
        node16 = LeafNode("a", "This is an Leaf node, with a tag", {"href": "https://www.testurl.com"})
        self.assertEqual(node16.to_html(), '<a href="https://www.testurl.com">This is an Leaf node, with a tag</a>')

    def test_LeafNode_to_html_without_tag(self):
        node17 = LeafNode(None, "This is an Leaf node, without a tag")
        self.assertEqual(node17.to_html(), 'This is an Leaf node, without a tag')

    def test_parent_to_html_with_children(self):
        node18 = LeafNode("b", "This is a child leaf node, with a tag", {"target": "_blank"})
        node19 = ParentNode("a", [node18], {"href": "https://www.testurl.com"})
        self.assertEqual(node19.to_html(), '<a href="https://www.testurl.com"><b target="_blank">This is a child leaf node, with a tag</b></a>')

    def test_parent_to_html_with_grandchildren(self):
        node20 = LeafNode("b", "This is a grandchild leaf node, with a tag", {"target": "_blank"})
        node21 = ParentNode("p", [node20])
        node22 = ParentNode("a", [node21], {"href": "https://www.testurl.com"})
        self.assertEqual(node22.to_html(), '<a href="https://www.testurl.com"><p><b target="_blank">This is a grandchild leaf node, with a tag</b></p></a>')

    def test_parent_to_html_empty_children(self):
        node23 = ParentNode("div", [])
        self.assertEqual(node23.to_html(), '<div></div>')

    def test_parent_missing_children(self):
        node24 = ParentNode("a", None)
        with self.assertRaises(ValueError) as message:
            node24.to_html()
        self.assertEqual(str(message.exception), "Child node is missing")

    def test_LeafNode_missing_value(self):
        node25 = LeafNode("a", None)
        with self.assertRaises(ValueError) as message:
            node25.to_html()
        self.assertEqual(str(message.exception), "Node has no value")

    def test_parent_to_html_empty_props(self):
        node26 = LeafNode("b", "This is a child leaf node, with a tag", {})
        node27 = ParentNode("div", [node26])
        self.assertEqual(node27.to_html(), '<div><b>This is a child leaf node, with a tag</b></div>')

    def test_parent_to_html_with_3_children(self):
        node28 = LeafNode("a", "This is the first child leaf node, with a tag and props", {"target": "_blank", "href": "https://www.testurl.com"})
        node29 = LeafNode("b", "This is the second child leaf node, with a tag and empty props", {})
        node30 = LeafNode("p", "This is the third child leaf node, with a tag and missing props", None)
        node31 = ParentNode("div", [node28, node29, node30], {"href": "https://www.testurl.com"})
        self.assertEqual(node31.to_html(), '<div href="https://www.testurl.com"><a target="_blank" href="https://www.testurl.com">This is the first child leaf node, with a tag and props</a><b>This is the second child leaf node, with a tag and empty props</b><p>This is the third child leaf node, with a tag and missing props</p></div>')

    def test_text_to_leaf_node(self):
        node32 = TextNode("This is a text node in bold", TextType.BOLD)
        node33 = text_node_to_html_node(node32)
        self.assertEqual(node33.tag, "b")
        self.assertEqual(node33.value, "This is a text node in bold")

    def test_text_to_leaf_node2(self):
        node34 = TextNode("This is an image", TextType.IMAGE, "https://www.testimage.com")
        node35 = text_node_to_html_node(node34)
        self.assertEqual(node35.tag, "img")
        self.assertEqual(node35.value, "")
        self.assertEqual(node35.props, {"src": "https://www.testimage.com", "alt": "This is an image"})

    def test_text_to_leaf_node3(self):
        node36 = TextNode("This is an link", TextType.LINK, "https://www.testimage.com")
        node37 = text_node_to_html_node(node36)
        self.assertEqual(node37.tag, "a")
        self.assertEqual(node37.value, "This is an link")
        self.assertEqual(node37.props, {"href": "https://www.testimage.com"})

    def test_markdown_to_html(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node38 = markdown_to_html_node(md)
        html39 = node38.to_html()
        self.assertEqual(
            html39,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_codeblock_to_html(self):
        md2 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node40 = markdown_to_html_node(md2)
        html41 = node40.to_html()
        self.assertEqual(
            html41,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_quoteblock_to_html(self):
        md3 = """
>This is a
>quote block,
>Where each line
>starts with a > character.
"""

        node42 = markdown_to_html_node(md3)
        html43 = node42.to_html()
        self.assertEqual(
            html43,
            "<div><blockquote>This is a\nquote block,\nWhere each line\nstarts with a > character.</blockquote></div>",
        )

    def test_markdown_headings_to_html(self):
        md4 = """
# This is a heading 1

## This is a heading 2

### This is a heading 3

#### This is a heading 4

##### This is a heading 5

###### This is a heading 6
"""

        node44 = markdown_to_html_node(md4)
        html45 = node44.to_html()
        self.assertEqual(
            html45,
            "<div><h1>This is a heading 1</h1><h2>This is a heading 2</h2><h3>This is a heading 3</h3><h4>This is a heading 4</h4><h5>This is a heading 5</h5><h6>This is a heading 6</h6></div>",
        )

    def test_markdown_unordered_list_to_html(self):
        md5 = """
- This is an unordered list
- with multiple entries
- each line starting
- with a - followed by a space
"""

        node46 = markdown_to_html_node(md5)
        html47 = node46.to_html()
        self.assertEqual(
            html47,
            "<div><ul><li>This is an unordered list</li><li>with multiple entries</li><li>each line starting</li><li>with a - followed by a space</li></ul></div>",
        )

    def test_markdown_ordered_list_to_html(self):
        md6 = """
1. This is an ordered list
2. with multiple entries
3. each line starting
4. with a digit followed by a full stop
"""

        node48 = markdown_to_html_node(md6)
        html49 = node48.to_html()
        self.assertEqual(
            html49,
            "<div><ol><li>This is an ordered list</li><li>with multiple entries</li><li>each line starting</li><li>with a digit followed by a full stop</li></ol></div>",
        )

    def test_extract_title(self):
        md7 = """
# Title Heading

## This is a heading 2

### This is a heading 3

1. This is an ordered list
2. with multiple entries
3. each line starting
4. with a digit followed by a full stop

- This is an unordered list
- with multiple entries
- each line starting
- with a - followed by a space

Here is a plain paragraph of text.
This test should pass and extract the 'h1' heading.
"""

        node50 = extract_title(md7)
        self.assertEqual(
            node50,
            "Title Heading",
        )

    def test_extract_title2(self):
        md8 = """
## This is a heading 2

### This is a heading 3

1. This is an ordered list
2. with multiple entries
3. each line starting
4. with a digit followed by a full stop

- This is an unordered list
- with multiple entries
- each line starting
- with a - followed by a space

Here is a plain paragraph of text.
This test should fail to extract as there is no 'h1' heading.
"""

        with self.assertRaises(Exception) as message:
            extract_title(md8)
        self.assertEqual(str(message.exception), "No title found in markdown")

if __name__ == "__main__":
    unittest.main()