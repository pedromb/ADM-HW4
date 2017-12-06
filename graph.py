'''
Module to create and manipulate the graph
'''
import json
import pickle
import networkx as nx
from conf import *
from models.author import Author
from models.publication import Publication
from models.conference import Conference
from models.node import Node
import tqdm

class Graph():
    '''
    Class to create and manipulate a graph using the NetworkX package
    '''

    def __init__(self, reduced = False, full = True):
        if reduced:
            try:
                self._load_graph(reduced)
            except:
                self._create_graph(RED_DATA, True)
        if full:
            try:
                self._load_graph(False)
            except:
                self._create_graph(FULL_DATA, False)
            
        
    def _create_graph(self, data_path, reduced = False):
        
        with open(data_path) as data_file:
            data = json.load(data_file)
            
        graph = nx.Graph()
        
        for entry in tqdm.tqdm(data, desc="Creating graph..."):
            
            conference = {
                    "id_str":entry["id_conference"],
                    "id_int":entry["id_conference_int"]
            }
            publication = {
                    "id_str": entry["id_publication"],
                    "id_int": entry["id_publication_int"],
                    "title": entry["title"]
            }
            nodes_id = []
            
            for author in entry["authors"]:
                try:
                    node = graph.node[author["author_id"]]["data"]
                except:
                    new_author = {
                            "name": author["author"],
                            "id": author["author_id"]
                    }
                    node = {
                            "author": new_author,
                            "publications": {},
                            "conferences": {}
                    }

                    graph.add_node(new_author['id'], data = node)
                    
                node['publications'][publication['id_int']] = publication
                node['conferences'][conference['id_int']] = conference
                
                if nodes_id:
                    for node_id in nodes_id:
                        graph.add_edge(node_id, author["author_id"], weight = None)
                nodes_id.append(author["author_id"])
        
        if reduced:
            self.red_graph = graph
        else:
            self.graph = graph

        self._add_weights(reduced)
        self._save_graph(reduced)
        

    def _add_weights(self, reduced = False):
        if reduced:
            _graph = self.red_graph
        else:
            _graph = self.graph
        edges_ids = _graph.edges()
        for node_id1, node_id2 in tqdm.tqdm(edges_ids, desc = "Adding weights..."):
            node1 = _graph.node[node_id1]["data"]
            node2 = _graph.node[node_id2]["data"]
            jaccard = self._jaccard_sim(node1, node2)
            _graph[node_id1][node_id2]["weight"] = jaccard

    def _jaccard_sim(self, node1, node2):
        pubs1 = set(node1['publications'].keys())
        pubs2 = set(node2['publications'].keys())
        jaccard = 1 - (len(pubs1.intersection(pubs2))/len(pubs1.union(pubs2)))
        return jaccard
    
    def _save_graph(self, reduced = False):
        filename = RED_GRAPH if reduced else GRAPH
        _graph = self.red_graph if reduced else self.graph
        with open(filename, 'wb') as output:
            pickle.dump(_graph, output, pickle.HIGHEST_PROTOCOL)
    
    def _load_graph(self, reduced = False):
        filename = RED_GRAPH if reduced else GRAPH
        with open(filename, 'rb') as input_graph:
            _graph = pickle.load(input_graph)
            if reduced:
                self.red_graph = _graph
            else:
                self.graph = _graph