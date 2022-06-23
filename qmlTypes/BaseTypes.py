import util
import re
from qmlTypes import Component

class Match:
    def __init__(self,component,index):
        self.component = component
        self.index = index
        self.match = None

    def attemptMatch(self):
        return False

class BasicMatch(Match):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = None
        self.kind = ""

    def attemptMatch(self):
        if not self.regex:
            return False

        self.match = self.regex.match(self.component.content[self.index])
        if not self.match:
            return False

        end, _ = util.getMatchingBrace(self.component.content,self.index)
        self.component.properties.append(\
            HierTag(\
                self.name(),\
                self.component.file,\
                self.index+self.component.index,\
                self.component.hier+[self.component.name],\
                self.kind\
            )\
        )
        self.index = end + 1
        return True

    def _name(self):
        return ""

    def name(self):
        if not self.match:
            return ""
        return self._name()

class MaybeCompMatch(BasicMatch):
    def __init__(self,component,index):
        super().__init__(component,index)
        self.regex = None
        self.kind = ""

    def attemptMatch(self):
        if not self.regex:
            return False

        line = self.component.content[self.index]
        self.match = self.regex.match(line)
        if not self.match:
            return False

        comp_regex = re.compile(r":\s*(\w+)\s*{$")
        comp_match = comp_regex.search(line)
        end, content = util.getMatchingBrace(self.component.content,self.index)

        if comp_match:
            self.component.components.append(\
                Component.Component(\
                    comp_match.group(1) + " [" + self.tag_name() + "]",\
                    self.component.file,\
                    content,\
                    self.index+self.component.index,\
                    self.component.hier+[self.component.name]\
                )\
            )
        else:
            self.component.properties.append(\
                HierTag(\
                    self.name(),\
                    self.component.file,\
                    self.index+self.component.index,\
                    self.component.hier+[self.component.name],\
                    self.kind\
                )\
            )
        self.index = end + 1
        return True

    def _tag_name(self):
        return ""

    def tag_name(self):
        if not self.match:
            return ""
        return self._tag_name()

class Tag:
    """Base class representing a ctags Tag."""
    def __init__(self, name, file, index, kind):
        self.name = name
        self.file = file
        self.index = index + 1
        self.kind = kind

    def __str__(self):
        """Tab-separated textual representation of the tag."""
        return "\t".join([self.name, self.file+";\"", self.kind, "line:"+str(self.index)])

class HierTag(Tag):
    def __init__(self,name,file,index,hier,tag):
        super().__init__(name,file,index,tag)
        self.hier = hier

    def __str__(self):
        return super().__str__() + "\tcomponent:" + ",".join(self.hier)
