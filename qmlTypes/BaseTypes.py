class Match:
    def __init__(self,component,index):
        self.component = component
        self.index = index
        self.match = None

    def attemptMatch(self):
        pass

class Tag:
    """Base class representing a ctags Tag."""
    def __init__(self, name, file, pattern, kind):
        self.name = name
        self.file = file
        self.pattern = pattern
        self.kind = kind

    def __str__(self):
        """Tab-separated textual representation of the tag."""
        return "\t".join([self.name, self.file, self.pattern, self.kind])

class HierTag(Tag):
    def __init__(self,name,file,pattern,hier,tag):
        super().__init__(name,file,pattern,tag)
        self.hier = hier

    def __str__(self):
        return super().__str__() + "\tcomponent:" + ",".join(self.hier)
