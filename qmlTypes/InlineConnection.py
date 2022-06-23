import re
from qmlTypes import BaseTypes

class InlineConnType(BaseTypes.BasicMatch):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*on(\w+)")
        self.kind = "q"

    def _name(self):
        return "on" + self.match.group(1)
