import xml.dom.minidom

# This is the function used for task 1 in the RTE project
def word_matching():
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
    text = t.split(" ")
    hypothesis = h.split(" ")
    for w in text:
        w = w.strip(",")
        w = w.strip(".")
        w = w.lower()
    for w in hypothesis:
        w = w.strip(",")
        w = w.strip(".")
        w.lower()
    return (text,hypothesis)
        

# Main method for testing purposes
def main():
    test_document = get_a_document_from_file("data/RTE2_dev.xml")
    pair_nodes = get_pair_nodes(test_document)
    pairs = get_text_pairs_from_pair_nodes(pair_nodes)
    for i in range(len(pairs)):
        pairs[i] = format_strings(pairs[i])
    h,t = pairs[0]
    print h
    print t

if __name__ == '__main__':
    main()
