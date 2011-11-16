import xml_util

# Same class as in the three distance algorithm class
class Node(list):
    """
    Simple recursive representation of a tree as a labeled node with zero or
    more child nodes
    """

    def __init__(self, label, *children):
        self.label = label
        list.__init__(self, children)
        
    def is_leaf(self):
        return not self
    
    def left_child(self):
        return self[0]

    def __str__(self):
        """
        string representation of tree as a labeled bracket structure
        """
        if self.is_leaf():
            return self.label
        else:
            return ( self.label + 
                     "( " + 
                     " ".join([str(child) for child in self]) + 
                     ")" )
        
    def __repr__(self):
        return self.label

def printPairValues(pair):
    node_values = xml_util.get_minipar_values_from_pair_node(pair)
    for n in node_values:
        n_id, lemma, parent_id = n
        print n_id + " " + lemma + " " + parent_id + "\n"

def main():
    dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
    pairs = xml_util.get_pairs(dom_doc)
    pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pairs)
    for i in range(1):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        
        #t_values = xml_util.get_minipar_values_from_text_node(t)
        h_values = xml_util.get_minipar_values_from_text_node(h)
        for v in h_values:
            print v

if __name__ == '__main__':
    main()
        
