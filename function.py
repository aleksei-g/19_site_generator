import markdown
import os
import json


def markdown_to_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text_file = f.read()
    html = markdown.markdown(text_file, extensions=['codehilite'])
    return html


def save_html_to_file(html, filepath):
    if os.path.dirname(filepath):
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(html)


def check_file_to_read(filepath):
    if os.access(filepath, os.F_OK):
        if os.access(filepath, os.R_OK):
            return True
    return False


def check_dir_to_write(path):
    if os.access(path, os.F_OK):
        if os.access(path, os.W_OK):
            return True
    return False


def read_json_file(filepath):
    with open(filepath, 'r', encoding='utf_8') as f:
        return json.load(f)
