import xml_util
import lexical

def threshold_iterator(threshold):
    # Be aware that it takes quite some time to read the preprocessed xml file
    dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
    pair_nodes = xml_util.get_pair_nodes(dom_doc)
    pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pair_nodes)
    if threshold == -1:
        for i in range(100):
            threshold = 1.0 - (0.01 * i)
            lemma_matching(threshold, pair_attributes)
    else:
        lemma_matching(threshold, pair_attributes)

def lemma_matching(threshold, pairs):
    pair_attributes = pairs[:]
    n = len(pair_attributes)
    results = [0 for foo in range(n+1)]
    entailments = [0 for foo in range(n+1)]
    for i in range(n):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_lemmas,t_pos = xml_util.get_lemmas_from_text_node(t)
        h_lemmas,h_pos = xml_util.get_lemmas_from_text_node(h)
        text = []
        for i in range(len(t_lemmas)):
            text.append((t_lemmas[i],t_pos[i]))
        hypothesis = []
        for i in range(len(h_lemmas)):
            hypothesis.append((h_lemmas[i],h_pos[i]))
        entailments[id_num] = calculate_entailment(text,hypothesis,threshold)
        if (e == entailments[id_num]):
            results[id_num] = 1
        else:
            results[id_num] = 0
    lexical.output_rte(entailments)
    print "Threshold: " + "%.2f"%threshold + " Accuracy: " + str(float(sum(results)) / float(n))

def calculate_entailment(text, hypothesis, threshold):
    matching_words = 0
    for h in hypothesis:
        if h in text:
            matching_words += 1
    entails = float(matching_words) / float(len(hypothesis))
    if entails > threshold:
        return "YES"
    else:
        return "NO"

def main():
    threshold_iterator(0.63) # Calculates the accuracy for different thresholds if arg is -1, uses the arg as threshold otherwise

if __name__ == '__main__':
    main()
