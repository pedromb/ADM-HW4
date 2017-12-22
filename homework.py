'''
Module with functions to answer the questions on Homework 4
'''
import sys
import getopt
import json
from src.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def viz_subgraph_author(author_id: int, max_hop_dist: int, reduced: bool = False):
    '''
    Visualize the subgraph induced by nodes that have hop distance at most
    equal to max_hop_dist with author_id
    Args:
        author_id: The integer id of an author
        max_hop_dist: the maximum hop distance to create the subgraph
        reduced: If reduced equals true it will use the reduced data
            to create the graph, otherwise it will use the full data
    '''
    graph = Graph(reduced)
    subgraph, node_list = graph.get_subgraph_author(author_id, max_hop_dist)
    author_component = nx.node_connected_component(graph.graph, author_id)
    per = round((len(subgraph.nodes())/len(author_component))*100, 2)
    print("Percentage of component = {}".format(str(per)))
    pos = nx.fruchterman_reingold_layout(subgraph)
    legend_handles = []
    plt.figure(figsize=(16, 12))
    cmap = plt.cm.get_cmap('hsv', len(node_list)+1)
    for index, value in enumerate(node_list):
        color = cmap(index)
        if index == 0:
            label = "Root"
        else:
            label = 'Distance {}'.format(str(index))
        patch = mpatches.Patch(color=color, label=label)
        legend_handles.append(patch)
        nx.draw_networkx(subgraph, pos=pos, nodelist=value, node_color=color,
                         with_labels=False, node_size=100)
    plt.legend(handles=legend_handles)
    plt.show()

def aris_distance(author_id: int, reduced: bool = False):
    '''
    Gets the shortest distance between author_id and Aris
    Args:
        author_id: The integer id of an author
        reduced: If reduced equals true it will use the reduced data
            to create the graph, otherwise it will use the full data
    '''
    graph = Graph(reduced)
    author_name = graph.get_author_name(author_id)
    print("Getting shortest path weight between {} and Aris\n".format(author_name))
    path = graph.aris_distance(author_id)
    edge_labels = []
    if path is not None:
        aris_graph = nx.Graph()
        aris_graph.add_node(path[0][2])
        for i in range(0, len(path)-1):
            current = path[i]
            next_n = path[i+1]
            aris_graph.add_node(next_n[2])
            aris_graph.add_edge(current[2], next_n[2], {"weight":next_n[1]})
            edge_labels.append(((current[2], next_n[2]), round(abs(current[1]-next_n[1]), 2)))
        pos = nx.fruchterman_reingold_layout(aris_graph)
        cmap = plt.cm.get_cmap('hsv', len(path)+1)
        plt.figure(figsize=(16, 12))
        nx.draw_networkx_edge_labels(aris_graph, pos, edge_labels=dict(edge_labels))
        for index, value in enumerate(path):
            color = cmap(index)
            nx.draw_networkx(aris_graph, pos=pos, nodelist=[value[2]], node_color=color,
                             with_labels=True, node_size=1500)
        plt.title('Shortest path between Aris and {} = {}'\
            .format(author_name, str(round(path[-1][1], 4))))
        plt.show()
    else:
        print("There is no path between Aris and {}".format(author_name))

def group_numbers(nodes_list: list, reduced: bool = False):
    '''
    Sets the group numbers for the nodes on the graph and saves locally as
    a json file.
    The group number is the min shortest path between the node and the nodes
    on nodes_list.
    Args:
        nodes_list: an integer list with nodes id
        reduced: If reduced equals true it will use the reduced data
            to create the graph, otherwise it will use the full data
    '''
    graph = Graph(reduced)
    graph.set_group_number(nodes_list)
    with open("group_numbers.json", 'w') as jfile:
        json.dump(graph.group_numbers, jfile)
        print("group_numbers.json available under current directory\n")

def dispatcher(exercise: str, letter: str, reduced: bool):
    '''
    Dispatches functions to solve exercises
    Args:
        exercise: the number of the exercise as string
        letter: the letter of the exercise
        reduced: to use reduced data or not
    '''
    if exercise == '2' and letter == 'b':
        try:
            print("\nInput author id: ", end="")
            author_id = int(input())
            print("\nInput d: ", end="")
            max_hop_dist = int(input())
            viz_subgraph_author(author_id, max_hop_dist, reduced)
        except ValueError:
            print("Author id and d should be integers")
            sys.exit(0)
    elif exercise == '3' and letter == 'a':
        try:
            print("\nInput author id: ", end="")
            author_id = int(input())
            aris_distance(author_id, reduced)
        except ValueError:
            print("Author id should be integer")
            sys.exit(0)
    elif exercise == '3' and letter == 'b':
        try:
            print("Input nodes list as csv [eg.: 1,2,3,4]: ", end="")
            nodes_list = list(map(int, input().split(',')))
            group_numbers(nodes_list, reduced)
        except ValueError:
            print("nodes list should be a list of comma separated integers")
            sys.exit(0)
    else:
        message = "Exercise does not exist. If you tried exercise 1 you can \
just create a Graph object from the graph module. If you tried exercise 2/a, please \
check the exercise2a.ipynb notebook instead"
        print(message)

def main(argv):
    '''
    Main entry point to call modules/functions to solve the exercises
    '''
    exercise = ''
    letter = ''
    reduced = False
    try:
        opts, _ = getopt.getopt(argv, "he:l:r:",
                                ["exercise=", "letter=", "reduced="])
    except getopt.GetoptError:
        print('homework.py -e <exercise> -l <letter> -r <reduced>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-e', '--exercise'):
            exercise = arg
        elif opt in ('-l', '--letter'):
            letter = arg
        elif opt in ('-r', '--reduced'):
            if arg.lower() in ('1', 'true', 't'):
                reduced = True
            elif arg.lower() in ('0', 'false', 'f'):
                reduced = False
    if not exercise or not letter:
        print('homework.py -e <exercise> -l <letter> -r <reduced>')
        sys.exit(2)
    dispatcher(exercise, letter, reduced)

if __name__ == '__main__':
    main(sys.argv[1:])
