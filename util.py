indent = 4

def print_lines_debug(lines):
    for line in lines:
        print(line[:-1])

def createPattern(line,indents):
    new = "".join([" " for _ in range(indents*indent)]) + line.strip() 
    return "/^{}$/;\"".format(new)

def unindent(content):
    return [line[indent:] for line in content]

def numForwardBraces(line):
    count = 0
    while line.find("{") > -1:
        line = line[:line.find("{")] + line[line.find("{")+1:]
        count = count + 1
    return count

def numBackBraces(line):
    count = 0
    while line.find("}") > -1:
        line = line[:line.find("}")] + line[line.find("}")+1:]
        count = count + 1
    return count

def getMatchingBrace(content,start):
    braceCount = 0
    for i in range(start,len(content)):
        if not len(content[i]):
            continue
        braceCount = braceCount + numForwardBraces(content[i]) - numBackBraces(content[i])
        if not braceCount:
            return i, unindent(content[start+1:i])
    return len(content), content[start+1:]
