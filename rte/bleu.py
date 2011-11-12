import xml_util
import lexical

# A modified version of the BLEU algorithm that takes in a hypothesis
# as a candidate and a text as a single reference.
# Returns the BLEU score.
def modified_bleu(text, hypothesis):
    # The only preprocessing done is to change all words to lower case
    for i in range(len(text)):
        text[i] = text[i].lower()
    for i in range(len(hypothesis)):
        hypothesis[i] = hypothesis[i].lower()
    # This algorithm use n-grams with 0 > n > 5
    maximum_n = 4
    bleu_precisions = []
    for i in range(1,1+maximum_n):
        matching_n_grams = 0
        candidate_n_grams = []
        reference_n_grams = []
        for j in range(len(text)-i+1):
            reference_n_grams.append(text[j:j+i])
        for j in range(len(hypothesis)-i+1):
            candidate_n_grams.append(hypothesis[j:j+i])
        for candidate in candidate_n_grams:
            if candidate in reference_n_grams:
                matching_n_grams += 1
        # Apparently you are supposed to divide on the length of the hypothesis itself here
        # but to me it would make more sense to divide on the length of the hypothesis n-gram
        # in order to give a identical text and hypothesis a score of 1.0.
        # Maybe I have misunderstood something
        bleu_precisions.append(float(matching_n_grams) / float(len(hypothesis)))
    return float(sum(bleu_precisions)) / float(maximum_n)
                
def threshold_iterator(threshold):
    # Be aware that it takes quite some time to read the preprocessed xml file
    dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
    pair_nodes = xml_util.get_pair_nodes(dom_doc)
    pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pair_nodes)
    if threshold == -1:
        for i in range(100):
            threshold = 1.0 - (0.01 * i)
            bleu_matching(threshold, pair_attributes)
    else:
        bleu_matching(threshold, pair_attributes)

def bleu_matching(threshold, pairs):
    pair_attributes = pairs[:]
    n = len(pair_attributes)
    results = [0 for foo in range(n+1)]
    entailments = [0 for foo in range(n+1)]
    for i in range(n):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_lemmas,pos = xml_util.get_lemmas_from_text_node(t)
        h_lemmas,pos = xml_util.get_lemmas_from_text_node(h)
        entailments[id_num] = calculate_entailment(t_lemmas,h_lemmas,threshold)
        if e == entailments[id_num]:
            results[id_num] = 1
    print "Threshold: " + "%.2f"%threshold + " Accuracy: " + str(float(sum(results)) / float(n))
    #lexical.output_rte(entailments)

def calculate_entailment(text, hypothesis, threshold):
    return "YES" if modified_bleu(text,hypothesis) > threshold else "NO"
        

def main():
    threshold_iterator(0.24)
    

if __name__ == '__main__':
    main()
