#DARSHAN N. LAL 
#1001667684
#dnl7684


from logical_expression import *

#This function works same as the all() function of python 3 
def all(iterable):
    for it_element in iterable:
        if not it_element:
            return False
    return True

#This function will check the final value is true or false
def entailmentcheck(know_bass, state):
    
    #initializing global variable
    global operator
    global ttentails

    #Initializing s dictionary
    symboldict = {}

    #Getting symbols
    try:
        for exp in know_bass.subexpressions:

            if len(exp.connective) == 1 and  len(exp.subexpressions) == 0:
                    symboldict[exp.symbol[0]] = True

                    if exp.symbol[0] in operator:
                        operator.remove(exp.symbol[0])        
            elif exp.connective[0] == 'not' and  len(exp.subexpressions[0].subexpressions) == 0:
                    symboldict[exp.subexpressions[0].symbol[0]] = False

                    if exp.subexpressions[0].symbol[0] in operator:
                        operator.remove(exp.subexpressions[0].symbol[0])
    except:
        print "Unable to access symbols"

    #After getting all the symbols tt_check_all
    oplist = list(operator)
    tt_check_all(know_bass, state, oplist, symboldict)

    #returning true or false value
    return ttentails

def tt_check_all(know_bass, state, symbols, symboldict):

    #initializing the global variables
    global ttentails
    global counter
    
   
    #if no symbol is present like 'M_1_1' which means it is true
    if len(symbols) != 0:
            operator_one = symbols[0]
            symbols.remove(operator_one)

            symbols_duplicate = deepcopy(symbols)

            #if 'not' is absent then true 
            symboldict[operator_one] = True
            tval = tt_check_all(know_bass, state, symbols, symboldict)

            #if 'not' is present then false
            symboldict[operator_one] = False
            fval = tt_check_all(know_bass, state, symbols_duplicate, symboldict)

    else:
        if verify_with_rules(know_bass, symboldict, []):
            ttentails.append(verify_with_rules(state, symboldict, []))
            return ttentails[len(ttentails) - 1]
        else:
            return True

def verify_with_rules(expression, symboldict, top_operator):
    
    if expression.connective[0]:
        
        #for every subexpression append the top stack of operators
        for subexpression in expression.subexpressions:
            top_operator.append(verify_with_rules(subexpression, symboldict, []))

        
        if len(top_operator) <= 0:
            if expression.connective[0] == 'and':
                return True
            elif expression.connective[0] in ['or', 'xor']:
                return False
        else:
            top_op = top_operator.pop()


        if expression.connective[0] == 'iff':
            if top_op == top_operator.pop():
                return True
            else:
                return False

        elif expression.connective[0] == 'if':
            while(len(top_operator) > 0):
                top_op = (not top_operator.pop()) or top_op
            return top_op

        elif expression.connective[0] == 'not':
            return (not top_op)

        elif expression.connective[0] == 'and':
            if top_op and all(top_operator):
                top_op = True
            else:
                top_op = False

            return top_op

        elif expression.connective[0] == 'or':
            while(len(top_operator) > 0):
                top_op2 = top_operator.pop()

                if top_op or top_op2:
                    top_op = True
                else:
                    top_op = False
            return top_op

        elif expression.connective[0] == 'xor':
            while(len(top_operator) > 0):
                if top_op != top_operator.pop():
                    return True
                else:
                    return False
        

    elif expression.symbol[0] and expression.symbol[0] != '':
        return symboldict[expression.symbol[0]]
    