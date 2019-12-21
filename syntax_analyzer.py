import sys
import lexical_analyzer as lexi
import time
import os


class Integer():

    def __init__(self, value = 0):
        self.value = value

    def __iadd__(self, other):
        self.value += other
        return self
        
ARROW = "-->"
TYPE = "TYPE"
T_RIGHT = "T_RIGHT"
R_Type = "R_Type"
ACCESS_MODIFIER = "ACCESS_MODIFIER"
TYPE_MODIFIER = "TYPE_MODIFIER"
PARENT = "PARENT"

DATA_TYPE="DATA_TYPE"
PARAMETER_LIST="PARAMETER_LIST"
CLASS_NAME="CLASS_NAME"
NAME="NAME"
CLASS_DATA_TABLE = "CLASS_DATA_TABLE"


class compatEntity():
    def __init__(self, left, right, op, result):
        self.left = left
        self.right = right
        self.op = op
        self.result = result



compatibilityTable = [
    compatEntity("int", "int", "+", "int"),
    compatEntity("int", "int", "-", "int"),
    compatEntity("int", "int", "*", "int"),
    compatEntity("int", "int", "/", "int"),
    compatEntity("int", "int", "=", "int"),
    compatEntity("text", "text", "=", "text"),
    compatEntity("float", "float", "+", "float"),
    compatEntity("float", "float", "-", "float"),
    compatEntity("float", "float", "*", "float"),
    compatEntity("float", "float", "/", "float"),
    compatEntity("float", "float", "=", "float"),
    compatEntity("boolean", "boolean", "AND", "boolean"),
    compatEntity("boolean", "boolean", "and", "boolean"),
    compatEntity("boolean", "boolean", "OR", "boolean"),
    compatEntity("boolean", "boolean", "or", "boolean"),
    compatEntity("boolean", "boolean", "=", "boolean"),
    #Cross Comptibility Check
    compatEntity("int", "float", "+", "float"),
    compatEntity("float", "int", "+", "float"),
    compatEntity("int", "float", "-", "float"),
    compatEntity("float", "int", "-", "float"),
    compatEntity("int", "float", "*", "float"),
    compatEntity("float", "int", "*", "float"),
    compatEntity("int", "float", "/", "float"),
    compatEntity("float", "int", "/", "float"),
    compatEntity("int", "float", "=", "int"),
    compatEntity("float", "int", "=", "float"),
    compatEntity("boolean", None, "not", "boolean"),
    compatEntity("float", None, "not", "float"),
    compatEntity("int", None, "not", "int"),
    
]


class scopeEntity():
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

class DTEntity():
    def __init__(self, name, type_, parent, CDT):
        self.name = name
        self.type = type_
        self.parent = parent
        self.CDT = CDT

class CDTEntity():
    def __init__(self, name, type_, AM, TM):
        self.name = name
        self.type = type_
        self.AM = AM
        self.TM = TM


scopeTable = []

defTable = []

tokenSet = []

class Stack():

    def __init__(self):
        pass

    def createScope(self):
        pass

    def deleteScope(self):
        pass

    def peek(self):
        pass

scopeStack = Stack()




def lookUpST(N, scopeStack, CDT):
    for item in scopeTable:
        if item.name == N:
            if ARROW in item:
                return item.type_.split(ARROW)[1]
            else:
                return item.type_
    return None


def insertST(N, T):
    if lookUpST(N, scopeStack) == None:
        scopeTable.append(scopeEntity(N, T))

def lookUpDT(N):
    for item in defTable:
        return item.type_
    return None

def insertDT(N, T, parent):
    if lookUpDT(N) == None:
        refTable = []
        defTable.append( DTEntity(N,T,parent,refTable)) 
        return refTable
    
    return False

def lookUpCDT(N, T, CDT):
    for item in CDT:
        if item.name == N:
            if ARROW in item:
                return {R_Type:item.split(ARROW)[1], ACCESS_MODIFIER:item.AM, TYPE_MODIFIER:item.TM}
            else:
               return {R_Type:item, ACCESS_MODIFIER:item.AM, TYPE_MODIFIER:item.TM} 
    return None

def lookUpCDTfromDT(N, T, DTname):
    for item in defTable:
        if item.name == DTname:
            for thing in item.CDT:
                if thing.name == N:
                    if ARROW in item:
                        return {R_Type:thing.split(ARROW)[1], ACCESS_MODIFIER:thing.AM, TYPE_MODIFIER:thing.TM}
                    else:
                        return {R_Type:thing, ACCESS_MODIFIER:thing.AM, TYPE_MODIFIER:thing.TM}
    return None


    


