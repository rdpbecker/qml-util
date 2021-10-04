#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

help_text = """
Extracts tags from QML files. Useful for the Tagbar plugin.

Usage:

Install Tagbar (http://majutsushi.github.io/tagbar/). Then, put this 
file anywhere and add the following to your .vimrc:

let g:tagbar_type_qml = {
        \\   'ctagstype':'qml'
        \\ , 'kinds':['c:component', 'f:function', 'p:property', 's:signal']
        \\ , 'ctagsbin':'~/Projects/qmltags/qmltags.py'
        \\ , 'ctagsargs':''
        \\ , 'sro':','
        \\ , 'kind2scope':{'c':'component'}
        \\ , 'scope2kind':{'component':'c'}
        \\ }
"""
indent = 4

import sys
import util
from qmlTypes import Component

def findComponents(content):
    components = []
    num = 0
    while num < len(content):
        if "{" in content[num]:
            end, component = util.getMatchingBrace(content,num)
            components.append([num,component])
            num = end
        num = num + 1
    return components

def main():
    if len(sys.argv) < 2:
        print(help_text)
        exit()

    filename = sys.argv[1]

    file_content = []
    try:
        with open(filename, "r") as vim_buffer:
            file_content = vim_buffer.readlines()
    except:
        exit()

    components = findComponents(file_content)
    if len(components) == 0:
        exit()

    component = components[-1]

    name = file_content[component[0]][:-3]
    pattern = util.createPattern(file_content[component[0]],0)
    idmatch = component[1][0].find("id:")
    if idmatch >= 0:
        name_id = component[1][0][idmatch+4:].strip()
        name = name + " [" + name_id + "]"
    root = Component.Component(name,filename,pattern,component[1])
    root.parse()
    print(root)
    root.printChildren()

main()
