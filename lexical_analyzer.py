import os
from keyword_constants import *
import regex as regex

CLASS_PART = "CLASS_PART"
VALUE_PART = "VALUE_PART"
LINE_NUMBER = "LINE_NUMBER"

keywords_dict = {

    IMPORT : ["import"],
    END_OF_STATEMENT : [";"],
    METHOD_OP : ["."],
    SEPARATOR_OP : [","],
    DATA_TYPE : ["int","text","float","boolean"],
    BOOLEAN_CONSTANTS : ["true", "false", "True", "False"],
    NONE : ["None"],
    WHILE : ["while"],
    FOREACH : ["foreach"],
    FOR : ["for"],
    IN : ["in"],
    IF : ["if"],
    ELSE : ["else"],
    ELIF : ["elif"],
    BREAK : ["break"],
    CONTINUE : ["continue"],
    RETURN : ["send"],
    STATIC : ["static"],
    CLASS : ["class"],
    INTERFACE : ["interface"],
    ABSTRACT : ["abstract"],
    ACCESS_MODIFIERS : ["private", "protected", "public"],
    CONSTRUCTOR : ["constructor"],
    CURLY_BRACKET_OPEN : ["{"],
    CURLY_BRACKET_CLOSE : ["}"],
    ROUND_BRACKET_OPEN : ["("],
    ROUND_BRACKET_CLOSE : [")"],
    SQUARE_BRACKET_OPEN : ["["],
    SQUARE_BRACKET_CLOSE : ["]"],
    AS_OP : ["="],
    COMPOUND_AS_OP : ["+=", "-=", "*=", "/=", "%="],
    PM : ["+", "-"],
    MDM : ["*", "/", "%"],
    RELATIONAL_OP : ["<", ">", "<=", ">=", "!=", "=="],
    BOOLEAN_AND : ["AND", "and"],
    BOOLEAN_OR : ["OR", "or"],
    UNI_BOOLEAN_OP : ["NOT"],
}

keywords_list = [item for subList in keywords_dict.values() for item in subList]

doubleOpPartA = ["<", ">", "!", "=", "+" , "-" , "*" , "/" , "%"]

doubleOpPartB = ["="]

tokenSet = []


def lexicalAnalyzer(path):

    outputFile = open(file = "lexer_output.token", mode = "wt")


    if path != "":
        filePath = os.path.abspath(path)
        

        inputFile = open(file = filePath, mode="rt")

        lineNumber =0

        insideString = False
        stringTerminator = ""

        insideMultiLineComment = False
        multiLineCommentString = ""
        multiLineCommentStart = 0

        for line in inputFile:
            line += " "
            temp = ""
            lineNumber+=1

            charIndex = 0
            while charIndex < len(line):

###################################################### Multi-Line Comment Detection ###################################################################################################
                if insideMultiLineComment:
                    while charIndex < len(line):

                        multiLineCommentString += line[charIndex]
                        if multiLineCommentString[len(multiLineCommentString)-2] == "#" and multiLineCommentString[len(multiLineCommentString)-1] == "#":
                            #generateToken(multiLineCommentString, multiLineCommentStart, outputFile)
                            charIndex += 1
                            insideMultiLineComment = False
                            break

                        charIndex+=1

                if charIndex > len(line)-1:
                    break
                            

                if line[charIndex] == "#" and line[charIndex+1] == "#" and not insideString:
                    insideMultiLineComment = True
                    multiLineCommentStart = lineNumber
                    if len(temp) > 0 :
                        generateToken(temp, lineNumber, outputFile)
                        temp = ""
                    multiLineCommentString = "##"
                    charIndex+=2
                    continue
#########################################################################################################################################################

###################################################### Single-Line Comment Detection ###################################################################################################

                if line[charIndex] == "#" and not insideString:
                    if len(temp) > 0:
                        generateToken(temp, lineNumber, outputFile)
                    
                    temp = line[charIndex:len(line)-1]
                    #generateToken(temp, lineNumber, outputFile)
                    break

#########################################################################################################################################################

###################################################### String Detection ###################################################################################################
               
                if line[charIndex] == "\\" and not insideString:
                    if len(temp) > 0 and not "\\" in temp:
                        generateToken(temp, lineNumber, outputFile)
                        temp = ""

                    temp += line[charIndex]
                    charIndex+=1
                    continue
               
               
                if (line[charIndex] == '\"' or line[charIndex] == "\'") and not insideString:
                    insideString = not insideString
                    stringTerminator = line[charIndex]
                    if len(temp) > 0:
                        generateToken(temp, lineNumber, outputFile)
                        temp = ""
                    temp += line[charIndex]
                    charIndex+=1

                if insideString:
                    temp+= line[charIndex]
                    if line[charIndex] == stringTerminator:
                        i = charIndex - 1
                        slashString = ""
                        while True:
                            if i >= 0:
                                if line[i] == "\\":
                                    slashString += line[i]
                                    i-=1
                                else:
                                    break
                            else:
                                break
                        
                        if len(slashString)% 2 == 0:
                            
                            insideString = not insideString
                            generateToken(temp, lineNumber, outputFile)
                            temp = ""

                    charIndex+=1
                    if charIndex < len(line):
                        continue
                    else:
                        charIndex-=1
                        insideString = not insideString

#########################################################################################################################################################

                
                if line[charIndex] not in (" ", "\n", ";"):

                    if line[charIndex] in doubleOpPartA:
                        if len(temp) > 0:
                            generateToken(temp, lineNumber, outputFile)
                        temp = ""

                        temp = line[charIndex]

                        if line[charIndex+1] in doubleOpPartB:
                            temp += line[charIndex+1]
                            charIndex+=2
                            generateToken(temp, lineNumber, outputFile)
                            temp=""
                            continue
                        
                        generateToken(temp, lineNumber, outputFile)
                        temp =""

                    elif line[charIndex] in keywords_list:
                        if line[charIndex] == ".":
                            try:
                                int(temp)
                                temp += line[charIndex]
                                charIndex+=1
                                continue
                            except Exception as e:
                                #print(e)
                                pass

                        if len(temp) > 0:
                            generateToken(temp, lineNumber, outputFile)
                        temp = ""
                        generateToken(line[charIndex], lineNumber, outputFile)

                    else:
                        temp += line[charIndex]
                else:
                    if len(temp) >0:
                        generateToken(temp, lineNumber, outputFile)
                        temp =""
                    
                    if line[charIndex] == ";":
                        generateToken(";", lineNumber, outputFile)


                
                charIndex+=1

        tokenSet.append({
            CLASS_PART  : END_MARKER,
            VALUE_PART  : "$",
            LINE_NUMBER : lineNumber
        })
        inputFile.close()
    outputFile.close()
    
    return tokenSet

        

        




def searchForKeyword(word):

    for className, values in keywords_dict.items():
        if word in values:
            return className

    return None

def generateToken(word, lineNumber, outFile):

    classPart = searchForKeyword(word)
    if classPart == None:
        classPart = regex.checkValue(word)
        if classPart == NO_MATCH:
            classPart = "INVALID IDENTIFIER"


    if classPart == STRING_CONST:
        word = word[1: len(word)-1]

    tokenSet.append({
        CLASS_PART  : classPart,
        VALUE_PART  : word,
        LINE_NUMBER : lineNumber
    })
    
    word = "\\n".join(word.split("\n"))
    
    token = "("+ classPart +", "+ word + ", " + str(lineNumber) + ")"
    #print(token)
    outFile.write(token + os.linesep) 


