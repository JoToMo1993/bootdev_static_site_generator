import os
import shutil

from markdown_converters.markdown_to_blocks import markdown_to_html_nodes, extract_title
from textnode import TextNode, TextType

def copy(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)

    for entry in os.listdir(src):
        print(entry)
        if os.path.isfile(src + entry):
            print('is file')
            shutil.copyfile(src + entry, dest + entry)
        elif os.path.isdir(src + entry):
            print('is directory')
            copy(src + entry + '/', dest + entry + '/')

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as markdown_file:
        markdown = markdown_file.read()
        with open(template_path, 'r') as template_path:
            html_node = markdown_to_html_nodes(markdown)
            html = html_node.to_html()
            title = extract_title(markdown)

            content = template_path.read().replace('{{ Title }}', title)
            content = content.replace('{{ Content }}', html)

            with open(dest_path, 'w') as output_file:
                output_file.write(content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    for entry in os.listdir(dir_path_content):
        print(entry)
        if os.path.isfile(dir_path_content + entry):
            generate_page(dir_path_content + entry, template_path, dest_dir_path + entry.replace('.md', '.html'))
        elif os.path.isdir(dir_path_content + entry):
            generate_pages_recursive(dir_path_content + entry + '/', template_path, dest_dir_path + entry + '/')

def main():
    text_node = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
    print(text_node)

    if os.path.exists('public'):
        shutil.rmtree('public')

    if not os.path.exists('static'):
        raise Exception('static folder not found')

    copy('static/', 'public/')

    generate_pages_recursive('content/', 'template.html', 'public/')

main()