import xml.dom.minidom
import xml_util
from sys import stdout

def threshold_iterator(threshold):
    document = xml_util.get_dom_from_xml("data/RTE2_dev.xml")
    pair_nodes = xml_util.get_pair_nodes(document)
    pair_attributes = xml_util.get_attributes_from_pair_nodes(pair_nodes)
    if threshold == -1:
        for i in range(100):
            threshold = 1.0 - (0.01 * i)
            word_matching(threshold, pair_attributes)
    else:
        word_matching(threshold,pair_attributes)
    
    

def word_matching(threshold, pairs):
    """ This is the function used for task 1 in the RTE project """
    pair_attributes = pairs[:]
    n = len(pair_attributes) # Number of pair attributes
    for i in range(n):
        pair_attributes[i] = format_strings(pair_attributes[i])
    results = [0 for foo in range(n+1)]
    entailments = [0 for foo in range(n+1)]
    for i in range(n):
        t,h,id_num,e = pair_attributes[i]
        entailments[id_num] = calculate_entailment(t,h,threshold)
        if (e == entailments[id_num]):
            results[id_num] = 1
        else:
            results[id_num] = 0
    output_rte(entailments)
    print "Threshold: " + "%.2f"%threshold + " Accuracy: " + str(float(float(sum(results)) / (float(n))))

def output_rte(entailments):
    stdout.write("ranked: no" + "\n")
    for i in range(1,len(entailments)):
        stdout.write(str(i) + " " + entailments[i]  + "\n")

# Formats the strings in a t/h pair so that each sentence string is replaced with a list of words that has
# been stripped of "." and "," as well as being changed to lower case.
def format_strings(pair):
    t,h,i,e = pair
    text = []
    hypothesis = []
    for w in t.split(" "):
        w = w.strip(",")
        w = w.strip(".")
        w = w.lower()
        text.append(w)
    for w in h.split(" "):
        w = w.strip(",")
        w = w.strip(".")
        w = w.lower()
        hypothesis.append(w)
    return (text,hypothesis,int(i),e)
        
def calculate_entailment(text,hypothesis,threshold):
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
    if entails > threshold:
        return "YES"
    else:
        return "NO"

# Main method for testing purposes
def main():
    # Optimal threshold is 0.61
    threshold_iterator(0.61) # Calculates the accuracy for different thresholds if arg is -1, uses the arg as threshold otherwise

if __name__ == '__main__':
    main()
