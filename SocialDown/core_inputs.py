import json
import os.path
from os.path import isfile, abspath, isdir
from os import mkdir


def create_dir(name):
    folder = abspath(name)
    if not isdir(folder):
        mkdir(folder)
    return folder


def create_sub_dir(name, sub):
    folder = abspath(name)
    if not isdir(folder):
        mkdir(folder)
    folder = os.path.join(folder, sub)
    if not isdir(folder):
        mkdir(folder)
    return folder


def clean_string(text):
    return " ".join(text.split()).strip()


def load_json(file_path):
    if not isfile(file_path):
        save_json({}, file_path)
    with open(file_path, 'r', encoding="utf8") as dic_file:
        return json.load(dic_file)


def save_json(obj, file_path):
    with open(file_path, 'w', encoding="utf8") as dic_file:
        json.dump(obj, dic_file, indent=2, ensure_ascii=False)


def load_lines(file_path):
    with open(file_path, 'r', encoding="utf8") as url_file:
        lines = url_file.readlines()
        urls = set()
        for line in lines:
            clean = line.strip()
            if len(clean) < 3:
                continue
            urls.add(clean)
        return sorted(urls)
