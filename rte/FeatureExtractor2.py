#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lars
#
# Created:     20.11.2011
# Copyright:   (c) Lars 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import xml_util
import lemma
import lexical
import bleu
import orange
import syntax_matching
import Synonyms

def main():
    """main method for testing"""
    features = FeatureExtractor()

class FeatureExtractor():
    # lemmas,bigrams,idf gives 0.7125 with cross validation
    # lemmas alone give 0.6025 with splitting the data in half, but only 0.545 if the training data is switched with the test data
    def __init__(self,createFile=True):
            self.processedPairs = self.readProcessedAttributesFromFile()
            self.pairs = self.readAttributesFromFile()
            self.features= {}
            self.IDs= []
            #self.features = {"words":[], "lemmas":[], "POS":[], "bigrams":[],"entails":[]}
            #self.features["words"] = self.calculateWordMatch()
            #self.features["lemmas"] = self.calculateLemmas()
            #self.features["POS"] = self.calculatePOS()
            #self.features["bigrams"] = self.calculateBigrams()
            self.features["idf"] = self.calculateIdf()
            #self.features["pol"] = self.calculatePolarity()
            self.features["entails"] = self.calculateClass()
            self.Domain = orange.Domain([orange.EnumVariable(x) for x in self.features.keys()])
            #print(self.features.keys())
            self.size= len(self.features["entails"])
            #self.ExampleTable= self.createOrangeTable()
            if(createFile):
                self.writeToTable("table2.tab")

    def writeToTable(self, name):
        table = open(name,"w")
        string = ""
        #adds the names of the features
        for n in self.features.keys():
            if(n != "entails"):
                string = string + n + "\t"
        string = string + "entails\t"
        string = string + "\n"
        counter = 0
        for n in range(len(self.features.keys()) -1):
            string = string + "continuous\t"
            counter = counter +1

        string = string + "discrete\n"
        for n in range(counter):
            string = string + "\t"
        string = string + "class\n"
        n = len(self.features["entails"])
        #n = 800
        for i in range(n):
            for f in self.features.keys():
                if(f != "entails"):
                    temp = self.features[f]
                    if(temp != None):
                        string = string + str(temp[i]) + "\t"
                    else:
                        string = string + "OMG WHAT THE FUCK IS WRONG"
            string = string + str(self.features["entails"][i]) + "\t"
            string = string + "\n"

        #super hack for removing the \t\n at the end of the string
        string = string[0:len(string)-2]
        table.write(string)
        table.close()

    def calculatePolarity(self):
        def helper(text,hypothesis):
                negatives = ["not", "refuse", "wrong", "deny", "no", "false", "ignore", "cannot", "can't", "never", "unsuccessfully"]
                text_negatives = 0
                hypothesis_negatives = 0
                for word in text:
                    if word in negatives:
                        text_negatives += 1
                for word in hypothesis:
                    if word in negatives:
                        hypothesis_negatives += 1
                if (text_negatives % 2) == (hypothesis_negatives % 2):
                    return 0
                else:
                    return 1

        pair_attributes = self.processedPairs[:]
        results = []
        n = len(pair_attributes)
        for i in range(n):
            t,h,id_num,e,ta = pair_attributes[i]
            id_num = int(id_num)
            text,pos = xml_util.get_lemmas_from_text_node(t)
            hypothesis,pos = xml_util.get_lemmas_from_text_node(h)
            results.append(helper(text,hypothesis))
        return results




    def calculateIdf(self):
        pair_attributes = self.processedPairs[:]
        idf_dict = syntax_matching.calculate_idf_dictionary(pair_attributes)
        results = []
        n = len(pair_attributes)
        for i in range(n):
            t,h,id_num,e,ta = pair_attributes[i]
            id_num = int(id_num)
            text,pos = xml_util.get_lemmas_from_text_node(t)
            hypothesis,pos = xml_util.get_lemmas_from_text_node(h)
            idf_counter = 0.0
            idf_divider = 0.0
            for word in hypothesis:
                for w in Synonyms.FindAllSynonyms(word):
                    if w in text:
                        idf_counter += (1.0 / float(idf_dict[word.lower()]))
                        break
                idf_divider += (1.0 / float(idf_dict[word.lower()]))
            idf_word_match = idf_counter / idf_divider
            results.append(idf_word_match)
        return results

    def createOrangeTable(self):
            """creates an ExampleTable for the orange framework"""
            data = []
            n = len(self.pairs)
            for i in range(n):
                data.append([])
                for f in self.features.keys():
                    temp = self.features[f]
                    temp2 = temp[i]
                    data[i].append(temp2)
            return orange.ExampleTable(self.Domain,data)

    def readProcessedAttributesFromFile(self):
            # Be aware that it takes quite some time to read the preprocessed xml file
            dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
            pair_nodes = xml_util.get_pair_nodes(dom_doc)
            pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pair_nodes)
            return pair_attributes

    def readAttributesFromFile(self):
        document = xml_util.get_dom_from_xml("data/RTE2_dev.xml")
        pair_nodes = xml_util.get_pair_nodes(document)
        pair_attributes = xml_util.get_attributes_from_pair_nodes(pair_nodes)
        return pair_attributes



    def calculateClass(self):
        pair_attributes = self.processedPairs[:]
        n = len(pair_attributes)
        results = []
        for i in range(n):
            t,h,id_num,e,ta = pair_attributes[i]
            self.IDs.append(id_num)
            if(e == unicode("YES")):
                results.append(1)
            else:
                results.append(0)
        return results

    #calculates word match for each pair
    def calculateLemmas(self):
                pair_attributes = self.processedPairs[:]
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

    def calculateWordMatch(self):
        pair_attributes = self.pairs[:]

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


    def calculatePOS(self):
        pair_attributes = self.processedPairs[:]
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

    def calculateBigrams(self):
        pair_attributes = self.processedPairs[:]

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
