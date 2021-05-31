import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import matplotlib.pyplot as plt

# parameters
fontsize = 10
relation_numbers_fontsize = 8

graph = nx.MultiGraph()

def make_entity(label):
    graph.add_node(label, shape='rectangle', fontsize=fontsize)

def make_attributes(entity, labels, constraint=True):
    labels[-1] = labels[-1] + '\l'
    labels = ['- '+s for s in labels]

    attribute_label = '\l'.join(labels)
    graph.add_node(attribute_label, shape='oval', fontsize=fontsize,
        fixedsize=False, width=0.4)
    graph.add_edge(entity, attribute_label, style='dashed', constraint=constraint)

    return attribute_label

relation_numbers_to_str = lambda tp: '{},{}'.format(*tp)

def make_relation(label, first, second, first_relation_numbers, second_relation_numbers):
    graph.add_node(label, shape='diamond', fontsize=fontsize)
    graph.add_edge(first, label, headlabel=relation_numbers_to_str(first_relation_numbers),
        labelfontsize=relation_numbers_fontsize, labeldistance=2.0)
    graph.add_edge(second, label, headlabel=relation_numbers_to_str(second_relation_numbers),
        labelfontsize=relation_numbers_fontsize, labeldistance=2.0)

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
make_entity('Library')

# generalizations
make_generalization('Data', 'NumPy', 'CSV', 'XML')
make_generalization('Hardware', 'Cluster', 'Computer')

# attributes
make_attributes('Data', ['ID!', 'Name', 'Notes'])
make_attributes('Run', ['Date', 'Duration', 'RAM', 'ExitCode', 'Error', 'Notes'])
make_attributes('Hardware', ['MachineName!', 'RAM', 'CPU', 'OS', 'Libraries', 'Notes'])
make_attributes('Parameters', ['ID!', 'Tuple', 'Notes'])
make_attributes('Cluster', ['Nodes'])
make_attributes('NumPy', ['Shape', 'Dtype'])
make_attributes('Algorithm', ['GitCommit!', 'GitBranch', 'Notes'])
make_attributes('Library', ['Name!', 'Version!'])
available_label = make_attributes('Available', ['Path'], constraint=False)

# relations
make_relation('Supports', 'Parameters', 'Algorithm', (1,'N'), (1,'N'))
make_relation('Available', 'Data', 'Hardware', (0, 'N'), (0, 'N'))
make_relation('Uses', 'Run', 'Algorithm', (0, 'N'), (1, 1))
make_relation('On', 'Run', 'Data', (0, 1), (1, 1))
make_relation('Where', 'Run', 'Hardware', (0, 'N'), (1, 1))
make_relation('Returns', 'Run', 'Data', (0, 1), (0, 1))
make_relation('With', 'Run', 'Parameters', (0, 'N'), (1, 1))
make_relation('Fixes', 'Algorithm', 'Algorithm', (0, 1), (0, 1))
make_relation('Has', 'Hardware', 'Library', (0, 'N'), (0, 'N'))
make_relation('Needs', 'Algorithm', 'Library', (0, 'N'), (0, 'N'))
make_relation('Depends', 'Library', 'Library', (0, 'N'), (0, 'N'))

# random constraints
graph.add_edge('Data', available_label, style='invis')
graph.add_edge('Cluster', available_label, style='invis')

A = to_agraph(graph)
A.layout('dot')
A.graph_attr['nodesep'] = 10
A.graph_attr['dpi'] = 300
A.draw('res/schema_concettuale.png')
