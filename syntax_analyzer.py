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
        




tokenSet = []

def getCP(count):
    return tokenSet[count.value][lexi.CLASS_PART]


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
    
    if staticOptional(count):
        if classBodyStLf(count):
            return True

    elif constructorSt(count):
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
    if paramBody(count):
        if body(count):
            if classBodySt(count):
                return True
    elif init(count):
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
    if classSt(count):
        if classStRecursive(count):
            return True
            
    elif interfaceSt(count):
        if classStRecursive(count):
            return True
        
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.CLASS or tokenSet[count.value][lexi.CLASS_PART] ==  lexi.INTERFACE:
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
    elif tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE" or "IDENTIFIER":
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
    if sst(count):
        if mst(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
        return True
    return False





#CHNAGED
def decOrObjDec(count):
    if dec(count):
        return True
    elif objectDec(count):
        return True
    return False

def dec(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "DATA_TYPE":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if init(count):
                if list_(count):
                    if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                        count+=1
                        return True
    return False

def init(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "AS_OP":
        count+=1
        if condition(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATMENT":
        return True
    return False

def  initIdConst(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if init(count):
            return True
    elif const(count):
        return True
    return False


def const(count):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.INTEGER_CONST: 
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "STRING_CONST":
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "FLOAT_CONST":
        count+=1
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == lexi.BOOLEAN_CONSTANTS:
        count+=1
        return True 
    return False



def objectDec(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
            count+=1
            if objectInit(count):
                if objectList(count):
                    if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                        count+=1
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
        if nt(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NONE":
        count+=1
        return True
    return False

def nt(count):
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
    if condition(count):
        if argumentBodyRecursive(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False




def argumentBodyRecursive(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if condition(count):
            if argumentBodyRecursive(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
        return True
    return False


def condition(count):
    if ae(count):
        if condition_dash(count):
            return True
    return False




def condition_dash(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "OR":
        count+=1
        if ae(count):
            if condition_dash(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT" or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
        return True
    return False

def ae(count):
    if ROPE(count):
        if ae_dash(count):
            return True
    return False

def ROPE(count):
    if e(count):
        if ROPE_Dash(count):
            return True
    return False


def e(count):
    if t(count):
        if e_Dash(count):
            return True
    return False

def t(count):
    if f(count):
        if t_Dash(count):
            return True
    return False

def e_Dash(count):
    if pm(count):
        if t(count):
            if e_Dash(condition):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT" or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
        return True
    return False

def t_Dash(count):
    if mdm(count):
        if f(count):
            if t_Dash(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "PM" or  lexi.SEPARATOR_OP or "END_OF_STATEMENT" or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
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

def f(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
        count+=1
        if condition(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                count+=1
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "NOT":
        count+=1
        if f(count):
            return True
    elif const(count):
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
        if f_Lf(count):
            return True
    return False
        
        
        



def f_Lf(count):
    if argumentOrNull(count):
        if objFunctionArrayInvocationRecursive(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "PM" or  lexi.SEPARATOR_OP or "END_OF_STATEMENT" or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
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
    if interfaceStRecursive(count):
        return True
    return False

def interfaceStRecursive(count):
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
    if argumentBody(count):
        if arrayCall(count):
            return True
    elif arrayCall(count):
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "METHOD_OP" or "END_OF_STATEMENT" or lexi.SEPARATOR_OP or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
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
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT" or lexi.SEPARATOR_OP or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
        return True
    return False

def arrayCall(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_OPEN":
        count+=1
        if e(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_CLOSE":
                count+=1
                if arrayCall2d(count):
                    return True
    return False

def arrayCall2d(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_OPEN":
        count+=1
        if e(count):
            if tokenSet[count.value][lexi.CLASS_PART] == "SQUARE_BRACKET_CLOSE":
                count+=1
    elif tokenSet[count.value][lexi.CLASS_PART] == "METHOD_OP" or "AS_OP" or "END_OF_STATEMENT":
        return True
    return False

def ifElseSt(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IF":
        count+=1
        if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_OPEN":
            count+=1
            if condition(count):
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
            if condition(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "ROUND_BRACKET_CLOSE":
                    count+=1
                    if body(count):
                        if elif_(count):
                            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "ELSE" or "IF":
        return True
    return False




def else_(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "ELSE":
        count+=1
        if body(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "IF":
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
            if condition(count):
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
    if dec(count):
        return True
    elif asSt(count):
        return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
        count+=1
        return True
    return False



def forCondition(count):
    if condition(count):
        if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
            count+=1
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
            count+=1
            return True
    return False


###############CHECK FOLLOW SET
def forIncDec(count):
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
    if condition(count):
        return True
    elif arrayBody(count):
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
    if condition(count):
        return True
    elif arrayBody(count):
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
    if arrayElements(count):
        if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
            count+=1
            return True
    elif arrayBody2d(count):
        if tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE":
            count+=1
            return True
    return False

def arrayElements(count):
    if condition(count):
        if arraySeparator(count):
            return True
    return False

################CHECK FOLLOW SET
def arraySeparator(count):
    if tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP:
        count+=1
        if condition(count):
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
    elif tokenSet[count.value][lexi.CLASS_PART] == "CURLY_BRACKET_CLOSE" or  lexi.SEPARATOR_OP:
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
    if dec(count):
        return True
    elif whileSt(count):
        return True
    elif ifElseSt(count):
        return True
    elif forSt(count):
        return True
    elif forEachSt(count):
        return True
    elif lfSst2(count):
        return True

def idConst(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "IDENTIFIER":
        count+=1
    elif const(count):
        return True
    return False

def lfSst2(count):
    if tokenSet[count.value][lexi.CLASS_PART] == lexi.IDENTIFIER:
        count+=1
        if sstAllFunctions(count):
            return True
    return False


def sstAllFunctions(count):
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
    elif argumentOrNull(count):
        if objFunctionArrayInvocationRecursive(count):
            if asOpOrCompound(count):
                if tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT":
                    count+=1
                    return True
    elif tokenSet[count.value][lexi.CLASS_PART] == "END_OF_STATEMENT" or lexi.SEPARATOR_OP or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
        return True
    return False


def sst(count):
    if dec(count):
        return True
    elif whileSt(count):
        return True
    elif ifElseSt(count):
        return True
    elif forSt(count):
        return True
    elif forEachSt(count):
        return True
    elif return_(count):
        return True
    elif lfSst2(count):
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
    if condition(count):
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




def objMethodAttributeRecursive(count):pass

def pm(count):pass

def ROPE_Dash(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "RELATIONAL_OP":
        count += 1
        if e(count):
            if ROPE_Dash(count):
                return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT" or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND":
        return True
    return False


def ae_dash(count):
    if tokenSet[count.value][lexi.CLASS_PART] == "AND":
        count += 1
        if ROPE(count):
          if ae_dash(count):
            return True
    elif tokenSet[count.value][lexi.CLASS_PART] ==  lexi.SEPARATOR_OP or "END_OF_STATEMENT" or "ROUND_BRACKET_CLOSE" or "IDENTIFIER" or "CURLY_BRACKET_CLOSE" or "DATA_TYPE" or "WHILE" or "IF" or "FOR" or "FOR_EACH" or "SEND": 
        return True
    return False








if __name__ == '__main__':
    main()
