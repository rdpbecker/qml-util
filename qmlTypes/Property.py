import re
from qmlTypes import BaseTypes

class PropType(BaseTypes.BasicMatch):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*property\s(\w+)\s(\w+)")
        self.kind = "p"

    def _name(self):
        return self.match.group(2)+" : "+self.match.group(1)
