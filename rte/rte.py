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
import bleu,pos,machine_learning,idf_weighting,syntax_matching
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
            machine_learning.main(3)
        elif text == "four":
            machine_learning.main(4)
        elif text != "exit":
            print "invalid input: input must be one of the following items:"
            print "one\ntwo\nthree\nfour"

if __name__ == '__main__':
    main()
