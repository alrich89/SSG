from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "Text (plain)"
    HEADING = "1-6 of # , followed by a space"
    CODE = "``` at the start, ending with ```"
    QUOTE = "> at the start"
    UNORDERED_LIST = "- , followed by a space"
    ORDERED_LIST = "1. any number, followed by a full stop"

def markdown_to_blocks(markdown):
    cleaned = []
    blocks = markdown.split("\n\n")
    for block in blocks:       
        if block.strip() != "":
            cleaned.append(block.strip())
    return cleaned

def block_to_block_type(block):
    lines = block.split("\n")
    quotes = 0
    ordered_list = 1
    unordered_list = 0
    for line in lines:
        if line.startswith(">"):
            quotes += 1
            if quotes == len(lines):
                return BlockType.QUOTE
        elif line.startswith("- "):
            unordered_list += 1
            if unordered_list == len(lines):
                return BlockType.UNORDERED_LIST
        elif line.startswith(f"{ordered_list}."):
            ordered_list += 1
            if ordered_list - 1 == len(lines):
                return BlockType.ORDERED_LIST         
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH