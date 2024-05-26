#!/usr/bin/env python3

# Lartu's WebSCFL Builder
# 18Y24
# WebSCFL stands for Web Sectioned Command First Language
# Version 1.5

import os
import shutil
from datetime import datetime


INCLUDE_DIR = "include"
SOURCE_DIR = "source"
IMAGES_DIR = "images"
RESULT_DIR = "docs"
OTHER_DIR  = "other"
RESULT_IMAGES_DIR = f"images"
FILE_EXTENSION = ".scfl"


def create_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copy_file_relative(src_relative_path, dest_relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, src_relative_path)
    dest_path = os.path.join(script_dir, dest_relative_path)
    print(f"Copied {src_path} to {dest_path}.")
    shutil.copy(src_path, dest_path)


def copy_dir_relative(src_relative_path, dest_relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, src_relative_path)
    dest_path = os.path.join(script_dir, dest_relative_path)
    print(f"Copied {src_path} to {dest_path}.")
    shutil.copytree(src_path, dest_path)


def list_files_in_folder(relative_folder_path):
    print(f"Looking for {FILE_EXTENSION} files in {relative_folder_path}.")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, relative_folder_path)
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            relative_file_path = os.path.relpath(os.path.join(root, file), script_dir)
            file_list.append(relative_file_path)
    return file_list


def replace_extension(file_path, new_extension):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name + new_extension
    return new_file_path


def webpage_compiled_message():
    current_time = datetime.now().strftime("%Y-%m-%d, %H:%M")
    return f"Webpage compiled on {current_time} using [[https://github.com/Lartu/WebSCFL/ WebSCFL]]."


def error(message: str):
    print(f"Error: {message}")
    exit(1)


