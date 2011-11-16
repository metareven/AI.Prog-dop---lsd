import xml_util
import tree_edit_dist


def threshold_iterator(threshold):
    dom_doc = xml_util.get_dom_from_xml("data/RTE2_dev.preprocessed.xml")
    pairs = xml_util.get_pairs(dom_doc)
    pair_attributes = xml_util.get_attributes_from_preprocessed_pair_nodes(pairs)
    tree_value_pairs = []
    for i in range(3):
        t,h,id_num,e,ta = pair_attributes[i]
        id_num = int(id_num)
        t_values = xml_util.get_minipar_values_from_text_node(t)
        h_values = xml_util.get_minipar_values_from_text_node(h)
        tree_value_pairs.append((t_values,h_values))
    trees1 = build_tree(tree_value_pairs[0])
    trees2 = build_tree(tree_value_pairs[2])
    t1,t2 = trees1
    t11,t22 = trees2
    #print t1
    #print t2
    
    print tree_edit_dist.distance(t22,t2)

def syntax_matching(tree_value_pairs, threshold):
    return 0
    

def build_tree(tree_value_pair):
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
    
    print text_tree
    print hypothesis_tree
    
    return (text_tree, hypothesis_tree)
    
#    text_nodes = {}
#    
#    
#    nodes = {}
#    children = {}
#    for n in hypothesis:
#        n_id,p_id,lemma = n
#        nodes[n_id] = Node(lemma)
#        if p_id not in children.keys():
#            children[p_id] = [n_id]
#        else:
#            children[p_id].append(n_id)
#    root_node = Node("root")
#    nodes[unicode("-1")] = root_node
#    for n_id in nodes.keys():
#        if n_id in children.keys():
#            for c in children[n_id]:
#                nodes[n_id].append(nodes[c])
#    print root_node
#    return ("text-tree", "hypothesis-tree")

def printPairValues(pair):
    node_values = xml_util.get_minipar_values_from_pair_node(pair)
    for n in node_values:
        n_id, lemma, parent_id = n
        print n_id + " " + lemma + " " + parent_id + "\n"

def main():
    threshold_iterator(-1)
    
        
            

if __name__ == '__main__':
    main()
        
