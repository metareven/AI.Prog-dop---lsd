import xml_util
import lexical


def threshold_iterator(threshold):
    dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
    pair_nodes = xml_util.get_pair_nodes(dom_doc)
    pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pair_nodes)
    if threshold == -1:
        for i in range(100):
            threshold = 1.0 - (0.01 * i)
            idf_weighting(threshold,pair_attributes)
    else:
        idf_weighting(threshold,pair_attributes)
    
def idf_weighting(threshold, pairs):
    pair_attributes = pairs[:]
    words = []
    documents = []
    n = len(pair_attributes)
    results = [0 for foo in range(n+1)]
    entailments = [0 for foo in range(n+1)]
    # Starts by adding all the words to the list 'words' and then making a set of these words
    # Also makes a list of documents where each document is a set of all the words in a given
    # (text, hypothesis) pair.
    for i in range(n):
        t,h,id_num,e,ta = pair_attributes[i]
        t_lemmas,pos = xml_util.get_lemmas_from_text_node(t)
        h_lemmas,pos = xml_util.get_lemmas_from_text_node(h)
        doc = []
        for word in t_lemmas:
            words.append(word.lower())
            doc.append(word.lower())
        for word in h_lemmas:
            words.append(word.lower())
            doc.append(word.lower())
        documents.append(set(doc))
    word_set = set(words)
    # Creates a dictionary 'idf_dict' that can be used to count how many document each word is present in
    idf_dict = {}
    # Starts by initiating the count for all words to 0
    for word in word_set:
        idf_dict[word] = 0
    # Then calculates the number of documents each word in the word_set appears in
    for word in word_set:
        for document in documents:
            if word in document:
                idf_dict[word] += 1
    print "dict done"
    for i in range(n):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_lemmas,pos = xml_util.get_lemmas_from_text_node(t)
        h_lemmas,pos = xml_util.get_lemmas_from_text_node(h)
        entailments[id_num] = calculate_entailment(t_lemmas,h_lemmas,idf_dict,threshold)
        results[id_num] = 1 if e == entailments[id_num] else 0
    lexical.output_rte(entailments)
    print "Threshold: " + "%.2f"%threshold + " Accuracy: " + str(float(sum(results)) / float(n))
    
def calculate_entailment(text, hypothesis, idf_dict, threshold):
    idf_counter = 0.0
    idf_divider = 0.0
    for word in hypothesis:
        if word in text:
            idf_counter += (1.0 / float(idf_dict[word.lower()]))
        idf_divider += (1.0 / float(idf_dict[word.lower()]))
    idf_word_match = idf_counter / idf_divider
    return "YES" if idf_word_match > threshold else "NO"

def main():
    # Optimal threshold is 0.61
    threshold_iterator(0.61)

if __name__ == '__main__':
    main()
    
    
        
