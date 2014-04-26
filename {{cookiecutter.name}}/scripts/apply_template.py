# -- coding: utf-8 --
"""
Usage:
    apply_template.py -i input_file -o output_file -t template

Options:
    -i input_file   Input tex file to use as the templates body.
    -o output_file  Output tex file.
    -t template     Template filename to use (shall be inside templates folder).
    -h, --help      Show this screen and exit.
"""

from jinja2 import Environment, FileSystemLoader
from docopt import docopt
import os
import sys
import encoding

# Add parent directory to the path.
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PARENT_DIR)
from metadata import *


def process_tex_file(input_path, template_name):
    with open(input_path, "r") as tex_file:
        body = tex_file.read()

    citations_found = "\cite{" in body

    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template(template_name)
    return template.render(body=body, citations_found=citations_found, **globals())


if __name__ == "__main__":
    arguments = docopt(__doc__)

    # Solve a problem with the encoding of the metadata.
    encoding.set_system_encoding_utf8()

    processed_tex_file = process_tex_file(arguments["-i"], arguments["-t"])

    with open(arguments["-o"], "w") as output_file:
        output_file.write(processed_tex_file.encode("utf-8"))