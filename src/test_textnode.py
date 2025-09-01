import unittest
from textnode import TextNode, TextType,  split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

    def test_no_url(self):
        node5 = TextNode("This text node should have no url", TextType.BOLD) #"https://www.testurl.com"
        self.assertIs(node5.url, None)
    
    def test_url_not_eq(self):
        node6 = TextNode("This text node should have a url", TextType.BOLD, "https://www.testurl.com")
        node7 = TextNode("This text node should have a url", TextType.BOLD, "https://www.differenttesturl.com")
        self.assertNotEqual(node6, node7)

    def test_split_nodes(self):
        node38 = [TextNode("This is text with a `code block` in the middle", TextType.TEXT)]
        node39 = split_nodes_delimiter(node38, "`", TextType.CODE)
        self.assertEqual(node39, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT)
        ])

    def test_split_nodes2(self):
        node40 = [
            TextNode("This is text with **bolded text** in the middle", TextType.TEXT),
            TextNode("This is a second text with **bolded text** in the middle", TextType.TEXT),
        ]
        node41 = split_nodes_delimiter(node40, "**", TextType.BOLD)
        self.assertEqual(node41, [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bolded text", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            TextNode("This is a second text with ", TextType.TEXT),
            TextNode("bolded text", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT)
        ])

    def test_split_nodes3(self):
        node42 = [TextNode("This is broken text with **bolded text in the middle", TextType.TEXT)]
        with self.assertRaises(Exception) as message:
            split_nodes_delimiter(node42, "**", TextType.BOLD)
        self.assertEqual(str(message.exception), "No closing delimiter found")

    def test_split_nodes4(self):
        node44 = [TextNode("_italic text_ starts this text", TextType.TEXT)]
        node45 = split_nodes_delimiter(node44, "_", TextType.ITALIC)
        self.assertEqual(node45, [
            TextNode("italic text", TextType.ITALIC),
            TextNode(" starts this text", TextType.TEXT)
        ])

    def test_split_nodes5(self):
        node46 = [TextNode("multiple `code` blocks are in this `text`", TextType.TEXT)]
        node47 = split_nodes_delimiter(node46, "`", TextType.CODE)
        self.assertEqual(node47, [
            TextNode("multiple ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" blocks are in this ", TextType.TEXT),
            TextNode("text", TextType.CODE)
        ])
    
    def test_extract_images(self):
        text48 = "This is text with an ![image](https://i.imgur.com/testimage.png)"
        text49 = extract_markdown_images(text48)
        self.assertListEqual([("image", "https://i.imgur.com/testimage.png")], text49)

    def test_extract_images2(self):
        text50 = "This is text with an ![image](https://i.imgur.com/testimage.png) with another ![different image](https://i.imgur.com/differenttestimage.png)"
        text51 = extract_markdown_images(text50)
        self.assertListEqual([("image", "https://i.imgur.com/testimage.png"), ("different image","https://i.imgur.com/differenttestimage.png")], text51)

    def test_extract_links(self):
        text52 = "This is text with an [link](https://www.testlink.com)"
        text53 = extract_markdown_links(text52)
        self.assertListEqual([("link", "https://www.testlink.com")], text53)

    def test_split_nodes_image(self):
        node_list54 = [
            TextNode("This is text with an ![image](https://i.imgur.com/testimage.png) and ![second image](https://i.imgur.com/testimage2.png)", TextType.TEXT),
            TextNode("This is more text with another ![image](https://i.imgur.com/testimage3.png) and a ![fourth image](https://i.imgur.com/testimage4.png) with more text", TextType.TEXT)
        ]
        node55 = split_nodes_image(node_list54)
        self.assertListEqual = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/testimage.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/testimage2.png"),
            TextNode("This is more text with another ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/testimage3.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("fourth image", TextType.IMAGE, "https://i.imgur.com/testimage4.png"),
            TextNode(" with more text", TextType.TEXT)
        ]

    def test_split_nodes_link(self):
        node_list56 = [
            TextNode("[a link](https://www.testlink.com) starts this text string followed by a [second link](https://www.testlink2.com) with follw-up text", TextType.TEXT),
            TextNode("This is more text with another [link](https://www.testlink3.com) and a [fourth link](https://www.testlink4.com)", TextType.TEXT)
        ]
        node57 = split_nodes_link(node_list56)
        self.assertListEqual = [
            TextNode("a link", TextType.LINK, "https://www.testlink.com"),
            TextNode(" starts this text string followed by a ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://www.testlink2.com"),
            TextNode("This is more text with another ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.testlink3.com"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("fourth link", TextType.LINK, "https://www.testlink4.com"),
        ]

    def test_text_to_textnodes(self):
        text58 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node59 = text_to_textnodes(text58)
        self.assertEqual(node59, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])


if __name__ == "__main__":
    unittest.main()