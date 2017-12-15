'''
Module with functions to answer the questions on Homework 4
'''
import sys
import getopt
import json
from src.graph import Graph
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def viz_centralities_conf(conf_id: int, reduced: bool = False):
    '''
    Visualize the centralities from the subgraph induced by the set
    of authors who published at conf_id
    Args:
        conf_id: The integer id of the conference to geneate the subgraph
        reduced: If reduced equals true it will use the reduced data
            to create the graph, otherwise it will use the full data
    '''
    graph = Graph(reduced)
    subgraph = graph.get_subgraph_conf(conf_id)
    degree, closeness, betweenness = graph.get_centralities(subgraph)
    raise NotImplementedError

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
    pos = nx.fruchterman_reingold_layout(subgraph)
    legend_handles = []
    plt.figure(figsize=(16, 12))
    for index, value in enumerate(node_list):
        color = np.random.rand(3,)
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
    print("Getting shortest path weight between {} and Aris\n"\
        .format(str(author_id)))
    return graph.aris_distance(author_id)

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

def dispatcher(exercise:str, letter:str, reduced:bool):
    '''
    Dispatches functions to solve exercises
    Args:
        exercise: the number of the exercise as string
        letter: the letter of the exercise
        reduced: to use reduced data or not
    '''
    if exercise == '2' and letter == 'a':
        try:
            print("\nInput conference id: ", end="")
            conf_id = int(input())
            viz_centralities_conf(conf_id, reduced)
        except ValueError:
            print("Conferece id should be an integer")
            sys.exit(0)
    elif exercise == '2' and letter == 'b':
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
            dist = aris_distance(author_id, reduced)
            print("Shortest path between {} and Aris has weight = {}\n"\
                .format(str(author_id), str(dist)))
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
just create a Graph object from the graph module."
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
