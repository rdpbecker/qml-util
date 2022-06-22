import re
import util
from qmlTypes import BaseTypes, Property, Signal, Function, Component

class CompType(BaseTypes.Match):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*([A-Z].*)\s\{") #}

    def attemptMatch(self):
        line = self.component.content[self.index]
        compmatch = self.regex.match(line)

        if not compmatch:
            return False

        if "}" in line:
            self.component.components.append(\
                Component(\
                    compmatch.group(1),\
                    self.component.file,\
                    line,\
                    self.index+self.component.index,\
                    self.component.hier+[self.component.name]\
                )\
            )
            self.index = self.index + 1

        else:
            end, content = util.getMatchingBrace(self.component.content,self.index)
            name = compmatch.group(1)
            if len(content):
                idmatch = content[0].find("id:")
                if idmatch >= 0:
                    name_id = content[0][idmatch+4:].strip()
                    name = name + " [" + name_id + "]"

            self.component.components.append(\
                Component(\
                    name,\
                    self.component.file,\
                    content,\
                    self.index+self.component.index,\
                    self.component.hier+[self.component.name]\
                )\
            )
            self.index = end + 1

        return True

class Component(BaseTypes.Tag):
    def __init__(self,name,file,content,index=0,hier=[]):
        super().__init__(name,file,index,"c")
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
        matcher = BaseTypes.Match(self,0)
        while index < len(self.content):
            handled = False
            for tagType in [Property.PropType,Signal.SignalType,Function.FuncType,CompType]:
                matcher = tagType(self,index)
                if (matcher.attemptMatch()):
                    handled = True
                    break

            if handled:
                index = matcher.index
            else:
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