def compile_file(filename: str):
    UNDEFINED = -1
    HEAD = 0
    BODY = 1

    if not FILE_EXTENSION in filename:
        print(f"Ignoring file {filename}.")
        return

    def add_line_to_file(line: str):
        nonlocal result_file_contents
        # Replace wikimedia-like links
        while "[[" in line:
            index = line.index("[[")
            if "]]" not in line:
                error(f"[[ without ]] found in line {line}.")
            else:
                endindex = line.index("]]")
            rawlink = line[index:endindex+2]
            if "||" not in rawlink:
                tokens = rawlink[2:-2].split(sep=None, maxsplit=1)
                linkdest = tokens[0].strip()
                linktext = tokens[1].strip()
            else:
                tokens = rawlink[2:-2].split(sep="||", maxsplit=1)
                linkdest = tokens[1].strip()
                linktext = tokens[0].strip()
            target = ""
            external = ""
            if "http://" in linkdest or "https://" in linkdest:
                target = "target=_blank"
                external = f"<img src='{RESULT_IMAGES_DIR}/external-link.png'>"
            link = f"<a class='link' href='{linkdest}' {target}>{linktext}{external}</a>"
            line = line.replace(rawlink, link)
        # Replace tooltips
        while "[(" in line:   # DOCUMENTAR
            index = line.index("[(")
            if ")]" not in line:
                error(f"[( without )] found in line {line}.")
            else:
                endindex = line.index(")]")
            rawtooltip = line[index:endindex+2]
            if "||" not in rawtooltip:
                error(f"[( ... )] tooltip without || found in line {line}.")
            else:
                tokens = rawtooltip[2:-2].split(sep="||", maxsplit=1)
                text = tokens[0].strip()
                info = tokens[1].strip()
            tooltip = f"<span class='tooltip' title='{info}'>{text}</span>"
            line = line.replace(rawtooltip, tooltip)
        # Replacements
        line = line.replace("&[;", "[")  # DOCUMENTAR
        line = line.replace("&];", "]")  # DOCUMENTAR
        line = line.replace("&doublepipe;", "||")  # DOCUMENTAR
        result_file_contents = f"{result_file_contents}\n{line}"

    compile_mode = HEAD
    requires_margin_above = False
    just_added_title_importance = 0
    added_visible_content = False
    result_file_contents = "<!-- Generated using Lartu's WebSCFL Builder -->"
    new_filename = replace_extension(filename.split("/")[-1], ".html")
    print(f"Compiling: {filename}")
    with open(filename, "r") as file:
        for line in file.readlines():
            line = line.strip()

            if line and line[0] in ["#", "!"]:
                continue

            tokens = line.split(None, 1)
            if tokens:
                command = tokens[0].upper().strip()
                argument = tokens[1].strip() if len(tokens) > 1 else ""

                # Non-compile mode commands
                if command == "INCLUDE":
                    try:
                        with open(f"{INCLUDE_DIR}/{argument}") as includefile:
                            add_line_to_file(includefile.read())
                        print(f"Included {INCLUDE_DIR}/{argument} in {new_filename}")
                    except:
                        error(f"Include file {INCLUDE_DIR}/{argument} not found.")
                    continue
                elif command == "COPY":
                    origin, destination = argument.split(",", 1)
                    origin = origin.strip()
                    destination = f"{RESULT_DIR}/{destination.strip()}"
                    try:
                        copy_file_relative(origin, destination)
                    except Exception as e:
                        error(f"Couldn't copy file {origin} to {destination}: {e}")
                    continue
                elif command == "COPYDIR":
                    origin, destination = argument.split(",", 1)
                    origin = origin.strip()
                    destination = f"{RESULT_DIR}/{destination.strip()}"
                    try:
                        copy_dir_relative(origin, destination)
                    except Exception as e:
                        error(f"Couldn't copy directory {origin} to {destination}: {e}")
                    continue

                # Compile mode commands
                if compile_mode == UNDEFINED:
                    error(f"Unknown command {command} in UNDEFINED mode.")

                elif compile_mode == HEAD:
                    if command == "HEAD:":
                        add_line_to_file(f"<head>")
                        compile_mode = HEAD
                    elif command == "BODY:":
                        add_line_to_file(f"</head>")
                        add_line_to_file(f"<body>")
                        compile_mode = BODY
                    elif command == "PAGETITLE":
                        add_line_to_file(f"<title>{argument}</title>")
                    elif command == "BACKGROUND":
                        add_line_to_file("<style>html{")
                        add_line_to_file("background-repeat: repeat;")
                        add_line_to_file(f'background-image: url("{RESULT_IMAGES_DIR}/{argument}");')
                        add_line_to_file("}</style>")
                        try:
                            copy_file_relative(f"{IMAGES_DIR}/{argument}", f"{RESULT_DIR}/{RESULT_IMAGES_DIR}/{argument}")
                        except:
                            error(f"Background image file {IMAGES_DIR}/{argument} not found.")
                    elif command == "DESCRIPTION":
                        add_line_to_file(f'<meta name="description" content="{argument}">')
                    elif command == "STYLE":
                        add_line_to_file(f'<link rel="stylesheet" href="{argument}">')
                        try:
                            copy_file_relative(f"{INCLUDE_DIR}/{argument}", f"{RESULT_DIR}/{argument}")
                        except:
                            error(f"Style file {INCLUDE_DIR}/{argument} not found.")
                    else:
                        error(f"Unknown command {command} in HEAD mode.")

                elif compile_mode == BODY:
                    if command == "TITLE":
                        '''if added_visible_content:
                            if just_added_title_importance >= 3:
                                add_line_to_file("<div class='mid_separator'></div>")
                            else:
                                add_line_to_file("<div class='big_separator'></div>")'''
                        add_line_to_file(f"<h1>{argument}</h1>")
                        requires_margin_above = True
                        just_added_title_importance = 3
                        added_visible_content = True
                    elif command == "HEADER":
                        if added_visible_content:
                            if just_added_title_importance >= 2:
                                add_line_to_file("<div class='mid_separator'></div>")
                            else:
                                add_line_to_file("<div class='big_separator'></div>")
                        add_line_to_file(f"<h2>{argument}</h2>")
                        requires_margin_above = True
                        just_added_title_importance = 2
                        added_visible_content = True
                    elif command == "SUBHEADER":
                        if added_visible_content:
                            if just_added_title_importance >= 1:
                                add_line_to_file("<div class='small_separator'></div>")
                            else:
                                add_line_to_file("<div class='mid_separator'></div>")
                        add_line_to_file(f"<h3>{argument}</h3>")
                        requires_margin_above = True
                        just_added_title_importance = 1
                        added_visible_content = True
                    elif command == "LINK":
                        if requires_margin_above:
                            add_line_to_file("<div class='small_separator'></div>")
                        just_added_title_importance = 0
                        separator = "||"
                        if separator not in argument:
                            separator = ","
                        linktokens = argument.split(separator, 2)
                        linktext = linktokens[0].strip().replace("&com;", ",")
                        linktext = linktext.replace("&doublepipe;", "||")
                        linkdest = linktokens[1].strip()
                        othertext = "" if len(linktokens) < 3 else linktokens[2].strip()
                        target = ""
                        external = ""
                        if "http://" in linkdest or "https://" in linkdest:
                            target = "target=_blank"
                            external = f"<img src='{RESULT_IMAGES_DIR}/external-link.png'>"
                        if othertext and othertext[0] not in "),.;:!?":
                            othertext = f" {othertext}"
                        add_line_to_file(f"<a class='link' href='{linkdest}' {target}>{linktext}{external}</a>{othertext}")
                        added_visible_content = True
                    elif command == "WRITE":
                        just_added_title_importance = 0
                        if requires_margin_above:
                            add_line_to_file("<div class='small_separator'></div>")
                        add_line_to_file(f"{argument}")
                        requires_margin_above = False
                        added_visible_content = True
                    elif command == "IMAGE":
                        just_added_title_importance = 0
                        if requires_margin_above:
                            add_line_to_file("<div class='small_separator'></div>")
                        imagetokens = argument.split(",", 1)
                        imagesrc = imagetokens[0].strip()
                        classes = imagetokens[1].strip().replace(",", " ") if len(imagetokens) >= 2 else ""
                        add_line_to_file(f"<div><img src='{RESULT_IMAGES_DIR}/{imagesrc}' class='{classes}'</img></div>")
                        try:
                            copy_file_relative(f"{IMAGES_DIR}/{imagesrc}", f"{RESULT_DIR}/{RESULT_IMAGES_DIR}/{imagesrc}")
                        except:
                            error(f"Image file {IMAGES_DIR}/{imagesrc} not found.")
                        requires_margin_above = True
                        added_visible_content = True
                    elif command == "LINKIMAGE":
                        just_added_title_importance = 0
                        if requires_margin_above:
                            add_line_to_file("<div class='small_separator'></div>")
                        imagetokens = argument.split(",", 2)
                        imagesrc = imagetokens[0].strip()
                        destination = imagetokens[1].strip()
                        classes = imagetokens[2].strip().replace(",", " ") if len(imagetokens) >= 3 else ""
                        target = ""
                        if "http://" in destination or "https://" in destination:
                            target = "target=_blank"
                        add_line_to_file(f"<div><a class='linkimage' href='{destination}' {target}><img src='{RESULT_IMAGES_DIR}/{imagesrc}' class='{classes}'><img src='{RESULT_IMAGES_DIR}/external-link.png'></a></div>")
                        try:
                            copy_file_relative(f"{IMAGES_DIR}/{imagesrc}", f"{RESULT_DIR}/{RESULT_IMAGES_DIR}/{imagesrc}")
                        except:
                            error(f"Image file {IMAGES_DIR}/{imagesrc} not found.")
                        requires_margin_above = True
                        added_visible_content = True
                    elif command == "FOOTNOTE":
                        just_added_title_importance = 0
                        if requires_margin_above:
                            add_line_to_file("<div class='small_separator'></div>")
                        add_line_to_file(f"<div class='footnote'>{argument}</div>")
                        requires_margin_above = True
                        added_visible_content = True
                    elif command == "BREAK":
                        just_added_title_importance = 0
                        add_line_to_file("<div class='small_separator'></div>")
                        add_line_to_file("<div class='small_separator'></div>")
                    elif command == "LISTITEM":
                        just_added_title_importance = 0
                        if requires_margin_above:
                            add_line_to_file("<div class='small_separator'></div>")
                        requires_margin_above = False
                        added_visible_content = True
                        add_line_to_file(f"<li class='list_item'>{argument}</li>")
                    elif command == "NEWLINE":
                        just_added_title_importance = 0
                        add_line_to_file("<br>")
                    elif command == "COMPILENOTE":
                        just_added_title_importance = 0
                        add_line_to_file(f"<div class='compilenote'>{webpage_compiled_message()}</div>")
                    else:
                        error(f"Unknown command {command} in BODY mode.")


    if compile_mode == HEAD:
        add_line_to_file("</head>")
    elif compile_mode == BODY:
        add_line_to_file("</body>")
    add_line_to_file("</html>")

    
    print(f"Compiled {filename}. Saving to {RESULT_DIR}/{new_filename}...")

    with open(f"{RESULT_DIR}/{new_filename}", "w+") as resultfile:
        resultfile.write(result_file_contents)
    
    print(f"Saved {RESULT_DIR}/{new_filename}.")


def setup():
    create_directory("docs")
    create_directory("docs/images")
    try:
        shutil.copytree("files", "docs/files")
        print("Copied the files directory to docs/files")
    except Exception as e:
        print(f"Warning: files director not found. Skipping copy.")
    try:
        copy_file_relative(f"{OTHER_DIR}/external-link.png", f"{RESULT_DIR}/{RESULT_IMAGES_DIR}/external-link.png")
    except:
        error(f"Style file {OTHER_DIR}/external-link.png not found.")


if __name__ == "__main__":
    setup()
    for filename in list_files_in_folder("src"):
        compile_file(filename)