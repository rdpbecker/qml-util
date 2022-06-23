import re
from qmlTypes import BaseTypes

class SignalType(BaseTypes.BasicMatch):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*signal\s(.*)")
        self.kind = "s"

    def _name(self):
        return self.match.group(1)
