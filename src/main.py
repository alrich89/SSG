from htmlnode import extract_title, markdown_to_html_node

import os
import shutil


PUBLIC_FOLDER = "public"
STATIC_FOLDER = "static"


def generate_page(from_path, template_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(os.path.abspath(from_path), mode='r') as f:
        markdown_file = f.read()
    html_node = markdown_to_html_node(markdown_file)
    title = extract_title(markdown_file)
    with open(os.path.abspath(template_path), mode='r') as f1:
        template_file = f1.read()
    page_html = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())
    with open(os.path.abspath(dest_path), mode='w') as f2:
        f2.write(page_html)

def generate_pages_recursive(current_dir, dir_path_content, template_path, des_dir_path):
    #use the generate_page function while recursively stepping through the folders from content.
    content_path  = os.path.abspath(dir_path_content)
    if current_dir == None:
        current_path = content_path
    else:
        current_path = os.path.abspath(current_dir)
    current_level_entries = os.listdir(current_path)
    public_path = os.path.abspath(des_dir_path)
    relative_path = os.path.relpath(current_path, content_path)
    destination_path = os.path.join(public_path, relative_path)
    os.makedirs(destination_path, exist_ok=True)
    for entry in current_level_entries:
        if os.path.isfile(os.path.join(current_path, entry)) and os.path.splitext(entry)[1] == ".md":
            generate_page(os.path.join(current_path, entry), template_path, os.path.join(destination_path,  os.path.splitext(entry)[0] + ".html"))
        elif os.path.isdir(os.path.join(current_path, entry)):
            generate_pages_recursive(os.path.join(current_path, entry), dir_path_content, template_path, des_dir_path)
    return

def static_to_public():
    #delete all of the contents of public.
    def clear_folder(folder):
        folder_path = os.path.abspath(folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)

       
    #copy all of the files from one directory to another while maintaining the structure.
    def copy_files(current_level):
        current_path  = os.path.abspath(current_level)
        current_level_entries = os.listdir(current_path)
        relative_path = os.path.relpath(current_path, os.path.abspath(STATIC_FOLDER))
        destination_path = os.path.join(os.path.abspath(PUBLIC_FOLDER), relative_path)
        os.makedirs(destination_path, exist_ok=True)
        for entry in current_level_entries:       
            if os.path.isfile(os.path.join(current_path, entry)):
                shutil.copyfile(os.path.join(current_path, entry), os.path.join(destination_path, entry))
            elif os.path.isdir(os.path.join(current_path, entry)):            
                copy_files(os.path.join(current_path, entry))
        return

    clear_folder(PUBLIC_FOLDER)
    copy_files(STATIC_FOLDER)


def main():
    static_to_public()
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(None, "content", "template.html", PUBLIC_FOLDER)

if __name__ == "__main__":
    main()