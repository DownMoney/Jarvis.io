# PART D: Semantics for the Query Language.

from statements import *
from pos_tagging import *
from agreement import *



# For convenience, we reproduce the parameterized rules from the handout here:

#    S      -> WHO QP[y] QM | WHICH Nom[y] QP[y] QM
#    QP[x]  -> VP[x] | DO[y] NP[y] T[p]
#    VP[x]  -> I[x] | T[x] NP | BE[x] A | BE[x] NP[x] | VP[x] AND VP[x]
#    NP[s]  -> P | AR Nom[s]
#    NP[p]  -> Nom[p]
#    Nom[x] -> AN[x] | AN[x] Rel[x]
#    AN[x]  -> N[x] | A AN[x]
#    Rel[x] -> WHO VP[x] | NP[y] T[y]
#    N[s]   -> "Ns"  etc.



def sem(tr):
    """translates a syntax tree into a logical lambda expression (in string form)"""
   

    if type(tr) is str:
      return ''

    rule = top_level_rule(tr)

   

    if (tr.node == 'P'):
        return tr[0][0]
    elif (tr.node == 'N'):
        return '(\\x.' + tr[0][0] + '(x))'   # \\ is the escape sequence for \
    elif tr.node == 'A':       
        return '(\\x.' + tr[0][0] + '(x))'
    elif tr.node == 'T':
        return noun_stem(tr[0][0])
    elif tr.node == 'I':
        return '(\\x.' + noun_stem(tr[0][0]) + '(x))'

    if (rule == 'AN -> A AN'):
        return '(\\x.(' + sem(tr[0]) + '(x) & ' + sem(tr[1]) + '(x)))'
    elif rule == 'S -> WHO QP QM':      
        return sem(tr[1])
    elif rule == 'VP -> BE A':
        return '(\\x.('+sem(tr[1])+'))(x)'
    elif rule == 'S -> WHICH Nom QP QM':
        return '(\\x.(('+sem(tr[1])+'(x)) & ('+sem(tr[2])+'(x))))'    
    elif rule == 'NP -> AR Nom':
        return '(\\x.('+sem(tr[1])+')(x))(x)'
    elif rule == 'QP -> DO NP T':
        return '(\\x. (exists y.('+sem(tr[1])+' & '+sem(tr[2])+'(y,x))))'
    elif rule == 'QP -> VP':
        return sem(tr[0])
    elif rule == 'VP -> T NP':        
        if top_level_rule(tr[1][0])[0] == 'P':
            return '(\\x.(exists y.(('+sem(tr[0])+'(x,y) & '+sem(tr[1])+'))))'      #Forward lookup to see if the person is a subject (i.e if they are being liked or if they are liking someone)
        return '(\\y.(exists x.(('+sem(tr[0])+'(y,x) & '+sem(tr[1])+'))))'
    elif rule == 'VP -> BE NP':
        return sem(tr[1])
    elif rule == 'AN -> N':
        return sem(tr[0])    
    elif rule == 'NP -> P':
        return '\\x.(y='+sem(tr[0])+')(x)'
    elif rule == 'VP -> VP AND VP':
        return '(\\x.('+sem(tr[0])+'(x) & '+sem(tr[2])+'(x)))'
    elif rule == 'VP -> I':
        return sem(tr[0])
    elif rule == 'Nom -> AN Rel':
        return '(\\x.('+sem(tr[0])+'(x) & '+sem(tr[1])+'(x)))'
    elif rule == 'Rel -> WHO VP':
        return  '(\\x.('+sem(tr[1])+'))(x)'

    temp = ''
    for tree in tr:
       temp += sem(tree)

   
    return temp

# Logic parser for lambda expressions

from nltk import LogicParser
lp = LogicParser()

# Lambda expressions can now be checked and simplified as follows:

