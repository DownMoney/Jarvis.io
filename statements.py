# PART A: Processing statements

def add(item,lst):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    allowed = []

    lx = []

    def __init__(self):
        self.lx = []
        self.allowed = ['P', 'N', 'A', 'I', 'T']

    def add(self,stem,cat):
        
        if cat in self.allowed:
            self.lx+=[{stem: cat}]

    def getAll(self,cat):
        r = []
        
        for item in self.lx:
          if cat in item.values():
            r += [item.keys()[0]]       
        return list(set(r))

class FactBase:
    """stores unary and binary relational facts"""
    
    unary = []
    binary = []

    def __init__(self):
        self.unary = []
        self.binary = []

    def addUnary(self,pred,e1):
        self.unary += [{'pred': pred, 'e1': e1}]

    def queryUnary(self,pred,e1):
        for item in self.unary:
            if item['pred'] == pred and item['e1'] == e1:
                return True
        return False

    def addBinary(self,pred,e1,e2):
        self.binary += [{'pred': pred, 'e1': e1, 'e2': e2}]

    def queryBinary(self,pred,e1,e2):
        for item in self.binary:
            if item['pred'] == pred and item['e1'] == e1 and item['e2'] == e2:
                return True
        return False

import re

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
   

    old = s

    vowels = ['a', 'e', 'i', 'o', 'u']

    if s == 'has':                                  #If the stem is have, its 3s form is has.
        s = 'have'   

    if not (re.search(r'(\w+(sse|zze))s$', s)):
        s = re.sub(r'(\w+(se|ze))s$', '\\1', s)         #If the stem ends in se or ze but not in sse or zze, add s (loses, dazes, lapses,
                                                    #analyses).

    s = re.sub(r'(\w+a)s$', '\\1', s)               #If the stem ends in y preceded by a vowel, or in a, simply add s (pays, buys,
    s = re.sub(r'(\w+[a,e,i,o,u]y)s$', '\\1', s)     #congas).   

    s = re.sub(r'(\w?\w+[^a,e,i,o,u])ies$', '\\1y', s)             #If the stem ends in y preceded by a non-vowel and contains at least three
                                                                   #letters, change the y to ies (
                                                                   #ies, tries, unifies).

    s = re.sub(r'(\w*[^a,e,i,o,u]ie)s$', '\\1', s)   #If the stem is of the form Xie where X is a single letter other than a vowel,
                                                     #simply add s (dies, lies, ties | note that this doesn't account for unties).

    s = re.sub(r'(\w+[o,x,xh,sh,ss,zz])es$', '\\1', s) #If the stem ends in o,x,ch,sh,ss or zz, add es (goes, boxes, attaches, washes,
                                                      #dresses, fizzes).

    s = re.sub(r'(\w+[^s,x,y,z,ch,sh,a,e,i,o,u])s$', '\\1', s)  #If the stem ends in anything except s,x,y,z,ch,sh or a vowel, simply add s
                                                                #(eats, tells, shows).

    s = re.sub(r'(\w+[^i,o,s,x,z,ch,sh]e)s$', '\\1', s)         #if the stem ends in e not preceded by i,o,s,x,z,ch,sh, just add s
                                                                #(likes, hates, bathes).

    #if old == s:           #disabled as when the verb is already in it's singular form it would return '' causing T_ without the verb
       # return ''

    return s


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement (wlist,lx,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
   
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')            
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.