def insertCDT(N, T, AM, TM, CDT):
    if lookUpCDT(N, T, CDT) == None:
        CDT.append(CDTEntity(N, T, AM, TM, CDT))    
        return True
    return False
def getLine(count):
    return tokenSet[count.value][lexi.LINE_NUMBER]        

def getCP(count):
    return tokenSet[count.value][lexi.CLASS_PART]

def getVP(count):
    return tokenSet[count.value][lexi.VALUE_PART]

def checkCompat(type_left, type_right, operator):
    for item in compatibilityTable:
        if type_left == item.left and type_right == item.right and operator == item.op:
            return item.result
    
    return None

def checkCompatUnary(typeOperand, operator):
    for item in compatibilityTable:
        if typeOperand == item.left and None == item.right and operator == item.op:
            return item.result
    
    return None    




def main():
    count = Integer()
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
        global tokenSet
        tokenSet = lexi.lexicalAnalyzer(filePath)
    
        if getCP(count) == lexi.CLASS or getCP(count) == lexi.INTERFACE or getCP(count) == lexi.IMPORT:
            if start(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "$":
                    print ("Successful Parsed")
                    time.sleep(1)
                    os.system('cls')
                    print(r'''
         .* *.               `o`o`
         *. .*              o`o`o`o      ^,^,^
           * \               `o`o`     ^,^,^,^,^
              \     ***        |       ^,^,^,^,^
               \   *****       |        /^,^,^
                \   ***        |       /
    ~@~*~@~      \   \         |      /
  ~*~@~*~@~*~     \   \        |     /
  ~*~@smd@~*~      \   \       |    /     #$#$#        .`'.;.
  ~*~@~*~@~*~       \   \      |   /     #$#$#$#   00  .`,.',
    ~@~*~@~ \        \   \     |  /      /#$#$#   /|||  `.,'
_____________\________\___\____|_/______/_________|\/\___||______
                ''')

                time.sleep(1)
                os.system('cls')
                print(r'''
                                   .''.       
       .''.      .        *''*    :_\/_:     . 
      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.
  .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-
 :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'
 : /\ : :::::     *_\/_*     -= o =-  /)\    '  *
  '..'  ':::'     * /\ *     .'/.\'.   '
      *            *..*         :
        *
        *            Success

                        
                ''')

                return True
        print("error at line {} : {}".format(tokenSet[count.value][lexi.LINE_NUMBER], tokenSet[count.value][lexi.VALUE_PART]))
        return False





###################################################### Definition Functions ###################################################################################################
def import_(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IMPORT":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                if import_(count):
                    return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CLASS" or lexi.INTERFACE or "$":
        return True
    
    return False

#Changed
def start(count):
    if (import_(count)):
        if classStRecursive(count):
            return True
    return False





def inheritanceBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        data[PARAMETER_LIST] = ""
        count+=1
        if insideInheritanceBody(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    return False

#CHANGED
def insideInheritanceBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":

        N = getVP(count)
        data[PARAMETER_LIST] += N
        count+=1
        if inheritanceBodyRecursive(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False



def inheritanceBodyRecursive(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if inheritanceBodyRecursive(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False

def classSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "CLASS":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            CN = getVP(count)
            if lookUpDT(CN) != None:
                print("Redeclaration Error")

            count+=1
            if inheritanceBody(count, data):
                CDT = insertDT(CN, lexi.CLASS, data)
                data[CLASS_DATA_TABLE] = CDT
                data[CLASS_NAME] = CN
                if classBody(count, data):
                    return True
    return False

#CHANGED
def classBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if classBodySt(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False
##################FOLLOW SET NOT COMPLETE#################
def classBodySt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ACCESS_MODIFIERS":
        AM = getVP(count)
        count+=1

        data[ACCESS_MODIFIER] = AM
        if methodAttrOrCons(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False


def methodAttrOrCons(count, data):
    if getCP(count) == lexi.STATIC or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.IDENTIFIER:
        if staticOptional(count, data):
            if classBodyStLf(count, data):
                return True
    elif getCP(count) == lexi.IDENTIFIER:
        count +=1
        if constructorSt(count):
            if classBodySt(count):
                return True

    return False

def classBodyStLf(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.DATA_TYPE:
        DT = getVP(count)
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            N = getVP(count)
            count+=1

            data[DATA_TYPE] = DT
            data[NAME] = N

            if classBodyStLfOne(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        DT = getVP(count)
        if lookUpDT(DT) != None:
            print("Redeclaration Error")

        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            N = getVP(count)
            count+=1

            data[DATA_TYPE] = DT
            data[NAME] = N
            if classBodyStLfTwo(count, data):
                return True
    return False

def classBodyStLfOne(count, data):
    scopeStack.createScope()
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if paramBody(count, data):
            if not insertCDT(data[NAME], data[PARAMETER_LIST]+ARROW+data[DATA_TYPE], data[ACCESS_MODIFIER], data[TYPE_MODIFIER], data[CLASS_DATA_TABLE]):
                print("Function Redeclaration Error at line: {}".format(getLine(count)))
            if body(count, data):
                scopeStack.deleteScope()
                if classBodySt(count, data):
                    return True
    elif getCP(count) == lexi.AS_OP or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        if init(count, data):
            if list_(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == lexi.END_OF_STATEMENT:  
                    count+=1
                    if classBodySt(count, data):
                        return True

    return False

def classBodyStLfTwo(count, data):
    scopeStack.createScope()
    if paramBody(count, data):
        if not insertCDT(data[NAME], data[PARAMETER_LIST], data[ACCESS_MODIFIER], data[TYPE_MODIFIER],data[CLASS_DATA_TABLE]):
            print("Function Redeclaration Error")
        if body(count, data):
            scopeStack.deleteScope()
            if classBodySt(count, data):
                return True
    elif objectInit(count,data):
        if objectList(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == lexi.END_OF_STATEMENT:
                count+=1  
                if classBodySt(count, data):
                    return True

    return False

#changed
def classStRecursive(count):
    if getCP(count) == lexi.CLASS:
        data = {}
        if classSt(count, data):
            if classStRecursive(count):
                return True

    elif getCP(count) == lexi.INTERFACE:
        data = {}      
        if interfaceSt(count, data):
            if classStRecursive(count):
                return True
            
    elif getCP(count) ==  lexi.CLASS or getCP(count) ==  lexi.INTERFACE or getCP(count) == lexi.END_MARKER:
            return True
    
    return False
#CHANGED
def methodSt(count):
    
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBody(count):
                if body(count):
                    return True
    return False

#CHANGED
def attributeSt(count):
    if decOrObjDec(count):
        if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
            return True
    return False


def staticOptional(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "STATIC":
        TM = getVP(count)
        data[TYPE_MODIFIER] = TM

        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE" or getCP(count) == "IDENTIFIER":
        return True
    return False

def paramBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1

        data[PARAMETER_LIST] = ""
        if insideParamBodyOrNull(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    return False


def insideParamBodyOrNull(count, data):
    if getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.IDENTIFIER:
        if insideParamBody(count,data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False

def insideParamBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        DT = getVP(count)
        if data[PARAMETER_LIST] == "":
            data[PARAMETER_LIST] = DT
        else:
            data[PARAMETER_LIST] += "," + DT
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBodyRecursive(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBodyRecursive(count, data):
                return True
    return False


###############FOLLOW NOT COMPLETE
def paramBodyRecursive(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if insideParamBody(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False



def lfParamBodyRecursive(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBodyRecursive(count):
                return True 
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBodyRecursive(count):
                return True
    return False


def body(count, body):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if mst(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False


def mst(count):
    if getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN or getCP(count) == lexi.IDENTIFIER:
        if sst(count):
            if mst(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False





#CHNAGED
def decOrObjDec(count):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count):
            return True
    elif getCP(count) == lexi.IDENTIFIER:
        if objectDec(count):
            return True
    return False

def dec(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        count+=1
        if arrayDec(count):
            if getCP(count) == lexi.IDENTIFIER:
                count+=1
                if init(count):
                    if list_(count):
                        if getCP(count) == lexi.END_OF_STATEMENT:
                            count+=1
                            return True
    return False

        

def init(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        count+=1
        if decOpt(count):
            return True
    elif getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False

def decOpt(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        data = {}
        if condition(count, data):
            return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN:
        count +=1
        if arrayBody(count):
            return True
    return False
    

def  initIdConst(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if init(count):
            return True
    elif getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        data = {}
        data[TYPE] = None
        if const(count, data):
            return True
    return False


def const(count, data, isRightOperand=False):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.INTEGER_CONST: 
        if isRightOperand:
            data[T_RIGHT] = "int"
        else:
            data[TYPE] = "int"

        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "STRING_CONST":
        if isRightOperand:
            data[T_RIGHT] = "text"
        else:
            data[TYPE] = "text"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "FLOAT_CONST":
        if isRightOperand:
            data[T_RIGHT] = "float"
        else:
            data[TYPE] = "float"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.BOOLEAN_CONSTANTS:
        if isRightOperand:
            data[T_RIGHT] = "boolean"
        else:
            data[TYPE] = "boolean"
        count+=1
        return True 
    return False



def objectDec(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if arrayDec(count):
            if getCP(count) == lexi.IDENTIFIER:
                count +=1
                if objectInit(count):
                    if objectList(count):
                        if getCP(count) == lexi.END_OF_STATEMENT:
                            count +=1
                            return True
    return False




#CHANGED
def objectInit(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        count+=1
        if lfObjectInit(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT":
        return True
    return False


#CHANGED
def lfObjectInit(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if argumentOrNull(count):
            if objFunctionArrayInvocationRecursive(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count+=1
        return True
    return False

def nt(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if argumentBody(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT":
        return True
    return False



def argumentBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        if insideArgumentBody(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    return False

def insideArgumentBody(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        data = {}
        if condition(count, data):
            data[PARAMETER_LIST] = data[DATA_TYPE]
            if argumentBodyRecursive(count, count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False







def argumentBodyRecursive(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if condition(count, data):
            data[PARAMETER_LIST] += "," + data[DATA_TYPE]
            if argumentBodyRecursive(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False


def condition(count, data, isRightOperand=False):
    if ae(count, data, isRightOperand):
        if condition_dash(count, data):
            return True
    return False


def condition_dash(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.BOOLEAN_OR:
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if ae(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if condition_dash(count, data):
                return True
    elif getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False

def ae(count, data, isRightOperand=False):
    if ROPE(count, data, isRightOperand):
        if ae_dash(count, data):
            return True
    return False


def ae_dash(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.BOOLEAN_AND:
        operator = getVP(count)
        count += 1
        data[T_RIGHT] = None
        if ROPE(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if ae_dash(count, data):
                return True
    elif getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False

def ROPE(count, data, isRightOperand=False):
    if e(count, data, isRightOperand):
        if ROPE_Dash(count, data):
            return True
    return False




def ROPE_Dash(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "RELATIONAL_OP":
        operator = getVP(count)
        count += 1
        data[T_RIGHT] = None
        if e(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if ROPE_Dash(count, data):
                return True
    elif getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False


def e(count, data, isRightOperand=False):
    if t(count, data, isRightOperand):
        if e_Dash(count, data):
            return True
    return False


def e_Dash(count, data):
    if getCP(count) == lexi.PM:
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if t(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if e_Dash(count, data):
                return True
    elif getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False

def t(count, data, isRightOperand=False):
    if f(count, data, isRightOperand):
        if t_Dash(count, data):
            return True
    return False


def t_Dash(count, data):
    if getCP(count) == lexi.MDM:
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if f(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if t_Dash(count, data):
                return True
    elif getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False




def f(count, data, isRightOperand=False):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        data = {}
        if condition(count, data, isRightOperand):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NOT":
        count+=1
        if f(count, data, isRightOperand):
            return True
    elif getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        if const(count, data, isRightOperand):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        data[TYPE] = None # remove after complting flf
        if f_Lf(count, data, isRightOperand):
            return True
    return False
        
        
        




def f_Lf(count, data, isRightOperand):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.SQUARE_BRACKET_OPEN  or getCP(count) == lexi.METHOD_OP  or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        if argumentOrNull(count):
            if objFunctionArrayInvocationRecursive(count):
                return True
    elif getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False






def mainFunction(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ACCESS_MODIFIERS":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "NONE":
            count+=1
            if tokenSet[count.value][lexi.CLASS_PART] == "MAIN":
                count+=1
                if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
                    count +=1
                    if mst(count):
                        #count+=1
                        if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                            count += 1                            
                            return True
    return False


def constructorSt(count, data):

    if tokenSet[count.value][lexi.CLASS_PART] == lexi.CONSTRUCTOR:
        count +=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            N = getVP(count)
            if N != data[CLASS_NAME]:
                print("Constructor Name Does Not Match The Current Class")
            count+=1

            scopeStack.createScope()
            if paramBody(count, data):
                if insertCDT(data[NAME], data[PARAMETER_LIST]+ARROW+data[CLASS_NAME],data[ACCESS_MODIFIER], None, data[CLASS_NAME] ):
                    print("Contructor Redeclaration Error")
                if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
                    count+=1
                    if constructorMst(count):
                        if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                            count+=1
                            return True
    return False

def interfaceSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.INTERFACE:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if inheritanceBody(count):
                if interfaceBody(count):
                    return True
    return False

def interfaceBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if interfaceMst(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False

def interfaceMst(count, data):
    if getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.STATIC or getCP(count) == lexi.IDENTIFIER:
        if staticOptional(count, data):
            if interfaceMethodSt(count, data):
                if interfaceMst(count, data):
                    return True
    elif getCP(count)  == lexi.CURLY_BRACKET_CLOSE:
        return True
    return False

def interfaceStRecursive(count):
    if getCP(count) == lexi.DATA_TYPE:
        if interfaceMethodSt(count):
            if interfaceStRecursive(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False

def interfaceMethodSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        DT = getVP(count)

        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            N = getVP(count)
            count+=1

            data[DATA_TYPE] = DT
            data[NAME] = N

            if paramBody(count, data):
                if not insertCDT(data[NAME], data[DATA_TYPE], None, data[TYPE_MODIFIER], data[CLASS_NAME]):
                    print("Method redeclaration Error at line: {}".format(getLine(count)))
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True

    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        DT = getVP(count)
        if lookUpDT(DT):
                print("Method redeclaration Error at line: {}".format(getLine(count)))
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            N = getVP(count)
            count+=1

            data[DATA_TYPE] = DT
            data[NAME] = N

            if paramBody(count, data):
                if not insertCDT(data[NAME], data[DATA_TYPE], None, data[TYPE_MODIFIER], data[CLASS_NAME]):
                    print("Method redeclaration Error at line: {}".format(getLine(count)))
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    return False


def objectList(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            if objectInit(count):
                if objectList(count):
                    return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        return True
    return False

def objFunctionArrayInvocation(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if argumentOrNull(count):
            if objFunctionArrayInvocationRecursive(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    return False



def argumentOrNull(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if argumentBody(count):
            if arrayCall(count):
                return True
    elif getCP(count) == lexi.SQUARE_BRACKET_OPEN:
        if arrayCall(count):
            return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.COMPOUND_AS_OP:
        return True
    return False





def objFunctionArrayInvocationRecursive(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "METHOD_OP":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if  argumentOrNull(count):
                if objFunctionArrayInvocationRecursive(count):
                    return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.COMPOUND_AS_OP:
        return True
    return False

def arrayCall(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_OPEN":
        count+=1
        data = {}
        if e(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_CLOSE":
                count+=1
                if arrayCall2d(count):
                    return True

    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False




def arrayCall2d(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_OPEN":
        count+=1
        data = {}
        if e(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_CLOSE":
                count+=1
                return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False



def ifElseSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IF":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            data = {}
            data[TYPE] = None
            if condition(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count):
                        if elif_(count):
                            if else_(count):
                                return True
    return False




def elif_(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ELIF":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            data = {}
            if condition(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count):
                        if elif_(count):
                            return True
    elif getCP(count) == lexi.ELSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN or getCP(count) == lexi.IDENTIFIER:
        return True
    return False






def else_(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ELSE":
        count+=1
        if body(count):
            return True
    elif getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN or getCP(count) == lexi.IDENTIFIER:
        return True
    return False



def forEachSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "FOREACH":
        count+=1
        if dtOrID(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
                count+=1
                if tokenSet[count.value][lexi.CLASS_PART] == "IN":
                    count+=1
                    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
                        count+=1
                        if body(count):
                            return True
    return False



def whileSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "WHILE":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            data = {}
            if condition(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count):
                        return True
    return False



def forSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "FOR":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            if forRule(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count):
                        return True
    return False

def forRule(count):
    if forDec(count):
        if forCondition(count):
            if forIncDec(count):
                return True
    return False



def forDec(count):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count):
            return True
    elif getCP(count) == lexi.IDENTIFIER:
        if asSt(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        count+=1
        return True
    return False



def forCondition(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        data = {}
        if condition(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
            count+=1
            return True
    return False


###############CHECK FOLLOW SET
def forIncDec(count):
    if getCP(count) == lexi.IDENTIFIER:
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if argumentOrNull(count):
                if objFunctionArrayInvocationRecursive(count):
                    if asOpOrCompound(count):
                        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False

def asSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if argumentOrNull(count):
            if objFunctionArrayInvocationRecursive(count):
                if asOpOrCompound(count):
                    if getCP(count) == lexi.END_OF_STATEMENT:
                        count+=1
                        return True
    return False


def asOpOrCompound(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        count += 1
        asStLf(count)
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.COMPOUND_AS_OP:
        count += 1
        asStLf(count)
        return True
    return False 


def asStLf(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        data = {}
        if condition(count, data):
            return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN:
        if arrayBody(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count += 1
        return True
    return False



def asStComplex(count):
    if argumentOrNull(count):
        if objFunctionArrayInvocationRecursive(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
                count+=1
                return True
    return False



def asStComplexOptions(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        data = {}
        if condition(count, data):
            return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN:
        if arrayBody(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count+=1
        return True
    return False


def arrayBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if onedOr2D(count):
            return True
    return False

def onedOr2D(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if arrayElements(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.SEPARATOR_OP:
        if arrayBody2d(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False

def arrayElements(count):
    data = {}
    if condition(count, data):
        if arraySeparator(count):
            return True
    return False

################CHECK FOLLOW SET
def arraySeparator(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        data = {}
        if condition(count, data):
            if arraySeparator(count):
              return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False 


##################CHECK FOLLOW SET
def arrayBody2d(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if arrayElements(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                if arraySeparator2d(count):
                    return True
    return False



#################CHECK FOLLOW SET
def arraySeparator2d(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if arrayBody2d(count):
            if arraySeparator2d(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False




def constructorMst(count):
    if constructorSst(count):
        if constructorMst(count):
            return True
    return False


def constructorSst(count):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count):
            return True
    elif getCP(count) == lexi.WHILE:
        if whileSt(count):
            return True
    elif getCP(count) == lexi.IF:
        if ifElseSt(count):
            return True
    elif getCP(count) == lexi.FOR:
        if forSt(count):
            return True
    elif getCP(count) == lexi.FOREACH:
        if forEachSt(count):
            return True
    elif getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN:
        if lfSst2(count):
            return True
    return False

def idConst(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
    elif getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        data = {}
        if const(count, data):
            return True
    return False

def lfSst2(count):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        count+=1
        if sstAllFunctions(count):
            return True
    return False


def sstAllFunctions(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if argumentBody(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count +=1
        if objectInit(count):
            if objectList(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN:
        if argumentOrNull(count):
            if objFunctionArrayInvocationRecursive(count):
                if asOpOrCompound(count):
                    if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                        count+=1
                        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT" or lexi.SEPARATOR_OP or getCP(count) == "ROUND_BRACKET_CLOSE" or getCP(count) == "IDENTIFIER" or getCP(count) == "CURLY_BRACKET_CLOSE" or getCP(count) == "DATA_TYPE" or getCP(count) == "WHILE" or getCP(count) == "IF" or getCP(count) == "FOR" or getCP(count) == "FOR_EACH" or getCP(count) == "SEND":
        return True
    return False


def sst(count):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count):
            return True
    elif getCP(count) == lexi.WHILE:
        if whileSt(count):
            return True
    elif getCP(count) == lexi.IF:
        if ifElseSt(count):
            return True
    elif getCP(count) == lexi.FOR:
        if forSt(count):
            return True
    elif getCP(count) == lexi.FOREACH:
        if forEachSt(count):
            return True
    elif getCP(count) == lexi.RETURN:
        if return_(count):
            return True
    elif getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN:
        if lfSst2(count):
            return True

    return False

def return_(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "SEND":
        count+=1
        if rValue(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                return True
    return False


###############CHECK FOLLOW SET FOR THIS###########
def rValue(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        data = {}
        if condition(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT": 
        return True
    return False




def list_(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count += 1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count += 1
            if init(count):
                if list_(count):
                    return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        return True
    return False




def arrayDec(count):
    if getCP(count) == lexi.SQUARE_BRACKET_OPEN:
        count+=1
        if getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
            count+=1
            if arrayDec2D(count):
                return True
    elif getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False

def arrayDec2D(count):
    if getCP(count) == lexi.SQUARE_BRACKET_OPEN:
        count +=1
        if getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
            count +=1
            return True
    elif getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False

def dtOrID(count):

    if getCP(count) == lexi.IDENTIFIER:
        count+=1
        return True
    elif getCP(count) == lexi.DATA_TYPE:
        count+=1
        return True

    return False






if __name__ == '__main__':
    main()