#   A = lp.parse('(\\x.((\\P.P(x,x))(loves)))(John)')
#   B = lp.parse(sem(tr))  # for some tree tr
#   A.simplify()
#   B.simplify()


# Model checker

from nltk.sem.logic import *

# Can use: A.variable, A.term, A.term.first, A.term.second, A.function, A.args

def interpret_const_or_var(s,bindings,entities):
    if (s in entities): # s a constant
        return s
    else:               # s a variable
        return [p[1] for p in bindings if p[0]==s][0]  # finds most recent binding

def model_check (P,bindings,entities,fb):
    if (isinstance (P,ApplicationExpression)):
        if (len(P.args)==1):
            pred = str(P.function)
            arg = interpret_const_or_var(str(P.args[0]),bindings,entities)
            return fb.queryUnary(pred,arg)
        else:
            pred = str(P.function.function)
            arg0 = interpret_const_or_var(str(P.args[0]),bindings,entities)
            arg1 = interpret_const_or_var(str(P.args[1]),bindings,entities)
            return fb.queryBinary(pred,arg0,arg1)
    elif (isinstance (P,EqualityExpression)):
        arg0 = interpret_const_or_var(str(P.first),bindings,entities)
        arg1 = interpret_const_or_var(str(P.second),bindings,entities)
        return (arg0 == arg1)
    elif (isinstance (P,AndExpression)):
        return (model_check (P.first,bindings,entities,fb) and
                model_check (P.second,bindings,entities,fb))
    elif (isinstance (P,ExistsExpression)):
        v = str(P.variable)
        P1 = P.term
        for e in entities:
            bindings1 = [(v,e)] + bindings
            if (model_check (P1,bindings1,entities,fb)):
                return True
        return False

def find_all_solutions (L,entities,fb):
    v = str(L.variable)
    P = L.term
    return [e for e in entities if model_check(P,[(v,e)],entities,fb)]

testFile = open('testFile.txt', 'r')
# Interactive dialogue session

def fetch_input():
    s = raw_input('$$ ')
    while (s.split() == []):
        s = raw_input('$$ ')
    return s    

def output(s):
    print ('     '+s)

def dialogue():
    lx = Lexicon()
    fb = FactBase()
    output('')
    s = fetch_input()
    while (s.split() == []):
        s = raw_input('$$ ')
    while (s != 'exit'):
        if (s[-1]=='?'):
            sent = s[:-1] + ' ?'  # tolerate absence of space before '?'
            wds = sent.split()                       

            tree_s = all_valid_parses(wds,lx)   #try to get only valid parses

            if len(tree_s)==0:
                tree_s = all_parses(wds,lx)     #if there are none try all of the parses

            if len(tree_s)==0:                  #No trees have been found
                if (wds[0].lower() == 'who'):
                    output ("No one")
                else:
                    output ("None")

            for trees in tree_s:
                try:
                    if (len(tree_s)>1):       
                        output ("Ambiguous! Trying anyway")

                    if (len(trees)==0):
                        output ("Eh??")                    
                    else:
                        tr = restore_words (trees,wds)                       
                        res = sem(tr)
                        #print res
                        lam_exp = lp.parse(res)
                        #print lam_exp
                        L = lam_exp.simplify()
                        print L  # useful for debugging
                        entities = lx.getAll('P')
                        results = find_all_solutions (L,entities,fb)

                        if (results != []):
                            buf = ''
                            for r in results:
                                buf = buf + r + '  '
                            output (buf)
                            break

                    if (wds[0].lower() == 'who'):
                        output ("No one")
                    else:
                        output ("None")        
                        
                except Exception, e:
                    print e

                    
        else:
            if (s[-1]=='.'):
                s = s[:-1]  # tolerate final full stop
            wds = s.split()
            msg = process_statement(wds,lx,fb)
            #print fb.binary
            if (msg == ''):
                output ("OK.")
            else:
                output ("Sorry - " + msg)
        s = fetch_input()

# End of PART D.
