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
import lexical
import bleu
import orange

def main():
    """main method for testing"""
    features = FeatureExtractor()

class FeatureExtractor():

        def __init__(self):
            self.features = {"words":[], "lemmas":[], "POS":[], "bigrams":[]}
            self.features["words"] = calculateWordMatch()
            self.features["lemmas"] = calculateLemmas()
            self.features["POS"] = calculatePOS()
            self.features["bigrams"] = calculateBigrams()
            self.Domain = orange.Domain([orange.EnumVariable(x) for x in ["words", "lemmas", "POS", "bigrams"]])
            self.ExampleTable= self.createOrangeTable()

        def createOrangeTable(self):
            """creates an ExampleTable for the orange framework"""
            data = []
            n = len(self.features.items())/len(self.features.keys())
            for i in range(n):
                data.append([])
                for f in self.features.keys():
                    temp = self.features[f]
                    temp2 = int(temp[i] * 100)
                    data[i].append(temp2)
            return orange.ExampleTable(self.Domain,data)

def readProcessedAttributesFromFile():
        # Be aware that it takes quite some time to read the preprocessed xml file
        dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
        pair_nodes = xml_util.get_pair_nodes(dom_doc)
        pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pair_nodes)
        return pair_attributes

def readAttributesFromFile():
    document = xml_util.get_dom_from_xml("data/RTE2_dev.xml")
    pair_nodes = xml_util.get_pair_nodes(document)
    pair_attributes = xml_util.get_attributes_from_pair_nodes(pair_nodes)
    return pair_attributes


#calculates word match for each pair
def calculateLemmas():
            pair_attributes = readProcessedAttributesFromFile()
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
    pair_attributes = readAttributesFromFile()

    n = len(pair_attributes) # Number of pair attributes
    results = []
    for i in range(n):
        pair_attributes[i] = lexical.format_strings(pair_attributes[i])
    for i in range(n):
        text,hypothesis,id_num,e = pair_attributes[i]
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


def calculatePOS():
    pair_attributes = readProcessedAttributesFromFile()
    n = len(pair_attributes)
    results = []
    for i in range(n):
        text,hypothesis,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_lemmas,t_pos = xml_util.get_lemmas_from_text_node(text)
        h_lemmas,h_pos = xml_util.get_lemmas_from_text_node(hypothesis)
        text = []
        for i in range(len(t_lemmas)):
            text.append((t_lemmas[i],t_pos[i]))
        hypothesis = []
        for i in range(len(h_lemmas)):
            hypothesis.append((h_lemmas[i],h_pos[i]))
        matching_words = 0
        for h in hypothesis:
            if h in text:
                matching_words += 1
        entails = float(matching_words) / float(len(hypothesis))
        results.append(entails)

    return results

def calculateBigrams():
    pair_attributes = readProcessedAttributesFromFile()

    n = len(pair_attributes)
    results = []
    entailments = [0 for foo in range(n+1)]
    for i in range(n):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_lemmas,pos = xml_util.get_lemmas_from_text_node(t)
        h_lemmas,pos = xml_util.get_lemmas_from_text_node(h)
        results.append(bleu.modified_bleu(t_lemmas,h_lemmas))

    return results





if __name__ == '__main__':
    main()
