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
import re

prop_re = re.compile(r"^\s*property\s(\w+)\s(\w+)")
signal_re = re.compile(r"^\s*signal\s(.*)")
func_re = re.compile(r"^\s*function\s(.*)")
comp_re = re.compile(r"^\s*([A-Z].*)\s\{") #}

def print_lines_debug(lines):
    for line in lines:
        print(line[:-1])

class Tag:
    """Base class representing a ctags Tag."""
    def __init__(self, name, file, pattern, kind):
        self.name = name
        self.file = file
        self.pattern = pattern
        self.kind = kind

    def __str__(self):
        """Tab-separated textual representation of the tag."""
        return "\t".join([self.name, self.file, self.pattern, self.kind])

class Component(Tag):
    def __init__(self,name,file,pattern,content,hier=[]):
        super().__init__(name,file,pattern,"c")
        self.content = content
        self.hier = hier
        self.properties = []
        self.functions = []
        self.components = []
    
    def __str__(self):
        if not len(self.hier):
            return super().__str__()
        return super().__str__() + "\tcomponent:" + ",".join(self.hier)

    def parse(self):
        index = 0
        while index < len(self.content):
            line = self.content[index]
            propmatch = prop_re.match(line)
            if propmatch:
                self.properties.append(Property(propmatch.group(2)+" : "+propmatch.group(1),self.file,createPattern(line,len(self.hier)+1),self.hier+[self.name]))
                index = index + 1
                continue

            signalmatch = signal_re.match(line)
            if signalmatch:
                self.properties.append(Signal(signalmatch.group(1)+" : "+signalmatch.group(1),self.file,createPattern(line,len(self.hier)+1),self.hier+[self.name]))
                index = index + 1
                continue

            funcmatch = func_re.match(line)
            if funcmatch:
                end, content = getMatchingBrace(self.content,index)
                self.functions.append(Function(funcmatch.group(1),self.file,createPattern(line,len(self.hier)+1),self.hier+[self.name]))
                index = end + 1
                continue

            compmatch = comp_re.match(line)
            if compmatch:
                if "}" in line:
                    self.components.append(Component(compmatch.group(1),self.file,createPattern(line,len(self.hier)+1),line,self.hier+[self.name]))
                    index = index + 1
                    continue
                end, content = getMatchingBrace(self.content,index)
                name = compmatch.group(1)
                if len(content):
                    idmatch = content[0].find("id:")
                    if idmatch >= 0:
                        name_id = content[0][idmatch+4:].strip()
                        name = name + " [" + name_id + "]"
                self.components.append(Component(name,self.file,createPattern(line,len(self.hier)+1),content,self.hier+[self.name]))
                index = end + 1
                continue
            
            index = index + 1

        for child in self.components:
            child.parse()

    def printChildren(self,recurse=True):
        for prop in self.properties:
            print(prop)
        for func in self.functions:
            print(func)
        for comp in self.components:
            print(comp)
            if (recurse):
                comp.printChildren()

class HierTag(Tag):
    def __init__(self,name,file,pattern,hier,tag):
        super().__init__(name,file,pattern,tag)
        self.hier = hier

    def __str__(self):
        return super().__str__() + "\tcomponent:" + ",".join(self.hier)

class Property(HierTag):
    def __init__(self,name,file,pattern,hier):
        super().__init__(name,file,pattern,hier,"p")

class Function(HierTag):
    def __init__(self,name,file,pattern,hier):
        super().__init__(name,file,pattern,hier,"f")

class Signal(HierTag):
    def __init__(self,name,file,pattern,hier):
        super().__init__(name,file,pattern,hier,"s")

def unindent(content):
    return [line[indent:] for line in content]

def numForwardBraces(line):
    count = 0
    while line.find("{") > -1:
        line = line[:line.find("{")] + line[line.find("{")+1:]
        count = count + 1
    return count

def numBackBraces(line):
    count = 0
    while line.find("}") > -1:
        line = line[:line.find("}")] + line[line.find("}")+1:]
        count = count + 1
    return count

def getMatchingBrace(content,start):
    braceCount = 0
    for i in range(start,len(content)):
        if not len(content[i]):
            continue
        braceCount = braceCount + numForwardBraces(content[i]) - numBackBraces(content[i])
        if not braceCount:
            return i, unindent(content[start+1:i])
    return len(content), content[start+1:]

def findComponent(content):
    start = -1
    end = -1
    for num,line in enumerate(content):
        if "{" in line and start < 0:
            start = num
            continue
        if line[0] == "}" and start >= 0:
            end = num
            break
    return start, end

def createPattern(line,indents):
    new = "".join([" " for _ in range(indents*indent)]) + line.strip() 
    return "/^{}$/;\"".format(new)

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

    start,end = findComponent(file_content)
    if end < 0:
        exit()

    name = file_content[start][:-3]
    pattern = createPattern(file_content[start],0)
    idmatch = file_content[start+1].find("id:")
    if idmatch >= 0:
        name_id = file_content[start+1][idmatch+4:].strip()
        name = name + " [" + name_id + "]"
    root = Component(name,filename,pattern,unindent(file_content[start+1:end]))
    root.parse()
    print(root)
    root.printChildren()

main()
