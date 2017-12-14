'''
Module to create and manipulate the graph
'''
import json
import pickle
import heapq as hp
import networkx as nx
from conf import *
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
    
    def get_subgraph_conf(self, conference_id: int, reduced=False):
        _graph = self.red_graph if reduced else self.graph
        subgraph_ids = []
        for node in _graph.nodes(data=True):
            data = node[1]['data']
            conferences = data['conferences']
            try:
                _ = conferences[conference_id]
                subgraph_ids.append(node[0])
            except KeyError:
                pass
        subgraph = _graph.subgraph(subgraph_ids)
        return subgraph

    def get_subgraph_author(self, author_id: int, d: int,reduced=False):
        _graph = self.red_graph if reduced else self.graph
        author_ids = [author_id]
        subgraph_ids = []
        node_list = [[author_id]]
        set_author_id = set(node_list[0])
        for i in range(d):
            edges = []
            for aut_id in author_ids:
                edges.extend(list(_graph[aut_id].keys()))
            author_ids = list(set(edges))
            node_list.append(list(set(author_ids).difference(set_author_id)))
            subgraph_ids.extend(author_ids)
            set_author_id = set_author_id.union(set(author_ids))
        subgraph = _graph.subgraph(subgraph_ids)
        return subgraph, node_list


    def _get_edges(self, author_id: int, d: int, reduced=False):
        _graph = self.red_graph if reduced else self.graph
        subgraph = []
        edges = list(_graph.graph[author_id].keys())
        if d == 0:
            return edges
        else:
            for edge in edges:
                subgraph.append(self._get_edges(edge, d-1, reduced))
        return subgraph

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

    def aris_distance(self, reduced = False, author_id = -1):
        _graph = self.graph if not reduced else self.red_graph
        aris = None
        # Find Aris
        for node in _graph.nodes():
            author_name = _graph.node[node]['data']['author']['name']
            if 'aris anagnostopoulos' == author_name.lower():
                aris = node
                break
        if aris is None:
            print('Aris not found')
            return None
        dist = self._shortest_path(start=author_id, finish = aris, graph=_graph)
        return dist

    def _shortest_path(self, start = None, finish = None, graph = None):
        distances = {}
        for node in graph.nodes():
            if node == start:
                distances[node] = 0
            else:
                distances[node] = float('inf')
        p_queue = []
        hp.heappush(p_queue, (0, start))
        visited = set()
        while p_queue:
            dist, node = hp.heappop(p_queue)
            if finish is not None:
                if node == finish:
                    return dist
            if node not in visited:
                visited.add(node)
                for edge in graph.edges(node, data=True):
                    neighbour = edge[1]  
                    weigth = edge[2]['weight']
                    _dist = dist + weigth
                    if _dist < distances[neighbour]:
                        distances[neighbour] = _dist
                    if neighbour not in visited:
                        hp.heappush(p_queue, (_dist, neighbour))
        return distances

    def set_group_number(self, nodes_list = None, reduced = False):
        _graph = self.graph if not reduced else self.red_graph
        nodes = _graph.nodes()
        self.group_numbers_red = {}
        self.group_numbers = {}
        _group_numbers = self.group_numbers if not reduced else self.group_numbers_red
        dists = []
        for sub_node in tqdm.tqdm(nodes_list):
            distances = self._shortest_path(start=sub_node, graph=_graph)
            dists.append(distances)
        for node in nodes:
            _group_numbers[node] = min([dist[node] for dist in dists])
    
    def get_centralities(self, reduced=False, graph=None):
        degree = nx.degree_centrality(graph) 
        closeness = nx.closeness_centrality(graph)
        betweenness = nx.betweenness_centrality(graph)
        return degree, closeness, betweenness

    def _get_graph(self, reduced=False):
        return self.graph if not reduced else self.red_graph
            