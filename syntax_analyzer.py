import lexical_analyzer as lexi
from classes import *
import sys
import time
import os

from sty import fg


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
TEMP_VAR = "TEMP_VAR"
TEMP_LABEL = "TEMP_LABEL"




compatibilityTable = [

    ########### INT #####################

    compatEntity("int", "int", "+", "int"),
    compatEntity("int", "int", "-", "int"),
    compatEntity("int", "int", "*", "int"),
    compatEntity("int", "int", "/", "int"),
    compatEntity("int", "int", "=", "int"),
    compatEntity("int", "int", "AND", "boolean"),
    compatEntity("int", "int", "and", "boolean"),
    compatEntity("int", "int", "OR", "boolean"),
    compatEntity("int", "int", "or", "boolean"),
    compatEntity("int", None, "not", "boolean"),
    compatEntity("int", "int", "<", "boolean"),
    compatEntity("int", "int", ">", "boolean"),
    compatEntity("int", "int", "==", "boolean"),
    compatEntity("int", "int", "!=", "boolean"),
    compatEntity("int", "int", "<=", "boolean"),
    compatEntity("int", "int", ">=", "boolean"),
    compatEntity("int", "int", "+=", "int"),
    compatEntity("int", "int", "-=", "int"),
    compatEntity("int", "int", "*=", "int"),
    compatEntity("int", "int", "/=", "int"),

    

    ########### FLOAT #####################

    compatEntity("float", "float", "+", "float"),
    compatEntity("float", "float", "-", "float"),
    compatEntity("float", "float", "*", "float"),
    compatEntity("float", "float", "/", "float"),
    compatEntity("float", "float", "=", "float"),
    compatEntity("float", "float", "AND", "boolean"),
    compatEntity("float", "float", "and", "boolean"),
    compatEntity("float", "float", "OR", "boolean"),
    compatEntity("float", "float", "or", "boolean"),
    compatEntity("float", None, "not", "boolean"),
    compatEntity("float", "float", "<", "boolean"),
    compatEntity("float", "float", ">", "boolean"),
    compatEntity("float", "float", "==", "boolean"),
    compatEntity("float", "float", "!=", "boolean"),
    compatEntity("float", "float", "<=", "boolean"),
    compatEntity("float", "float", ">=", "boolean"),
    compatEntity("float", "float", "+=", "float"),
    compatEntity("float", "float", "-=", "float"),
    compatEntity("float", "float", "*=", "float"),
    compatEntity("float", "float", "/=", "float"),


    ########### BOOLEAN #####################

    compatEntity("boolean", "boolean", "AND", "boolean"),
    compatEntity("boolean", "boolean", "and", "boolean"),
    compatEntity("boolean", "boolean", "OR", "boolean"),
    compatEntity("boolean", "boolean", "or", "boolean"),
    compatEntity("boolean", "boolean", "=", "boolean"),
    compatEntity("boolean", None, "not", "boolean"),

    #########Cross Comptibility Check ###########
    
    #### INT-FLOAT####
    
    compatEntity("int", "float", "AND", "float"),
    compatEntity("int", "float", "and", "float"),
    compatEntity("int", "float", "OR", "float"),
    compatEntity("int", "float", "or", "float"),
    compatEntity("int", "float", "+", "float"),
    compatEntity("int", "float", "-", "float"),
    compatEntity("int", "float", "*", "float"),
    compatEntity("int", "float", "/", "float"),
    compatEntity("int", "float", "=", "int"),
    compatEntity("int", "float", "<", "boolean"),
    compatEntity("int", "float", ">", "boolean"),
    compatEntity("int", "float", "==", "boolean"),
    compatEntity("int", "float", "!=", "boolean"),
    compatEntity("int", "float", "<=", "boolean"),
    compatEntity("int", "float", ">=", "boolean"),
    compatEntity("int", "float", "+=", "int"),
    compatEntity("int", "float", "-=", "int"),
    compatEntity("int", "float", "*=", "int"),
    compatEntity("int", "float", "/=", "int"),

    ###### FLOAT INT ######

    compatEntity("float", "int", "+", "float"),
    compatEntity("float", "int", "-", "float"),
    compatEntity("float", "int", "*", "float"),
    compatEntity("float", "int", "/", "float"),
    compatEntity("float", "int", "=", "float"),
    compatEntity("float", "int", "AND", "float"),
    compatEntity("float", "int", "and", "float"),
    compatEntity("float", "int", "OR", "float"),
    compatEntity("float", "int", "or", "float"),
    compatEntity("float", "int", "<", "boolean"),
    compatEntity("float", "int", ">", "boolean"),
    compatEntity("float", "int", "==", "boolean"),
    compatEntity("float", "int", "!=", "boolean"),
    compatEntity("float", "int", "<=", "boolean"),
    compatEntity("float", "int", ">=", "boolean"),
    compatEntity("float", "int", "+=", "float"),
    compatEntity("float", "int", "-=", "float"),
    compatEntity("float", "int", "*=", "float"),
    compatEntity("float", "int", "/=", "float"),

    ##### TEXT #####

    compatEntity("text", "text", "=", "text"),
    compatEntity("text", "text", "==", "boolean"),
    compatEntity("text", "text", "!=", "boolean"),
]

