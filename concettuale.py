import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import matplotlib.pyplot as plt

# parameters
fontsize = 10
relation_numbers_fontsize = 8

graph = nx.Graph()

def make_entity(label):
    graph.add_node(label, shape='rectangle', fontsize=fontsize)

def make_attributes(entity, labels):
    labels[-1] = labels[-1] + '\l'
    labels = ['- '+s for s in labels]

    attribute_label = '\l'.join(labels)
    graph.add_node(attribute_label, shape='oval', fontsize=fontsize,
        fixedsize=False, width=0.4)
    graph.add_edge(entity, attribute_label, style='dashed')

relation_numbers_to_str = lambda tp: '{},{}'.format(*tp)

def make_relation(label, first, second, first_relation_numbers, second_relation_numbers):
    graph.add_node(label, shape='diamond', fontsize=fontsize)
    graph.add_edge(first, label, label=relation_numbers_to_str(first_relation_numbers),
        fontsize=relation_numbers_fontsize)
    graph.add_edge(label, second, label=relation_numbers_to_str(second_relation_numbers),
        fontsize=relation_numbers_fontsize)

def make_generalization(label, *generalization_names):
    graph.add_node(label + "_gen", shape='point', style='invis')
    graph.add_edge(label, label + "_gen", style='dotted')

    for gen in generalization_names:
        make_entity(gen)
        graph.add_edge(gen, label + "_gen", style='dotted')

# entities
make_entity('Data')
make_entity('Algorithm')
make_entity('Run')
make_entity('Parameters')
make_entity('Hardware')

# generalizations
make_generalization('Data', 'NumPy', 'CSV', 'XML')
make_generalization('Hardware', 'Cluster', 'Computer')

# attributes
make_attributes('Data', ['ID!', 'Notes'])
make_attributes('Run', ['Date', 'Duration', 'RAM', 'ExitCode', 'Error', 'Notes'])
make_attributes('Hardware', ['ID!', 'RAM', 'CPU', 'OS', 'Libraries', 'Notes'])
make_attributes('Parameters', ['ID!', 'Tuple'])
make_attributes('Cluster', ['Nodes'])
make_attributes('NumPy', ['Shape', 'Dtype'])
make_attributes('Algorithm', ['ID!', 'Path', 'GitBranch', 'Notes'])

# relations
make_relation('Supports', 'Parameters', 'Algorithm', (1,'N'), (1,'N'))
make_relation('Available', 'Data', 'Hardware', (1, 'N'), (1, 'N'))
make_relation('Uses', 'Run', 'Algorithm', (0, 'N'), (1, 1))
make_relation('On', 'Run', 'Data', (0, 'N'), (1, 1))
make_relation('Where', 'Run', 'Hardware', (0, 'N'), (1, 1))
make_relation('Returns', 'Run', 'Data', (1,1), (1,1))

A = to_agraph(graph)
A.layout('dot')
A.graph_attr['nodesep'] = 10
A.graph_attr['dpi'] = 300
A.draw('res/schema_concettuale.png')
