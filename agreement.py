# PART C: Syntax and agreement checking

from statements import *
from pos_tagging import *

# Grammar for the query language (with POS tokens as terminals):

from nltk import parse_cfg
from nltk import parse
from nltk import Tree

query_grammar = parse_cfg('''
   S     -> WHO QP QM | WHICH Nom QP QM | WHAT QP QM
   QP    -> VP | DO NP T
   VP    -> I | T NP | BE A | BE NP | VP AND VP
   NP    -> P | AR Nom | Nom
   Nom   -> AN | AN Rel
   AN    -> N | A AN
   Rel   -> WHO VP | NP T
   N     -> "Ns" | "Np"
   I     -> "Is" | "Ip"
   T     -> "Ts" | "Tp"
   A     -> "A"
   P     -> "P"
   BE    -> "BEs" | "BEp"
   DO    -> "DOs" | "DOp"
   AR    -> "AR"
   WHO   -> "WHO"
   WHICH -> "WHICH"
   AND   -> "AND"
   QM    -> "?"
   ''')

cp = parse.ChartParser(query_grammar)

def all_parses(wlist,lx):
    """returns all possible parse trees for all possible taggings of wlist"""
    all = []
    for tagging in tag_words(wlist,lx):  
        print tagging     
        all = all + cp.nbest_parse(tagging)
    return all

# This produces parse trees of type Tree.
# Available operations on trees:  tr.node, tr[i],  len(tr)


# Singular/plural agreement checking.

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

def label(t):
    if (isinstance(t,str)):
        return t
    elif (isinstance(t,tuple)):
        return t[1]
    else:
        return t.node

def top_level_rule(tr):
    if (isinstance(tr,str)):
        return ''
    else:
        rule = tr.node + ' ->'
        for t in tr:
            rule = rule + ' ' + label(t)
        return rule

def N_phrase_num(tr):

    
    """returns the number attribute of a noun-like tree, based on its head noun"""
    if type(tr) is str:
      return ''

    rule = top_level_rule(tr)

    if (tr.node == 'N'):
      return tr[0][1]  # the s or p from Ns or Np
    elif tr.node == 'P':
      return 's'
   # elif tr.node == 'A':
   #  return 's'

    if rule == 'NP -> P':
      return N_phrase_num(tr[0])
    elif rule == 'NP -> Nom':
      return N_phrase_num(tr[0])
    elif rule == 'NP -> AR Nom':
      return N_phrase_num(tr[1])
    elif rule == 'Nom -> AN':
      return N_phrase_num(tr[0])
    elif rule == 'AN -> N':
      return N_phrase_num(tr[0])
    elif rule == 'Nom -> AN Rel':
      return N_phrase_num(tr[0])
    elif rule == 'AN -> A':
      return N_phrase_num(tr[0])

    temp = ''
    for tree in tr:
       temp += N_phrase_num(tree)

    return temp

def V_phrase_num(tr):
    if type(tr) is str:
        return ''

    rule = top_level_rule(tr)

    """returns the number attribute of a verb-like tree, based on its head verb,
       or '' if this is undetermined."""
    if (tr.node == 'T' or tr.node == 'I'):
        return tr[0][1]  # the s or p from Is,Ts or Ip,Tp
    elif tr.node == 'BE':
        return tr[0][2]
    elif tr.node == 'DO':
        return tr[0][2]

    if rule == 'QP -> VP':
      return V_phrase_num(tr[0])
    elif rule == 'QP -> DO NP T':
      left = V_phrase_num(tr[0])
      right = V_phrase_num(tr[2])
      if left == right:
        return left
      else:
        return ''
    elif rule == 'VP -> I':
      return V_phrase_num(tr[0])
    elif rule == 'VP -> T NP':
      return V_phrase_num(tr[0])
    elif rule == 'VP -> BE A':
      return V_phrase_num(tr[0])
    elif rule == 'VP -> BE NP':
      return V_phrase_num(tr[0])
    elif rule == 'VP -> VP AND VP':
      left = V_phrase_num(tr[0])
      right = V_phrase_num(tr[2])
      if left == right:
        return left
      else:
        return ''
    elif rule == 'Rel -> WHO VP':
      return V_phrase_num(tr[1])
    elif rule == 'Rel -> NP T':
      return V_phrase_num(tr[1])


    temp = ''
    for tree in tr:
       temp += V_phrase_num(tree)

    return temp

def matches(n1,n2):
  
  return (n1==n2 or n1=='' or n2=='')

def check_node(tr):
    """checks agreement constraints at the root of tr"""

    if (isinstance(tr,str)):
        return True

    rule = top_level_rule(tr)
    if (rule == 'S -> WHICH Nom QP QM'):
        return (matches (N_phrase_num(tr[1]), V_phrase_num(tr[2])))
    elif rule == 'S -> WHO QP QM':
      return check_node(tr[1])
    elif rule == 'QP -> VP':
      return check_node(tr[0])
    elif rule == 'QP -> DO NP T':
      return (matches( V_phrase_num(tr[2]), N_phrase_num(tr[1])))
    elif rule == 'VP -> T NP':
      return matches(V_phrase_num(tr[0]), V_phrase_num(tr[1]))
    elif rule == 'VP -> BE NP':
      return matches(V_phrase_num(tr[0]), N_phrase_num(tr[1]))
    elif rule == 'Nom -> AN Rel':
      return matches(N_phrase_num(tr[0]), N_phrase_num(tr[1]))
    elif rule == 'VP -> VP AND VP':
      return matches(N_phrase_num(tr[0]), V_phrase_num(tr[2])) # and matches(N_phrase_num(tr[2]), V_phrase_num(tr[2]))
    else:
      return True


def check_all_nodes(tr):
    """checks agreement constraints everywhere in tr"""
    if (isinstance(tr,str)):
        return True
    elif (not check_node(tr)):
        return False
    else:
        for subtr in tr:
            if (not check_all_nodes(subtr)):
                return False
        return True

def all_valid_parses(wlist,lx):
    """returns all possible parse trees for all possible taggings of wlist
       that satisfy agreement constraints"""
    return [t for t in all_parses(wlist,lx) if check_all_nodes(t)]

# Converter to add words back into trees.
# Strips singular verbs and plural nouns down to their stem.

def restore_words_aux(tr,wds):
    
    if (isinstance(tr,str)):

        wd = wds.pop()
        if (tr=='Is'):
            return ('I_' + verb_stem(wd), tr)
        elif (tr=='Ts'):
            return ('T_' + verb_stem(wd), tr)
        elif (tr=='Np'):
            return ('N_' + noun_stem(wd), tr)
        elif (tr=='Ip' or tr=='Tp' or tr=='Ns' or tr=='A'):
            return (tr[0] + '_' + wd, tr)
        else:
            return (wd, tr)
    else:
        return Tree(tr.node, [restore_words_aux(t,wds) for t in tr])

def restore_words(tr,wds):
    """adds words back into syntax tree, sometimes tagged with POS prefixes"""
    wdscopy = wds+[]
    wdscopy.reverse()
    return restore_words_aux(tr,wdscopy)

# Example:

# lx.add('John','P')
# lx.add('like','T')
# tr0 = all_valid_parses(['Who','likes','John','?'],lx)[0]
# tr.draw()
# tr = restore_words(tr0,['Who','likes','John','?'])

# End of PART C.