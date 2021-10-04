import re
import util
from qmlTypes import BaseTypes

class FuncType(BaseTypes.Match):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*function\s(.*)")

    def attemptMatch(self):
        line = self.component.content[self.index]
        funcmatch = self.regex.match(line)

        if not funcmatch:
            return False

        end, _ = util.getMatchingBrace(self.component.content,self.index)

        self.component.functions.append(\
            Function(\
                funcmatch.group(1),\
                self.component.file,\
                util.createPattern(line,len(self.component.hier)+1),\
                self.component.hier+[self.component.name]\
            )\
        )
        self.index = end + 1
        return True

class Function(BaseTypes.HierTag):
    def __init__(self,name,file,pattern,hier):
        super().__init__(name,file,pattern,hier,"f")
