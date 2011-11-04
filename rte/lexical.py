import xml.dom.minidom

def word_matching():
    """ This is the function used for task 1 in the RTE project """
    return 0

# Function for reading an xml document from file
# Takes the url of an xml document as input and returns a dom instance of the xml
def get_a_document_from_file(file_object):
    return xml.dom.minidom.parse(file_object)

# Takes a list of elements nodes with name "pair" and returns a list of string pairs (text, hypotesis)
def get_text_pairs_from_pair_nodes(pair_nodes):
    pairs = []
    for pair in pair_nodes:
        text = pair.getElementsByTagName("t")[0].childNodes[0].nodeValue
        hypothesis = pair.getElementsByTagName("h")[0].childNodes[0].nodeValue
        pairs.append((text,hypothesis))
    return pairs

# Takes a dom as input and returns a list of element nodes with name "pair"
def get_pair_nodes(doc):
    pairs = doc.getElementsByTagName("pair")
    return pairs

# Formats the strings in a t/h pair so that each sentence string is replaced with a list of words that has
# been stripped of "." and "," as well as being changed to lower case.
def format_strings(pair):
    t,h = pair
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
    return (text,hypothesis)
        
def calculate_entailment(pair, threshold):
    text,hypothesis = pair
    #print "text" + "\n"
    #print text
    #print "hypothesis" + "\n"
    #print hypothesis
    matching_words = 0
    for word in hypothesis:
        if word in text:
            matching_words += 1
    entails = (float(matching_words) / float(len(hypothesis)))
    print "entails: " + str(entails)
    if entails > threshold:
        return "YES"
    else:
        return "NO"

# Main method for testing purposes
def main():
    test_document = get_a_document_from_file("data/RTE2_dev.xml")
    pair_nodes = get_pair_nodes(test_document)
    pairs = get_text_pairs_from_pair_nodes(pair_nodes)
    for i in range(len(pairs)):
        pairs[i] = format_strings(pairs[i])
    threshold = 0.70
    for i in range(10):
        print calculate_entailment(pairs[i],threshold)
    

if __name__ == '__main__':
    main()