scopeTable = []
defTable = []
tokenSet = []


scopeStack = Stack()




def lookUpST(N, CDT):
    for i in range(len(scopeTable)-1, -1, -1):
        if scopeTable[i].name == N:
            return scopeTable[i].type_

    for item in CDT:
        if item.name == N:
            return item.type_

    return None

def lookUpSTSingleScope(N):
    currScope = scopeStack.peek()
    for item in scopeTable:
        if item.name == N and item.scope == currScope:
            return item.type_
        
    return None



def insertST(N, T):
    if lookUpSTSingleScope(N) == None:
        scopeTable.append(scopeEntity(N, T, scopeStack.peek()))
        return True
    return False

def lookUpDT(N):
    for item in defTable:
        if N == item.name:
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

            isOldFunc = ARROW in item.type_
            isNewFunc = ARROW in T 

            if isOldFunc and isNewFunc:

                pListAndRTypeOld = item.type_.split(ARROW)
                pListAndRTypeNew = T.split(ARROW)
                if pListAndRTypeOld[0] == pListAndRTypeNew[0]:
                    return {R_Type:item.type_.split(ARROW)[1], ACCESS_MODIFIER:item.AM, TYPE_MODIFIER:item.TM}
                else:
                    return None

            else:
                return None

    return None

def lookUpCDTfromDT(N, T, DTname):
    for item in defTable:
        if item.name == DTname:
            for thing in item.CDT:
                if thing.name == N:
                    if ARROW in thing.type_:
                        return {R_Type:thing.type_.split(ARROW)[1], ACCESS_MODIFIER:thing.AM, TYPE_MODIFIER:thing.TM}
                    else:
                        return {R_Type:thing.type_, ACCESS_MODIFIER:thing.AM, TYPE_MODIFIER:thing.TM}
    return None

def insertCDT(N, T, AM, TM, CDT):
    if lookUpCDT(N, T, CDT) == None:
        CDT.append(CDTEntity(N, T, AM, TM))    
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

ICG_file = None
label_no = 0
temp_count = 0

def create_label():
    global label_no
    return "L"+ str(label_no) +":"

def use_label():
    global label_no
    return "L"+ str(label_no)

def temp_var():
    global temp_count
    return "t"+ str(temp_count)

def inc_temp():
    global temp_count
    temp_count+=1

def dec_temp():
    global temp_count
    temp_count-=1

