import unittest

from block import markdown_to_blocks, BlockType, block_to_block_type

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks,[
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ])

    def test_markdown_to_blocks2(self):
        markdown2 = """
# This is a heading followed by 3 blank lines



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks2 = markdown_to_blocks(markdown2)
        self.assertEqual(blocks2,[
            "# This is a heading followed by 3 blank lines",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ])

    def test_block_to_block_type(self):
        block3 = """``` This is a code block 
with multiple lines
of code
```"""
        block4 = block_to_block_type(block3)
        self.assertEqual(block4, BlockType.CODE)

    def test_block_to_block_type2(self):
        block5 = """>this is quote line
>another quote line
>a third quote line"""
        block6 = block_to_block_type(block5)
        self.assertEqual(block6, BlockType.QUOTE)

    def test_block_to_block_type3(self):
        block5 = """>this is quote line
>another quote line
a third line but NOT a quote"""
        block6 = block_to_block_type(block5)
        self.assertEqual(block6, BlockType.PARAGRAPH)

    def test_block_to_block_type4(self):
        block7 = """### this is Heading line"""
        block8 = block_to_block_type(block7)
        self.assertEqual(block8, BlockType.HEADING)

    def test_block_to_block_type5(self):
        block9 = """####### this is Heading line with 1 too many '#' characters"""
        block10 = block_to_block_type(block9)
        self.assertEqual(block10, BlockType.PARAGRAPH)
    
    def test_block_to_block_type6(self):
        block11 = """1. this is an ordered list
2. with more entries
3. and more entries"""
        block12 = block_to_block_type(block11)
        self.assertEqual(block12, BlockType.ORDERED_LIST)    

if __name__ == "__main__":
    unittest.main()