import xml_util
import tree_edit_dist
import lexical

idf_dict = {}


def threshold_iterator(threshold):
    """ 
    The method used to extract data from the XML-file and calculate distances.
    Iterates over different thresholds to find the best threshold or just
    calculates the entailment values for one threshold.
    """
    global idf_dict
    dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
    pairs = xml_util.get_pairs(dom_doc)
    pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pairs)
    idf_dict = calculate_idf_dictionary(pair_attributes)
    tree_value_pairs = []
    
    # Extracting the actual lemma values from the pair nodes
    for i in range(len(pair_attributes)):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_values = xml_util.get_minipar_values_from_text_node(t)
        h_values = xml_util.get_minipar_values_from_text_node(h)
        tree_value_pairs.append((t_values,h_values))
        
    # Calculating distances between text and hypothesis
    distances = []
    for i in range(len(tree_value_pairs)):
        t_tree,h_tree = build_tree(tree_value_pairs[i])
        dist = tree_edit_dist.distance(t_tree, h_tree, idf_cost)
        normalizer = tree_edit_dist.distance(tree_edit_dist.Node("root"), h_tree, idf_cost)
        normalized_dist = float(dist) / float(normalizer)
        distances.append(normalized_dist)
        
    #for d in distances:
    #    print d
    
    if threshold == -1:
        for i in range(200):
            threshold = 1.0 - (0.005 * i)
            syntax_matching(pair_attributes, distances, threshold)
    else:
        syntax_matching(pair_attributes, distances, threshold)
        
        
    
def syntax_matching(pair_attributes, distances, threshold):
    """ Calculates entailment values based on the tree edit distances and threshold """
    n = len(pair_attributes)
    entailments = [0 for foo in range(n+1)]
    results = [0 for foo in range(n+1)]
    # Calculates entailments and accuracy
    for i in range(n):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        entails = distances[i] < threshold
        entailments[id_num] = "YES" if entails else "NO"
        results[id_num] = 1 if entailments[id_num] == e else 0
    lexical.output_rte(entailments)
    print "Threshold: " + "%.3f"%threshold + " Accuracy: " + str(float(sum(results)) / float(n))
        
    

def build_tree(tree_value_pair):
    """ Builds a tree of a text and a hypothesis """
    text,hypothesis = tree_value_pair
    
    def builder(tree_values):
        nodes = {}
        children = {}
        for n in tree_values:
            n_id,p_id,lemma = n
            nodes[n_id] = tree_edit_dist.Node(lemma)
            if p_id not in children.keys():
                children[p_id] = [n_id]
            else:
                children[p_id].append(n_id)
        root_node = tree_edit_dist.Node("root")
        nodes[unicode("-1")] = root_node
        for n_id in nodes.keys():
            if n_id in children.keys():
                for c in children[n_id]:
                    nodes[n_id].append(nodes[c])
        return root_node
    
    text_tree = builder(text)
    hypothesis_tree = builder(hypothesis)
    
    #print text_tree
    #print hypothesis_tree
    
    return (text_tree, hypothesis_tree)


def idf_cost(node1, node2, idf_value=idf_dict):
    """ Defines the idf-cost for edit operation on pair of nodes """
    
    # deletion cost
    if node2 is None:
        return 0
    
    # insertion cost
    if node1 is None:
        if node2.label in idf_value.keys(): # if the label is an actual lemma
            return 1.0 / float(idf_value[node2.label])
        else:
            return 1.0 / 800.0 # if the label is used in all trees, such as "root"
    
    # substitution cost
    if node1.label != node2.label:
        return 1
    else:
        return 0
    
def calculate_idf_dictionary(pair_attributes):
    """ Calculates the idf-dictionary """
    for i in range(len(pair_attributes)):
        t, h, id_num, e, ta = pair_attributes[i]
        t_lemmas, pos = xml_util.get_lemmas_from_text_node(t)
        h_lemmas, pos = xml_util.get_lemmas_from_text_node(h)
        doc = []
        words = []
        documents = []
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
    return idf_dict



def main():
    threshold_iterator(0.41)
    
        
            
if __name__ == '__main__':
    main()
        
