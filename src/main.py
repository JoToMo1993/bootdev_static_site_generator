import os
import shutil
import sys

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as markdown_file:
        markdown = markdown_file.read()
        with open(template_path, 'r') as template_path:
            html_node = markdown_to_html_nodes(markdown)
            html = html_node.to_html()
            title = extract_title(markdown)

            content = template_path.read().replace('{{ Title }}', title)
            content = content.replace('{{ Content }}', html)
            content = content.replace('href="/', 'href="' + basepath)
            content = content.replace('src="/', 'src="' + basepath)

            with open(dest_path, 'w') as output_file:
                output_file.write(content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    for entry in os.listdir(dir_path_content):
        print(entry)
        if os.path.isfile(dir_path_content + entry):
            generate_page(dir_path_content + entry, template_path, dest_dir_path + entry.replace('.md', '.html'), basepath)
        elif os.path.isdir(dir_path_content + entry):
            generate_pages_recursive(dir_path_content + entry + '/', template_path, dest_dir_path + entry + '/', basepath)

def main():
    text_node = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
    print(text_node)
    destDir = 'docs'

    if os.path.exists(destDir):
        shutil.rmtree(destDir)

    if not os.path.exists('static'):
        raise Exception('static folder not found')

    args = sys.argv
    basepath = '/'
    if len(args) > 1:
        basepath = args[1]

    copy('static/', destDir + '/')

    generate_pages_recursive('content/', 'template.html', destDir + '/', basepath)

main()