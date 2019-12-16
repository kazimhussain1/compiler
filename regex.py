import re as re

NO_MATCH = "No match Found"
IDENTIFIER = "IDENTIFIER"
STRING_CONST = "STRING_CONST"
FLOAT_CONST = "FLOAT_CONST"
INTEGER_CONST = "INTEGER_CONST"



def checkValue(word):

    int_re = r"[\+\-]?[0-9]+"
    float_re = r"[\+\-]?([0-9]*\.[0-9]+)"

    string_re = r"(\"([^\"]|\\\")*\")|(\'([^\']|\\\')*\')"
    
    id_re = r"[a-zA-Z_]+[0-9a-zA-z_]*"

    result = re.fullmatch(int_re, word)
    

    if result == None:
        result = re.fullmatch(float_re, word)

        if result == None:
            result = re.fullmatch(string_re, word)

            if result == None:
                result = re.fullmatch(id_re, word)

                if result == None:
                    return NO_MATCH
            
                else:
                   return IDENTIFIER
            
            else:
                return STRING_CONST

        else:
           return FLOAT_CONST

    else:
        return INTEGER_CONST
