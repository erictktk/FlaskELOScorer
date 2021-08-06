import os.path
import argparse

import os
import sys


EXT_MAP = {".ttf": "truetype", ".otf": "opentype"}


def create_css(directory):
    """
    Writes a css file from all the fonts in a directory

    :param directory:
    :return:
    """
    entries = os.listdir(directory)

    file_path = os.path.join(directory, 'fontStyle.css')

    with open(file_path, 'w') as f:
        entire_text = ""
        for i, e in enumerate(entries):
            splitext = os.path.splitext(e)

            actual_entry = splitext[0]
            ext = splitext[1]

            relative_path = None

            first_line = "@font-face { \n"
            second_line = '  font-family: "{0}"; \n'.format(actual_entry)
            third_line = '  src: url("{0}") format("{1}"); }\n'.format(relative_path, EXT_MAP[ext])
            space = '\n'

            entire_text += first_line + second_line + third_line + space

        f.write(entire_text)