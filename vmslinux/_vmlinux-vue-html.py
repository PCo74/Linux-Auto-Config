#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
generates a view of VMs in HTML format
©PCo-2017/2022
"""

import glob
import html
import os
import re
import sys
import webbrowser
from enum import Enum

from lib.vm_filename import VmFilename
from lib.init_file import InitFile

FIC_CONFIG = "../config.ini"

HTML_SCHEMA = """<p><img src="{0}" alt="schema"></p>"""

HTML_ATTENTION = """# <strong>✋ {0}</strong>"""

HTML_DETAILS = """
        <details>
            <summary><em>{0}</em> {1}</summary>
            <pre>\n{2}</pre>
        </details>
"""

HTML_CSS = """
        body { font-family: system-ui; }
        h1 > em { color: navy; font-style: normal;  }
        img { border: 1px silver solid; padding: 10px; border-radius: 15px; }
        em { border-radius: .3em; padding: .0em .2em; background-color: lightblue; }
        strong { color: red; }
        pre { background-color: wheat; color: navy; border-radius: .3em; padding: .2em; overflow: auto; }      
        details > summary { padding: 4px; background-color: #eee; border: none;
            box-shadow: 1px 1px 2px #bbb; cursor: pointer; margin-top: 0.5em; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type">
    <title>{0}</title>
    <meta name="author" content="PCo-2016/2022">
    <meta name="description" content="linux, VM">
    <style>
        {1}
    </style>
  </head>
  <body>
    <h1><em>[ {2} ] :: {0}</em></h1>
    {4}
    
    {3}
  </body>
</html>
"""


class Block:
    """
    block representing either a configuration file or commands to execute
    """

    class BlockType(Enum):
        FILE_CONFIG = "nano"
        BASH_CMD = "cmd bash"

    def __init__(self, name):
        self.name = name
        self._lines = []
        if name[0] == "/" or name[0] == ".":
            self.type = Block.BlockType.FILE_CONFIG
        else:
            self.type = Block.BlockType.BASH_CMD

    def add_line(self, line):
        line = html.escape(line).replace(chr(27), '␛')
        if line[0:5] == "# !!!":
            line = HTML_ATTENTION.format(line[5:])
        self._lines.append(line)

    def is_viewed(self):
        block_exceptions = (r"/etc/issue", r"_(.*)$")
        for be in block_exceptions:
            if re.match(be, self.name):
                return False
        return True

    def get_content(self):
        return "\n".join(self._lines)


class VM:
    """
    definition of a Virtual Machine
    """

    FILE_CONFIG = "../config.ini"

    def __init__(self, filename, id_file):
        self.filename = filename
        self.id_file = id_file
        self.blocks = []
        self.vf = VmFilename(filename)

    def extract_blocks(self):
        id_file_lg = len(self.id_file)
        block = None
        with open(self.filename, 'r', -1, "utf-8") as ft:
            for line in ft:
                line = line.rstrip('\n\r')
                if line[:id_file_lg] == self.id_file:  # mark block name
                    if block is not None:  # not first block
                        self.blocks.append(block)
                    block = Block(line[id_file_lg:].split()[0])
                else:
                    block.add_line(line)
        if block is not None:
            self.blocks.append(block)

    def generate_html(self):
        details = ""
        for blk in vm.blocks:
            if blk.is_viewed():
                details += HTML_DETAILS.format(blk.type.value, blk.name, blk.get_content().strip())

        img = HTML_SCHEMA.format(vm.vf.schema) if self.vf.schema else ""
        with open(self.vf.html, 'w', -1, "utf-8") as fh:
            fh.write(HTML_TEMPLATE.format(
                self.vf.name, HTML_CSS, self.vf.last_dir, details, img))


# main #################################################################################################################

if len(sys.argv) < 2:
    sys.exit("""Argument manquant !
Syntaxe : _vmslinux-vue-html.py {<répertoire>|<fichier>.txt}""")

init_file = InitFile(VM.FILE_CONFIG)

source = os.path.basename(sys.argv[1])
if os.path.isdir(source):
    source = source + os.path.sep + "*.txt"

glob_source = glob.glob(source)
if glob_source:
    for fic in glob.glob(source):
        vm = VM(fic, init_file.props['IDFIC'])
        vm.extract_blocks()
        vm.generate_html()
        webbrowser.open(vm.vf.url, new=2)
else:
    print(source, " -> aucun fichier de VMs trouvé !!!")
