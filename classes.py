class Integer():
    def __init__(self, value = 0):
        self.value = value

    def __iadd__(self, other):
        self.value += other
        return self

class scopeEntity():
    def __init__(self, name, type_, scope):
        self.name = name
        self.type_ = type_
        self.scope = scope

class DTEntity():
    def __init__(self, name, type_, parent, CDT):
        self.name = name
        self.type_ = type_
        self.parent = parent
        self.CDT = CDT

class CDTEntity():
    def __init__(self, name, type_, AM, TM):
        self.name = name
        self.type_ = type_
        self.AM = AM
        self.TM = TM

class compatEntity():
    def __init__(self, left, right, op, result):
        self.left = left
        self.right = right
        self.op = op
        self.result = result

class Stack():
    def __init__(self):
        self.list = []
        self.count = 1
        self.peekDepth = -1

    def createScope(self):
        self.list.append(self.count)
        self.count+=1
        self.peekDepth+=1

    def deleteScope(self):
        self.list.pop()

    def peek(self):
        return self.list[len(self.list)-1]