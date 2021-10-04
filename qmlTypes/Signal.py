import re
import util
from qmlTypes import BaseTypes

class SignalType(BaseTypes.Match):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*signal\s(.*)")

    def attemptMatch(self):
        line = self.component.content[self.index]
        signalmatch = self.regex.match(line)

        if not signalmatch:
            return False

        self.component.properties.append(\
            Signal(\
                signalmatch.group(1),\
                self.component.file,\
                util.createPattern(line,len(self.component.hier)+1),\
                self.component.hier+[self.component.name]\
            )\
        )
        self.index = self.index + 1
        return True

class Signal(BaseTypes.HierTag):
    def __init__(self,name,file,pattern,hier):
        super().__init__(name,file,pattern,hier,"s")
