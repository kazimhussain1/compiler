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
        

TYPE = "TYPE"
T_RIGHT = "T_RIGHT"

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
]
        

tokenSet = []

def getCP(count):
    return tokenSet[count.value][lexi.CLASS_PART]

def getVP(count):
    return tokenSet[count.value][lexi.VALUE_PART]

def checkCompat(type_left, type_right, operator):
    for item in compatibilityTable:
        if type_left == item.left and type_right == item.right and operator == item.op:
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





def inheritanceBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        if insideInheritanceBody(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    return False

#CHANGED
def insideInheritanceBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if inheritanceBodyRecursive(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False



def inheritanceBodyRecursive(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if inheritanceBodyRecursive(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False

def classSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "CLASS":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if inheritanceBody(count):
                if classBody(count):
                    return True
    return False

#CHANGED
def classBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if classBodySt(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False
##################FOLLOW SET NOT COMPLETE#################
def classBodySt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ACCESS_MODIFIERS":
        count+=1
        if methodAttrOrCons(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False


def methodAttrOrCons(count):
    if getCP(count) == lexi.STATIC or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.IDENTIFIER:
        if staticOptional(count):
            if classBodyStLf(count):
                return True
    elif getCP(count) == lexi.IDENTIFIER:
        count +=1
        if constructorSt(count):
            if classBodySt(count):
                return True

    return False

def classBodyStLf(count):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.DATA_TYPE:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            count+=1
            if classBodyStLfOne(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            count+=1
            if classBodyStLfTwo(count):
                return True
    return False

def classBodyStLfOne(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if paramBody(count):
            if body(count):
                if classBodySt(count):
                    return True
    elif getCP(count) == lexi.AS_OP or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        if init(count):
            if list_(count):
                if tokenSet[count.value][lexi.CLASS_PART] == lexi.END_OF_STATEMENT:  
                    count+=1
                    if classBodySt(count):
                        return True

    return False

def classBodyStLfTwo(count):
    if paramBody(count):
        if body(count):
            if classBodySt(count):
                return True
    elif objectInit(count):
        if objectList(count):
            if tokenSet[count.value][lexi.CLASS_PART] == lexi.END_OF_STATEMENT:
                count+=1  
                if classBodySt(count):
                    return True

    return False

#changed
def classStRecursive(count):
    if getCP(count) == lexi.CLASS:
        if classSt(count):
            if classStRecursive(count):
                return True

    elif getCP(count) == lexi.INTERFACE:      
        if interfaceSt(count):
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


def staticOptional(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "STATIC":
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE" or getCP(count) == "IDENTIFIER":
        return True
    return False

def paramBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        if insideParamBodyOrNull(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    return False


def insideParamBodyOrNull(count):
    if getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.IDENTIFIER:
        if insideParamBody(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False

def insideParamBody(count):
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


###############FOLLOW NOT COMPLETE
def paramBodyRecursive(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if insideParamBody(count):
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


def body(count):
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

        

def init(count):
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
        if const(count):
            return True
    return False


def const(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.INTEGER_CONST: 
        data[TYPE] = "int"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "STRING_CONST":
        data[TYPE] = "text"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "FLOAT_CONST":
        data[TYPE] = "float"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.BOOLEAN_CONSTANTS:
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
def objectInit(count):
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



def argumentBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        if insideArgumentBody(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    return False

def insideArgumentBody(count):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        data = {}
        if condition(count, data):
            if argumentBodyRecursive(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False







def argumentBodyRecursive(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        data = {}
        if condition(count, data):
            if argumentBodyRecursive(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False


def condition(count, data):
    if ae(count, data):
        if condition_dash(count, data):
            return True
    return False




def condition_dash(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "OR":
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if ae(count, data):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if condition_dash(count, data):
                return True
    elif getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False

def ae(count, data):
    if ROPE(count, data):
        if ae_dash(count, data):
            return True
    return False

def ROPE(count, data):
    if e(count, data):
        if ROPE_Dash(count, data):
            return True
    return False


def e(count, data):
    if t(count, data):
        if e_Dash(count, data):
            return True
    return False

def t(count, data):
    if f(count, data):
        if t_Dash(count, data):
            return True
    return False

def e_Dash(count, data):
    if getCP(count) == lexi.PM:
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if t(count, data):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if e_Dash(count, data):
                return True
    elif getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False




def t_Dash(count, data):
    if getCP(count) == lexi.MDM:
        operator = getVP.count
        count+=1
        data[T_RIGHT] = None
        if f(count, data):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if t_Dash(count, data):
                return True
    elif getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False




def mdm(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "*":
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "/":
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "%":
        count+=1
        return True
    return False

def f(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        data = {}
        if condition(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NOT":
        count+=1
        if f(count, data):
            return True
    elif getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        if const(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if f_Lf(count, data):
            return True
    return False
        
        
        




def f_Lf(count, data):
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


def constructorSt(count):

    if tokenSet[count.value][lexi.CLASS_PART] == lexi.CONSTRUCTOR:
        count +=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBody(count):
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

def interfaceBody(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if interfaceMst(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False

def interfaceMst(count):
    if getCP(count) == lexi.DATA_TYPE:
        if interfaceMethodSt(count):
            if interfaceMst(count):
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

def interfaceMethodSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDNETIFIER":
            count+=1
            if paramBody(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    return False

################FOLLOW NOT COMPLETE
def objectList(count):
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
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
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
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
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
    elif getCP(count) == lexi.ELSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.SEND or getCP(count) == lexi.IDENTIFIER:
        return True
    return False






def else_(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ELSE":
        count+=1
        if body(count):
            return True
    elif getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.SEND or getCP(count) == lexi.IDENTIFIER:
        return True
    return False



def forEachSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "FOREACH":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
            count+=1
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
        if asSt(count):
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
                    if asStLf(count):
                        return True
    return False


def asOpOrCompound(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        count += 1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count += 1
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
        if const(count):
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




def list_(count):
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





def ROPE_Dash(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "RELATIONAL_OP":
        operator = getVP(count)
        count += 1
        data[T_RIGHT] = None
        if e(count, data):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if ROPE_Dash(count, data):
                return True
    elif getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False


def ae_dash(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "AND":
        operator = getVP(count)
        count += 1
        data[T_RIGHT] = None
        if ROPE(count, count):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            if data[TYPE] == None:
                print("Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]))
            if ae_dash(count, count):
                return True
    elif getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
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






if __name__ == '__main__':
    main()
