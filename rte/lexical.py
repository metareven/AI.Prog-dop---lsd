import xml.dom.minidom

def word_matching():
    return 0

# function for reading an xml document from file
# takes the url of an xml document as input and returns a dom instance of the xml
def get_a_document_from_file(file_object):
    return xml.dom.minidom.parse(file_object)

# main method for testing purposes
def main():
    test_document = get_a_document_from_file("data/RTE2_dev.xml")
    print test_document.childNodes
    # test_document -> root node -> proper child -> 1 for t / 3 for h
    print test_document.childNodes[1].childNodes[1].childNodes[1].childNodes[0].nodeValue # only the odd numbered children are actual pairs
    print test_document.childNodes[1].nodeType

if __name__ == '__main__':
    main()
