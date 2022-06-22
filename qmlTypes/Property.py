import re
import util
from qmlTypes import BaseTypes

class PropType(BaseTypes.Match):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*property\s(\w+)\s(\w+)")

    def attemptMatch(self):
        line = self.component.content[self.index]
        propmatch = self.regex.match(line)

        if not propmatch:
            return False

        self.component.properties.append(\
            Property(\
                propmatch.group(2)+" : "+propmatch.group(1),\
                self.component.file,\
                self.index+self.component.index,\
                self.component.hier+[self.component.name]
            )
        )
        self.index = self.index + 1
        return True

class Property(BaseTypes.HierTag):
    def __init__(self,name,file,index,hier):
        super().__init__(name,file,index,hier,"p")
