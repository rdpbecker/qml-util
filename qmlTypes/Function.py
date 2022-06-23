import re
from qmlTypes import BaseTypes

class FuncType(BaseTypes.BasicMatch):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*function\s(.*)\s*{")
        self.kind = "f"

    def _name(self):
        return self.match.group(1)
