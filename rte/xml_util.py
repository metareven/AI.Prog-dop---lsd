import xml.dom.minidom


# Function for reading an xml document from file
# Takes the url of an xml document as input and returns a dom instance of the xml
def get_dom_from_xml(xml_file):
    return xml.dom.minidom.parse(xml_file)

# Takes a dom as input and returns a list of element nodes with name "pair"
def get_pair_nodes(doc):
    pairs = doc.getElementsByTagName("pair")
    return pairs

# Takes a list of elements nodes with name "pair" and returns a list of string pairs (text, hypotesis)
def get_attributes_from_pair_nodes(pair_nodes):
    pairs = []
    for pair in pair_nodes:
        text = pair.getElementsByTagName("t")[0].childNodes[0].nodeValue
        hypothesis = pair.getElementsByTagName("h")[0].childNodes[0].nodeValue
        id_number = pair.getAttributeNode("id").value
        entailment = pair.getAttributeNode("entailment").value
        pairs.append((text,hypothesis,id_number,entailment))
    return pairs