def main():
    count = Integer()
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
        global tokenSet
        tokenSet = lexi.lexicalAnalyzer(filePath)
        print("")
        if getCP(count) == lexi.CLASS or getCP(count) == lexi.INTERFACE or getCP(count) == lexi.IMPORT:
            global ICG_file
            ICG_file = open(file = "output.icg", mode = "wt")
            if start(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "$":
                    print ("Successful Parsed")
                    time.sleep(1)
                    os.system('cls')
#                     print(r'''
#          .* *.               `o`o`
#          *. .*              o`o`o`o      ^,^,^
#            * \               `o`o`     ^,^,^,^,^
#               \     ***        |       ^,^,^,^,^
#                \   *****       |        /^,^,^
#                 \   ***        |       /
#     ~@~*~@~      \   \         |      /
#   ~*~@~*~@~*~     \   \        |     /
#   ~*~@smd@~*~      \   \       |    /     #$#$#        .`'.;.
#   ~*~@~*~@~*~       \   \      |   /     #$#$#$#   00  .`,.',
#     ~@~*~@~ \        \   \     |  /      /#$#$#   /|||  `.,'
# _____________\________\___\____|_/______/_________|\/\___||______
#                 ''')

#                 time.sleep(1)
#                 os.system('cls')
#                 print(r'''
#                                    .''.       
#        .''.      .        *''*    :_\/_:     . 
#       :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.
#   .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-
#  :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'
#  : /\ : :::::     *_\/_*     -= o =-  /)\    '  *
#   '..'  ':::'     * /\ *     .'/.\'.   '
#       *            *..*         :
#         *
#         *            Success

                        
#                 ''')

                print(fg.green, "Syntax successfully parsed", fg.rs, sep = '')

                return True
        print(fg.red, "error at line {} : {}".format(tokenSet[count.value][lexi.LINE_NUMBER], tokenSet[count.value][lexi.VALUE_PART]),fg.rs, sep = '')
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
        exist = lookUpDT(N)

        if not exist: #use data dictionary to print class or interface struct
            print(fg.red, "Unknown Identifier at line: {}".format(getLine(count)), fg.rs, sep = '')

        
        data[PARAMETER_LIST] = N

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
            N = getVP(count)
            exist = lookUpDT(N)

            if not exist:
                print(fg.red, "Unknown Identifier at line: {}".format(getLine(count)), fg.rs, sep = '')

        
            data[PARAMETER_LIST] += "," + N
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
               print(fg.red, "Redeclaration Error at line: {}", getLine(count), fg.rs, sep = '')

            count+=1
            if inheritanceBody(count, data):
                CDT = insertDT(CN, lexi.CLASS, data[PARAMETER_LIST])
                data[CLASS_DATA_TABLE] = CDT
                data[CLASS_NAME] = CN
                if classBody(count, data):
                    if not lookUpCDT(CN,"",CDT):
                        insertCDT(CN,ARROW+CN,"public", None,CDT)
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
    elif getCP(count) == lexi.CONSTRUCTOR:
        if constructorSt(count, data):
            if classBodySt(count, data):
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
        if lookUpDT(DT) == None:
           print(fg.red, "{} not declared at line: {}".format(getVP(count), getLine(count)), fg.rs, sep = '')

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
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if paramBody(count, data):
            if not insertCDT(data[NAME], data[PARAMETER_LIST]+ARROW+data[DATA_TYPE], data[ACCESS_MODIFIER], data[TYPE_MODIFIER], data[CLASS_DATA_TABLE]):
               print(fg.red, "Function Redeclaration Error at line: {}".format(getLine(count)), fg.rs, sep = '')
            if body(count, data):
                scopeStack.deleteScope()
                if classBodySt(count, data):
                    return True
    elif getCP(count) == lexi.AS_OP or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        insertCDT(data[NAME], data[DATA_TYPE], data[ACCESS_MODIFIER], data[TYPE_MODIFIER], data[CLASS_DATA_TABLE])
        if init(count, data):
            if list_(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == lexi.END_OF_STATEMENT:  
                    count+=1
                    if classBodySt(count, data):
                        return True

    return False

def classBodyStLfTwo(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if paramBody(count, data):
            if not insertCDT(data[NAME], data[PARAMETER_LIST], data[ACCESS_MODIFIER], data[TYPE_MODIFIER],data[CLASS_DATA_TABLE]):
                print(fg.red, "Function Redeclaration Error at line: {}".format(getLine(count)), fg.rs, sep = '')
            if body(count, data):
                scopeStack.deleteScope()
                if classBodySt(count, data):
                    return True
    elif getCP(count) == lexi.AS_OP or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        insertCDT(data[NAME], data[DATA_TYPE], data[ACCESS_MODIFIER], data[TYPE_MODIFIER], data[CLASS_DATA_TABLE])
        if objectInit(count,data):
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
def methodSt(count, data):
    
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if paramBody(count, data):
                if body(count, data):
                    return True
    return False

#CHANGED
def attributeSt(count, data):
    if decOrObjDec(count, data):
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
        data[TYPE_MODIFIER] = None
        return True
    return False

def paramBody(count, data):
    scopeStack.createScope()
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

#insert in scope tabel
def insideParamBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        DT = getVP(count)
        if data[PARAMETER_LIST] == "":
            data[PARAMETER_LIST] = DT
        else:
            data[PARAMETER_LIST] += "," + DT
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            N =getVP(count)
            insertST(N, DT)
            count+=1
            if paramBodyRecursive(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        
        DT = getVP(count)
        if data[PARAMETER_LIST] == "":
            data[PARAMETER_LIST] = DT
        else:
            data[PARAMETER_LIST] += "," + DT

        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            N = getVP(count)
            insertST(N, DT)
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



# def lfParamBodyRecursive(count):
#     if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
#         count+=1
#         if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
#             count+=1
#             if paramBodyRecursive(count):
#                 return True 
#     elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
#         count+=1
#         if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
#             count+=1
#             if paramBodyRecursive(count):
#                 return True
#     return False


def body(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if mst(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False


def mst(count, data):
    if getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN or getCP(count) == lexi.IDENTIFIER:
        if sst(count, data):
            if mst(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False





#CHNAGED
def decOrObjDec(count, data):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count, data):
            return True
    elif getCP(count) == lexi.IDENTIFIER:
        if objectDec(count, data):
            return True
    return False

def dec(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        data[DATA_TYPE] = getVP(count)
        count+=1
        if arrayDec(count, data):
            if getCP(count) == lexi.IDENTIFIER:
                N = getVP(count)
                data[NAME] = N
                if not insertST(N, data[DATA_TYPE]):
                    print(fg.red, "Redeclaration Error '{}' at line: {}".format(N, getLine(count)), fg.rs, sep = '')
                count+=1
                if init(count,data):
                    if list_(count, data):
                        if getCP(count) == lexi.END_OF_STATEMENT:
                            count+=1
                            return True
    return False

        

def init(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        O = getVP(count)
        count+=1
        if decOpt(count, data):
            ICG_file.write(temp_var() + " = " + data[TEMP_VAR] + "\n")
            T = checkCompat(data[DATA_TYPE], data[TYPE], O)
            if data[DATA_TYPE] != T:
                print(fg.red, "Cannot assign '{}' to variable of type '{}' at Line: {}".format(data[TYPE], data[DATA_TYPE], getLine(count)), fg.rs, sep = '')
            return True
    elif getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False

def decOpt(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        if condition(count, data):
            return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN:
        count +=1
        if arrayBody(count, data):
            return True
    return False
    


def const(count, data, isRightOperand=False):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.INTEGER_CONST: 
        ICG_file.write(temp_var() + " = " + getVP(count) + "\n")
        data[TEMP_VAR] = temp_var()
        inc_temp()
        if isRightOperand:
            data[T_RIGHT] = "int"
        else:
            data[TYPE] = "int"

        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "STRING_CONST":
        ICG_file.write(temp_var() + " = " + getVP(count) + "\n")
        data[TEMP_VAR] = temp_var()
        inc_temp()
        if isRightOperand:
            data[T_RIGHT] = "text"
        else:
            data[TYPE] = "text"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "FLOAT_CONST":
        ICG_file.write(temp_var() + " = " + getVP(count) + "\n")
        data[TEMP_VAR] = temp_var()
        inc_temp()
        if isRightOperand:
            data[T_RIGHT] = "float"
        else:
            data[TYPE] = "float"
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.BOOLEAN_CONSTANTS:
        ICG_file.write(temp_var() + " = " + getVP(count) + "\n")
        data[TEMP_VAR] = temp_var()
        inc_temp()
        if isRightOperand:
            data[T_RIGHT] = "boolean"
        else:
            data[TYPE] = "boolean"
        count+=1
        return True 
    return False



def objectDec(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if arrayDec(count, data):
            if getCP(count) == lexi.IDENTIFIER:
                count +=1
                if objectInit(count, data):
                    if objectList(count, data):
                        if getCP(count) == lexi.END_OF_STATEMENT:
                            count +=1
                            return True
    return False




#CHANGED
def objectInit(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        count+=1
        if lfObjectInit(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT":
        return True
    return False


#CHANGED
def lfObjectInit(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        data[NAME] = getVP(count)
        count+=1
        if argumentOrNull(count, data):
            if objFunctionArrayInvocationRecursive(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count+=1
        return True
    return False

# def nt(count):
#     if getCP(count) == lexi.ROUND_BRACKET_OPEN:
#         if argumentBody(count):
#             return True
#     elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT":
#         return True
#     return False



def argumentBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        if insideArgumentBody(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE": 
                # if lookUpCDT(data[NAME], data[PARAMETER_LIST], data[CLASS_DATA_TABLE])== None:
                #    print(fg.red, "{} not declared at line: {}".format(data[NAME], getLine(count)))
                count+=1
                return True
    return False

def insideArgumentBody(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        
        if condition(count, data):
            data[PARAMETER_LIST] = data[TYPE]
            if argumentBodyRecursive(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False







def argumentBodyRecursive(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if condition(count, data):
            data[PARAMETER_LIST] += "," + data[TYPE]
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
        temp = data[TEMP_VAR]
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if ae(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            ICG_file.write(temp_var() + " = " + temp + " " + operator + " " + data[TEMP_VAR] + "\n")
            data[TEMP_VAR] = temp_var()
            inc_temp()
            if data[TYPE] == None:
               print(fg.red, "Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]), fg.rs, sep = '')
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
        temp = data[TEMP_VAR]
        operator = getVP(count)
        count += 1
        data[T_RIGHT] = None
        if ROPE(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            ICG_file.write(temp_var() + " = " + temp + " " + operator + " " + data[TEMP_VAR] + "\n")
            data[TEMP_VAR] = temp_var()
            inc_temp()
            if data[TYPE] == None:
               print(fg.red, "Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]), fg.rs, sep = '')
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
        temp = data[TEMP_VAR]
        operator = getVP(count)
        count += 1
        data[T_RIGHT] = None
        if e(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            ICG_file.write(temp_var() + " = " + temp + " " + operator + " " + data[TEMP_VAR] + "\n")
            data[TEMP_VAR] = temp_var()
            inc_temp()
            if data[TYPE] == None:
               print(fg.red, "Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]), fg.rs, sep = '')
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
        temp = data[TEMP_VAR]
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if t(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            ICG_file.write(temp_var() + " = " + temp + " " + operator + " " + data[TEMP_VAR] + "\n")
            data[TEMP_VAR] = temp_var()
            inc_temp()
            if data[TYPE] == None:
               print(fg.red, "Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]), fg.rs, sep = '')
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
        temp = data[TEMP_VAR]
        operator = getVP(count)
        count+=1
        data[T_RIGHT] = None
        if f(count, data, True):
            data[TYPE] = checkCompat(data[TYPE], data[T_RIGHT], operator)
            ICG_file.write(temp_var() + " = " + temp + " " + operator + " " + data[TEMP_VAR] + "\n")
            data[TEMP_VAR] = temp_var()
            inc_temp()
            if data[TYPE] == None:
               print(fg.red, "Type Mismatch Error at Line:{}".format(tokenSet[count.value][lexi.LINE_NUMBER]), fg.rs, sep = '')
            if t_Dash(count, data):
                return True
    elif getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False




def f(count, data, isRightOperand=False):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        
        if condition(count, data, isRightOperand):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NOT":
        count+=1
        if f(count, data, isRightOperand):
            ICG_file.write(temp_var() + " = " + data[TEMP_VAR] + "\n")
            data[TEMP_VAR] = temp_var()
            inc_temp()
            return True
    elif getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS:
        if const(count, data, isRightOperand):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        data[NAME] = getVP(count)
        count+=1
        if f_Lf(count, data, isRightOperand):
            return True
    return False
        
        
        




def f_Lf(count, data, isRightOperand):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.SQUARE_BRACKET_OPEN  or getCP(count) == lexi.METHOD_OP  or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        if argumentOrNull(count, data, isRightOperand = isRightOperand):
            if objFunctionArrayInvocationRecursive(count, data, isRightOperand = isRightOperand):
                return True
    elif getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
        return True
    return False






def mainFunction(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ACCESS_MODIFIERS":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "NONE":
            count+=1
            if tokenSet[count.value][lexi.CLASS_PART] == "MAIN":
                count+=1
                if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
                    count +=1
                    if mst(count, data):
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
               print(fg.red, "Constructor Name '{}' Does Not Match The Current Class Name '{}' at line: {}".format(N, data[CLASS_NAME], getLine(count)), fg.rs, sep = '')
            count+=1

            if paramBody(count, data):
                if not insertCDT(N, data[PARAMETER_LIST]+ARROW+data[CLASS_NAME],data[ACCESS_MODIFIER], lexi.CONSTRUCTOR, data[CLASS_DATA_TABLE] ):
                   print(fg.red, "Contructor Redeclaration Error at line: {}".format(getLine(count)), fg.rs, sep = '')
                if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
                    count+=1
                    if constructorMst(count, data):

                        scopeStack.deleteScope()
                        if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                            count+=1
                            return True
    return False

def interfaceSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.INTERFACE:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if inheritanceBody(count, data):
                if interfaceBody(count, data):
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

def interfaceStRecursive(count, data):
    if getCP(count) == lexi.DATA_TYPE:
        if interfaceMethodSt(count, data):
            if interfaceStRecursive(count, data):
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
                   print(fg.red, "Method redeclaration Error at line: {}".format(getLine(count)), fg.rs, sep = '')
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True

    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        DT = getVP(count)
        if lookUpDT(DT):
               print(fg.red, "Method redeclaration Error at line: {}".format(getLine(count)), fg.rs, sep = '')
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
            N = getVP(count)
            count+=1

            data[DATA_TYPE] = DT
            data[NAME] = N

            if paramBody(count, data):
                if not insertCDT(data[NAME], data[DATA_TYPE], None, data[TYPE_MODIFIER], data[CLASS_NAME]):
                   print(fg.red, "Method redeclaration Error at line: {}".format(getLine(count)), fg.rs, sep = '')
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    return False


def objectList(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            if objectInit(count, data):
                if objectList(count, data):
                    return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        return True
    return False

# def objFunctionArrayInvocation(count, data):
#     if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
#         count+=1
#         if argumentOrNull(count, data):
#             if objFunctionArrayInvocationRecursive(count, data):
#                 if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
#                     count+=1
#                     return True
#     return False



def argumentOrNull(count, data, lookUpFromDT = False, isRightOperand = False):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if argumentBody(count, data):

            if lookUpFromDT:
                returnType = lookUpCDTfromDT(data[NAME], data[PARAMETER_LIST], data[TYPE])
            else:
                returnType = lookUpCDT(data[NAME], data[PARAMETER_LIST], data[CLASS_DATA_TABLE])
            if returnType:
                if isRightOperand:
                    data[T_RIGHT] = returnType[R_Type]
                else:
                    data[TYPE] = returnType[R_Type]
            else:
                returnType = lookUpCDTfromDT(data[NAME], data[PARAMETER_LIST], data[NAME])
                if returnType:
                    if isRightOperand:
                        data[T_RIGHT] = returnType[R_Type]
                    else:
                        data[TYPE] = returnType[R_Type]
                else:
                    if isRightOperand:
                        data[T_RIGHT] = ""
                    else:
                        data[TYPE] = ""


            if not returnType:
               print(fg.red, "{} not declared at line: {}".format(data[NAME], getLine(count)), fg.rs, sep = '')
            elif returnType[ACCESS_MODIFIER] != "public":
               print(fg.red, "Cannot access {} method '{}' of class '{}' at line: {}".format(returnType[ACCESS_MODIFIER], data[NAME],data[DATA_TYPE], getLine(count)), fg.rs, sep = '')
            if arrayCall(count, data):
                return True
    elif getCP(count) == lexi.SQUARE_BRACKET_OPEN:
        if arrayCall(count, data):
            return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.COMPOUND_AS_OP:
        if lookUpFromDT:
            if isRightOperand:
                DT = lookUpCDTfromDT(data[NAME], "", data[T_RIGHT])
            else:
                DT = lookUpCDTfromDT(data[NAME], "", data[DATA_TYPE])
            if DT != None:
                if DT[ACCESS_MODIFIER] != "public":
                    print(fg.red, "Cannot access {} method '{}' of class '{}' at line: {}".format(DT[ACCESS_MODIFIER], data[NAME],data[DATA_TYPE], getLine(count)), fg.rs, sep = '')
                if isRightOperand:
                    data[T_RIGHT] = DT[R_Type]
                else:
                    data[TYPE] = DT[R_Type]

            else:
                if isRightOperand:
                    data[T_RIGHT] = DT
                else:
                    data[TYPE] = DT

        else:
            DT = lookUpST(data[NAME], data[CLASS_DATA_TABLE])

            if isRightOperand:
                data[T_RIGHT] = DT
            else:
                data[TYPE] = DT
        
        if DT == None:
            print(fg.red, "{} not declared at line: {}".format(data[NAME], getLine(count)), fg.rs, sep = '')
        return True
    return False





def objFunctionArrayInvocationRecursive(count, data, isRightOperand = False):
    if tokenSet[count.value][lexi.CLASS_PART] == "METHOD_OP":
        if isRightOperand:
            T = data[T_RIGHT]
        else:
            T = data[TYPE]
        if T == "int" or T == "float" or T == "text" or T == "boolean":
           print(fg.red, "primitive data type cannot use '.' operator at line: {}".format(getLine(count)), fg.rs, sep = '')
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            data[NAME] = getVP(count)

            count+=1
            if  argumentOrNull(count, data, lookUpFromDT = True, isRightOperand = isRightOperand):
                if objFunctionArrayInvocationRecursive(count, data, isRightOperand = isRightOperand):
                    return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.COMPOUND_AS_OP:
        return True
    return False

def arrayCall(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_OPEN":
        count+=1
        
        if e(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_CLOSE":
                count+=1
                if arrayCall2d(count, data):
                    return True

    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False




def arrayCall2d(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_OPEN":
        count+=1
        
        if e(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_CLOSE":
                count+=1
                return True
    elif getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        return True
    return False



def ifElseSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "IF":
        count+=1
        scopeStack.createScope()
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            
            if condition(count, data):
                ICG_file.write("if("+ data[TEMP_VAR] +" == false) jmp " + use_label() + "\n")
                if data[TYPE] != "boolean":
                   print(fg.red, "Expression should return boolean type at line: {}".format(getLine(count)), fg.rs, sep = '')

                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count, data):
                        global label_no
                        label_no+=1
                        temp = use_label()
                        data[TEMP_LABEL] = temp
                        ICG_file.write("jmp " + temp + "\n")
                        label_no-=1
                        ICG_file.write(create_label() + "\n")
                        label_no+=1
                        scopeStack.deleteScope()
                        if elif_(count, data):
                            
                            if else_(count, data):

                                ICG_file.write(temp + ":" + "\n")

                                return True


    return False




def elif_(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ELIF":
        count+=1

        scopeStack.createScope()
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            
            if condition(count, data):

                ICG_file.write("if(" + data[TEMP_VAR] + " == false) jmp " + use_label() + "\n")

                if data[TYPE] != "boolean":
                   print(fg.red, "Expression should return boolean type at line: {}".format(getLine(count)), fg.rs, sep = '')

                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count, data):
                        global label_no
                        ICG_file.write("jmp " + data[TEMP_LABEL] + "\n")
                        ICG_file.write(create_label() + "\n")
                        label_no+=1
                        scopeStack.deleteScope()
                        if elif_(count, data):
                            return True
    elif getCP(count) == lexi.ELSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN or getCP(count) == lexi.IDENTIFIER:
        return True
    return False






def else_(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "ELSE":
        count+=1
        scopeStack.createScope()
        if body(count, data):
            scopeStack.deleteScope()
            return True
    elif getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN or getCP(count) == lexi.IDENTIFIER:
        return True
    return False



def forEachSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "FOREACH":
        count+=1
        scopeStack.createScope()
        if dtOrID(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
                N=getVP(count)
                count+=1
                if not insertST(N, data[DATA_TYPE]):
                   print(fg.red, "Redeclaration err {}".format(getLine(count)), fg.rs, sep = '')
                if tokenSet[count.value][lexi.CLASS_PART] == "IN":
                    count+=1
                    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
                        N = getVP(count)
                        DT = lookUpST(N, data[CLASS_DATA_TABLE])
                        if DT == None:
                           print(fg.red, "Unknown identifier found at line : {}".format(getLine(count)), fg.rs, sep = '')
                        count+=1
                        if body(count, data):
                            scopeStack.deleteScope()
                            return True
    return False



def whileSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "WHILE":

        global label_no
        ICG_file.write(create_label() + "\n")
        label_no+=1

        count+=1
        scopeStack.createScope()
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            
            if condition(count, data):
                ICG_file.write("if("+ data[TEMP_VAR] +" == false) jmp " + use_label() + "\n")
                
                if data[TYPE] != "boolean":
                   print(fg.red, "Expression should return boolean type at line: {}".format(getLine(count)), fg.rs, sep = '')

                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count, data):
                        label_no-=1
                        ICG_file.write("jmp " + use_label() + "\n")
                        label_no+=1
                        ICG_file.write(create_label() + "\n")
                        label_no+=1
                        scopeStack.deleteScope()
                        return True
    return False



def forSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "FOR":
        count+=1
        scopeStack.createScope()
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            if forRule(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count, data):
                        global label_no
                        label_no-=1
                        ICG_file.write("jmp " + use_label() + "\n")
                        label_no+=1
                        ICG_file.write(create_label() + "\n")
                        label_no+=1
                        scopeStack.deleteScope()
                        return True
    return False

def forRule(count, data):
    if forDec(count, data):
        ICG_file.write(create_label() + "\n")
        global label_no
        label_no+=1
        if forCondition(count, data):
            ICG_file.write("if("+ data[TEMP_VAR] +" == false) jmp " + use_label() + "\n")
            if forIncDec(count, data):
                return True
    return False



#write attributed grammer
def forDec(count, data):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count, data):
            return True
    elif getCP(count) == lexi.IDENTIFIER:
        if asSt(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        count+=1
        return True
    return False



def forCondition(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        if condition(count, data):
            if data[TYPE] != "boolean":
               print(fg.red, "Expression should return boolean type at line: {}".format(getLine(count)), fg.rs, sep = '')
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
            count+=1
            return True
    return False


###############CHECK FOLLOW SET
def forIncDec(count, data):
    if getCP(count) == lexi.IDENTIFIER:
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if argumentOrNull(count, data):
                if objFunctionArrayInvocationRecursive(count, data):
                    if asOpOrCompound(count, data):
                        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False

def asSt(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        N = getVP(count)
        count+=1

        data[NAME] = N
        if argumentOrNull(count, data):
            if objFunctionArrayInvocationRecursive(count, data):
                print(data[DATA_TYPE], data[TYPE])
                if asOpOrCompound(count, data):
                    if getCP(count) == lexi.END_OF_STATEMENT:
                        count+=1
                        return True
    return False


def asOpOrCompound(count, data):
    if getCP(count) == lexi.AS_OP:
        count += 1
        if asStLf(count, data):
            ICG_file.write(temp_var() + " = " + data[TEMP_VAR] + "\n")
            inc_temp()
            return True
    elif getCP(count) == lexi.COMPOUND_AS_OP:
        count += 1
        if asStLf(count, data):
            ICG_file.write(temp_var() + " = " + temp_var() + " " + getVP(count)[0] + data[TEMP_VAR] + "\n")
            inc_temp()
            return True
    elif getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False 


def asStLf(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        
        if condition(count, data):
            return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN:
        if arrayBody(count, data):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count += 1
        return True
    return False



# def asStComplex(count, data):
#     if argumentOrNull(count, data):
#         if objFunctionArrayInvocationRecursive(count, data):
#             if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
#                 count+=1
#                 return True
#     return False



# def asStComplexOptions(count, data):
#     if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        
#         if condition(count, data):
#             return True
#     elif getCP(count) == lexi.CURLY_BRACKET_OPEN:
#         if arrayBody(count, data):
#             return True
#     elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
#         count+=1
#         return True
#     return False


def arrayBody(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if onedOr2D(count, data):
            return True
    return False

def onedOr2D(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if arrayElements(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    elif getCP(count) == lexi.CURLY_BRACKET_OPEN or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.SEPARATOR_OP:
        if arrayBody2d(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                return True
    return False

def arrayElements(count, data):
    
    if condition(count, data):
        if arraySeparator(count,data):
            return True
    return False

################CHECK FOLLOW SET
def arraySeparator(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        
        if condition(count, data):
            if arraySeparator(count, data):
              return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False 


##################CHECK FOLLOW SET
def arrayBody2d(count,data):
    if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_OPEN":
        count+=1
        if arrayElements(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
                count+=1
                if arraySeparator2d(count, data):
                    return True
    return False



#################CHECK FOLLOW SET
def arraySeparator2d(count ,data):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if arrayBody2d(count, data):
            if arraySeparator2d(count, data):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False




def constructorMst(count, data):
    if getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH  or getCP(count) == lexi.IDENTIFIER:
        if constructorSst(count, data):
            if constructorMst(count, data):
                return True
    elif getCP(count) == lexi.CURLY_BRACKET_CLOSE:
        return True
    return False


def constructorSst(count, data):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count, data):
            return True
    elif getCP(count) == lexi.WHILE:
        if whileSt(count, data):
            return True
    elif getCP(count) == lexi.IF:
        if ifElseSt(count, data):
            return True
    elif getCP(count) == lexi.FOR:
        if forSt(count, data):
            return True
    elif getCP(count) == lexi.FOREACH:
        if forEachSt(count, data):
            return True
    elif getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN:
        if lfSst2(count, data):
            return True
    return False


def lfSst2(count, data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        data[NAME] = getVP(count)
        count+=1
        if sstAllFunctions(count, data):
            return True
    return False


def sstAllFunctions(count, data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN:
        if argumentBody(count, data):
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        data[DATA_TYPE] = data[NAME]
        T = lookUpDT(data[DATA_TYPE])
        if T== None:
           print(fg.red, "Unknown identifier found at line : {}".format(getLine(count)), fg.rs, sep = '')
        
        N = getVP(count)
        data[NAME] = N
        if not insertST(N, data[DATA_TYPE]):
           print(fg.red, "Redeclaration Error at line: {}", getLine(count), fg.rs, sep = '')
        count +=1
        if objectInit(count, data):
            if objectList(count, data):
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    elif getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.SQUARE_BRACKET_OPEN  or getCP(count) == lexi.METHOD_OP or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.AS_OP or getCP(count) == lexi.COMPOUND_AS_OP or getCP(count) == lexi.MDM or getCP(count) == lexi.PM or getCP(count) == lexi.RELATIONAL_OP or getCP(count) == lexi.BOOLEAN_AND or getCP(count) == lexi.BOOLEAN_OR or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.ROUND_BRACKET_CLOSE:
        if argumentOrNull(count, data):
            if objFunctionArrayInvocationRecursive(count,data):
                if asOpOrCompound(count, data):
                    if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                        count+=1
                        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT" or lexi.SEPARATOR_OP or getCP(count) == "ROUND_BRACKET_CLOSE" or getCP(count) == "IDENTIFIER" or getCP(count) == "CURLY_BRACKET_CLOSE" or getCP(count) == "DATA_TYPE" or getCP(count) == "WHILE" or getCP(count) == "IF" or getCP(count) == "FOR" or getCP(count) == "FOR_EACH" or getCP(count) == "SEND":
        return True
    return False





def sst(count, data):
    if getCP(count) == lexi.DATA_TYPE:
        if dec(count, data):
            return True
    elif getCP(count) == lexi.WHILE:
        if whileSt(count, data):
            return True
    elif getCP(count) == lexi.IF:
        if ifElseSt(count, data):
            return True
    elif getCP(count) == lexi.FOR:
        if forSt(count, data):
            return True
    elif getCP(count) == lexi.FOREACH:
        if forEachSt(count, data):
            return True
    elif getCP(count) == lexi.RETURN:
        if return_(count,data):
            return True
    elif getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.ROUND_BRACKET_CLOSE or getCP(count) == lexi.END_OF_STATEMENT or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.CURLY_BRACKET_CLOSE or getCP(count) == lexi.DATA_TYPE or getCP(count) == lexi.WHILE or getCP(count) == lexi.IF or getCP(count) == lexi.FOR or getCP(count) == lexi.FOREACH or getCP(count) == lexi.RETURN:
        if lfSst2(count,data):
            return True

    return False

def return_(count,data):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.RETURN:
        count+=1
        if rValue(count,data):
            if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                count+=1
                return True
    return False


###############CHECK FOLLOW SET FOR THIS###########
def rValue(count,data):
    if getCP(count) == lexi.ROUND_BRACKET_OPEN or getCP(count) == lexi.UNI_BOOLEAN_OP or getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.INTEGER_CONST or getCP(count) == lexi.FLOAT_CONST or getCP(count) == lexi.STRING_CONST or getCP(count) == lexi.BOOLEAN_CONSTANTS or getCP(count) == lexi.END_OF_STATEMENT:
        
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
            N = getVP(count)
            data[NAME] = N
            if not insertST(N, data[DATA_TYPE]):
                print(fg.red, "Redeclaration Error '{}' at line: {}".format(N, getLine(count)), fg.rs, sep = '')
            count += 1
            if init(count,data):
                if list_(count,data):
                    return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        return True
    return False




def arrayDec(count,data):
    if getCP(count) == lexi.SQUARE_BRACKET_OPEN:
        count+=1
        if getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
            count+=1
            if arrayDec2D(count,data):
                return True
    elif getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False

def arrayDec2D(count,data):
    if getCP(count) == lexi.SQUARE_BRACKET_OPEN:
        count +=1
        if getCP(count) == lexi.SQUARE_BRACKET_CLOSE:
            count +=1
            return True
    elif getCP(count) == lexi.IDENTIFIER or getCP(count) == lexi.SEPARATOR_OP or getCP(count) == lexi.END_OF_STATEMENT:
        return True
    return False

def dtOrID(count,data):

    if getCP(count) == lexi.IDENTIFIER:
        data[DATA_TYPE] = getVP(count) 
        count+=1
        return True
    elif getCP(count) == lexi.DATA_TYPE:
        data[DATA_TYPE] = getVP(count) 
        count+=1
        return True

    return False






if __name__ == '__main__':
    main()
