import xml.dom.minidom

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

def get_pair_nodes(doc):
    pairs = doc.getElementsByTagName("pair")
    return pairs


# Main method for testing purposes
def main():
    test_document = get_a_document_from_file("data/RTE2_dev.xml")
    pair_nodes = get_pair_nodes(test_document)
    pairs = get_text_pairs_from_pair_nodes(pair_nodes)
    print len(pairs)
    print pairs[0]
    print pairs[len(pairs)-1]

if __name__ == '__main__':
    main()
