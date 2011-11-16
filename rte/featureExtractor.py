#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lars
#
# Created:     15.11.2011
# Copyright:   (c) Lars 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import xml_util
import lemma

def main():
    a = FeatureExtractor()
    pass

class FeatureExtractor():

        def __init__(self):
            self.features = {"words":[], "lemmas":[], "POS":[], "bigrams":[]}
            self.features["words"] = calculateWordMatch()
            self.features["lemmas"] = calculateLemmas()
            self.features["POS"] = calculatePOS()
            self.features["bigrams"] = calculateBigrams()

def readAttributesFromFile():
        # Be aware that it takes quite some time to read the preprocessed xml file
        dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
        pair_nodes = xml_util.get_pair_nodes(dom_doc)
        pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pair_nodes)
        return pair_attributes


#calculates word match for each pair
def calculateLemmas():
            pair_attributes = readAttributesFromFile()
            n = len(pair_attributes)
            results = []
            entailments = [0 for foo in range(n+1)]
            for i in range(n):
                t,h,id_num,e,ta = pair_attributes[i]
                id_num = int(id_num)
                text,pos = xml_util.get_lemmas_from_text_node(t)
                hypothesis,pos = xml_util.get_lemmas_from_text_node(h)

                matching_words = 0
                new_hyp = []
                for word in hypothesis:
                    if word not in new_hyp:
                        new_hyp.append(word)
                hypothesis = new_hyp[:]
                for word in hypothesis:
                    if word in text:
                        matching_words += 1
                entails = (float(matching_words) / float(len(hypothesis)))
                results.append(entails)
            return results

def calculateWordMatch():
            pass

def calculatePOS():
            pass

def calculateBigrams():
            pass




if __name__ == '__main__':
    main()
