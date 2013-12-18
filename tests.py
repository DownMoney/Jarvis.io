from statements import Lexicon
from statements import FactBase
import statements
import pos_tagging
from agreement import *
from semantics import *

l2 = Lexicon()
f2 = FactBase()


process_statement(['John', 'is', 'running'],l2,f2)
process_statement(['John', 'is', 'a', 'duck'],l2,f2)


tr0 = all_parses(['Which', 'duck', 'is', 'running', '?'],l2)


for t in tr0:
	print t
	tr = restore_words(t, ['Which', 'duck', 'is', 'running', '?'])
	print check_all_nodes(t)
	tr.draw()

