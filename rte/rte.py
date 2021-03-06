#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lars
#
# Created:     23.11.2011
# Copyright:   (c) Lars 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import bleu,pos,machine_learning,idf_weighting,syntax_matching,lemma,lexical,tree_edit_dist,syntax_matching
def main():
    text = ""
    while text.lower() != "exit":
        text = str(raw_input())
        if text == "one":
            #do phase one
            pass
        elif text == "two":
            #do phase 2
            pass
        elif text == "three":
            machine_learning.main(3,False)
        elif text == "four":
            machine_learning.main(4,False)
        elif text == "four make":
            machine_learning.main(4,True)
        elif text == "lemma":
            lemma.main()
        elif text == "bleu":
            bleu.main()
        elif text == "lexical":
            lexical.main()
        elif text == "tree distance":
            syntax_matching.main()
        elif text == "idf weighting":
            idf_weighting.main()
        elif text == "pos":
            pos.main()
        elif text != "exit":
            print "invalid input: input must be one of the following items:"
            print "one\ntwo\nthree\nfour"

if __name__ == '__main__':
    main()
