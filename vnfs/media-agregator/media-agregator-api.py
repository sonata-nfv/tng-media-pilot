#!/usr/bin/python3

from flask import Flask, request, Response

import codecs
import re

INDENTATION = ' ' * 4

TEMPLATE_VARIABLE_OPENING_TAG = '___TEMPLATE_VARIABLE_OPENING_TAG___'
TEMPLATE_VARIABLE_CLOSING_TAG = '___TEMPLATE_VARIABLE_CLOSING_TAG___'

app = Flask(__name__)

"""Additional functions for formatting the nginx.conf"""

def strip_line(single_line):
    """Strips the line and replaces neighbouring whitespaces with single space (except when within quotation marks)."""
    single_line = single_line.strip()
    if single_line.startswith('#'):
        return single_line

    within_quotes = False
    parts = []
    for part in re.split('"', single_line):
        if within_quotes:
            parts.append(part)
        else:
            parts.append(re.sub(r'[\s]+', ' ', part))
        within_quotes = not within_quotes
    return '"'.join(parts)


def apply_variable_template_tags(line: str) -> str:
    """Replaces variable indicators ${ and } with tags, so subsequent formatting is easier."""
    return re.sub(r'\${\s*(\w+)\s*}',
                  TEMPLATE_VARIABLE_OPENING_TAG + r"\1" + TEMPLATE_VARIABLE_CLOSING_TAG,
                  line,
                  flags=re.UNICODE)


def strip_variable_template_tags(line: str) -> str:
    """Replaces tags back with ${ and } respectively."""
    return re.sub(TEMPLATE_VARIABLE_OPENING_TAG + r'\s*(\w+)\s*' + TEMPLATE_VARIABLE_CLOSING_TAG,
                  r'${\1}',
                  line,
                  flags=re.UNICODE)


def clean_lines(orig_lines) -> list:
    """Strips the lines and splits them if they contain curly brackets."""
    cleaned_lines = []
    for line in orig_lines:
        line = strip_line(line)
        line = apply_variable_template_tags(line)
        if line == "":
            cleaned_lines.append("")
            continue
        else:
            if line.startswith("#"):
                cleaned_lines.append(strip_variable_template_tags(line))
            else:
                cleaned_lines.extend(
                    [strip_variable_template_tags(l).strip() for l in re.split(r"([{}])", line) if l != ""])

    return cleaned_lines


def join_opening_bracket(lines):
    """When opening curly bracket is in it's own line (K&R convention), it's joined with precluding line (Java)."""
    modified_lines = []
    for i in range(len(lines)):
        if i > 0 and lines[i] == "{":
            modified_lines[-1] += " {"
        else:
            modified_lines.append(lines[i])
    return modified_lines


def perform_indentation(lines):
    """Indents the lines according to their nesting level determined by curly brackets."""
    indented_lines = []
    current_indent = 0
    for line in lines:
        if not line.startswith("#") and line.endswith('}') and current_indent > 0:
            current_indent -= 1

        if line != "":
            indented_lines.append(current_indent * INDENTATION + line)
        else:
            indented_lines.append("")

        if not line.startswith("#") and line.endswith('{'):
            current_indent += 1

    return indented_lines


def format_config_contents(contents):
    """Accepts the string containing nginx configuration and returns formatted one. Adds newline at the end."""
    lines = contents.splitlines()
    lines = clean_lines(lines)
    lines = join_opening_bracket(lines)
    lines = perform_indentation(lines)

    text = '\n'.join(lines)

    for pattern, substitute in ((r'\n{3,}', '\n\n\n'), (r'^\n', ''), (r'\n$', '')):
        text = re.sub(pattern, substitute, text, re.MULTILINE)

    return text + '\n'


def format_config_file(file_path):
    """
    Performs the formatting on the given file. The function tries to detect file encoding first.
    :param file_path: path to original nginx configuration file. This file will be overridden.
    """
    encodings = ('utf-8', 'latin1')

    encoding_failures = []
    chosen_encoding = None

    for enc in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=enc) as rfp:
                original_file_content = rfp.read()
            chosen_encoding = enc
            break
        except ValueError as e:
            encoding_failures.append(e)

    if chosen_encoding is None:
        raise Exception('none of encodings %s are valid for file %s. Errors: %s'
                        % (encodings, file_path, [e.message for e in encoding_failures]))

    assert original_file_content is not None

    with codecs.open(file_path, 'w', encoding=chosen_encoding) as wfp:
        wfp.write(format_config_contents(original_file_content))


"""This function creates an app in the nginx.conf for the new camera"""
@app.route("/connectCamera", methods=["PUT"])
def connect_camera():
    input_json = request.get_json()

    stream_app = input_json['stream_app']

    code_block = "application "+ stream_app + " {\n " \
                                              "live on;\n " \
                                              "record off;\n" \
                                              "#-Insert Push here-\n" \
                                              "}\n"

    with open("/opt/nginx/nginx.conf", "r") as myfile:
        data = myfile.readlines()
        index = data.index('        #-Insert Application here-\n')
        data.insert(index + 1, code_block)

        data_str = ''.join(data)

        with open("/opt/nginx/nginx.conf", "w") as output:
            output.write(data_str)

    format_config_file("/opt/nginx/nginx.conf")

    return Response(None, status=200, content_type='application/json')


"""This function adds a push statement in a specific app"""
@app.route("/connectStream", methods=["PUT"])
def connect_stream():
    input_json = request.get_json()

    stream_app = input_json['stream_app']
    stream_key = input_json['stream_key']

    push_url = "push rtmp://10.100.16.56:1935/stream/"+stream_key+";" #TODO: Change the harcoded url to the real server

    with open("/opt/nginx/nginx.conf", "r") as myfile:
        data = myfile.readlines()
        index = data.index('        application ' + stream_app + ' {\n')
        data.insert(index + 4, push_url)

        data_str = ''.join(data)

        with open("/opt/nginx/nginx.conf", "w") as output:
            output.write(data_str)

    format_config_file("/opt/nginx/nginx.conf")

    return Response(None, status=200, mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #app.run(debug=True)
