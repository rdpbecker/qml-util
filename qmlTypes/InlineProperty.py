import re
from qmlTypes import BaseTypes

class InlinePropType(BaseTypes.MaybeCompMatch):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = re.compile(r"^\s*(\w+):")
        self.kind = "p"

    def _name(self):
        return self.match.group(1) + " : unknown"

    def _tag_name(self):
        return self.match.group(1)
