'''
Module to create and manipulate the graph
Set configurations on the conf.py file
'''
import sys
import json
import pickle
import heapq as hp
import tqdm
import networkx as nx
from src.conf import FULL_DATA, RED_DATA, GRAPH, RED_GRAPH

class Graph():

    '''
    Class to create and manipulate a graph using the NetworkX package
    The graph object is accessible through the graph attribute
    Args:
        reduced: If reduced equals true it will use the reduced data
            to create the graph, otherwise it will use the full data
    '''

    def __init__(self, reduced: bool = False):
        try:
            print("\nTrying to load graph from local file")
            self.graph = self.__load_graph(reduced)
            print("\nGraph loaded\n")
        except FileNotFoundError:
            print("\nGraph not found, will create graph from dataset\n")
            data = RED_DATA if reduced else FULL_DATA
            self.graph = self.__create_graph(data, reduced)
            self.__save_graph(reduced)
            print("\nFinished\n")
        self.group_numbers = {}

    def __create_graph(self, data_path: str, reduced: bool = False):
        '''
        Function to create the graph using NetworkX.
        The graph object will be accesible on the graph attribute
        Args
            data_path: The path to the json file with the graph data
        '''
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
                except KeyError:
                    new_author = {
                        "name": author["author"],
                        "id": author["author_id"]
                    }
                    node = {
                        "author": new_author,
                        "publications": {},
                        "conferences": {}
                    }

                    graph.add_node(new_author['id'], data=node)

                node['publications'][publication['id_int']] = publication
                node['conferences'][conference['id_int']] = conference

                if nodes_id:
                    for node_id in nodes_id:
                        graph.add_edge(node_id, author["author_id"], weight=None)
                nodes_id.append(author["author_id"])

        graph = self.__add_weights(graph)
        return graph


    def __add_weights(self, graph):
        '''
        Function to add weights to the graph object.
        The weights are added as 1 - jaccard similarity between two connected nodes
        '''
        edges_ids = graph.edges()
        for node_id1, node_id2 in tqdm.tqdm(edges_ids, desc="Adding weights..."):
            node1 = graph.node[node_id1]["data"]
            node2 = graph.node[node_id2]["data"]
            weight = self.__weight(node1, node2)
            graph[node_id1][node_id2]["weight"] = weight
        return graph

    def __weight(self, node1, node2):
        '''
        Calculates 1 - jaccard similarity between two nodes.
        The jaccard similarity is calculated as the number of publications in common
        divided by the number of total publications between two authors.
        Args
            node1: A node from a NetworkX graph
            node2: A node from a NetworkX graph
        Returns:
            1 - jaccard similarity between node1 and node2
        '''
        pubs1 = set(node1['publications'].keys())
        pubs2 = set(node2['publications'].keys())
        weight = 1 - (len(pubs1.intersection(pubs2))/len(pubs1.union(pubs2)))
        return weight

    def get_subgraph_conf(self, conference_id: int):
        '''
        Gets the sugraph induced by the set of authors who published at
        conference_id
        Args:
            conference_id: The integer id of a conference
        Returns:
            A NetworkX Graph object
        '''
        subgraph_ids = []
        for node in self.graph.nodes(data=True):
            data = node[1]['data']
            conferences = data['conferences']
            try:
                _ = conferences[conference_id]
                subgraph_ids.append(node[0])
            except KeyError:
                pass
        subgraph = self.graph.subgraph(subgraph_ids)
        return subgraph

    def get_subgraph_author(self, author_id: int, max_hop_dist: int):
        '''
        Gets the subgraph induced by nodes that have hop distance at most
        equal to max_hop_dist with author_id
        Args:
            author_id: The integer id of an author
            max_hop_dist: the maximum hop distance to create the subgraph
        Returns:
            A tuple with a NetworkX Graph object and the list of nodes
            on the graph
        '''
        if not self.__check_node(author_id):
            sys.exit(2)
        author_ids = [author_id]
        subgraph_ids = [author_id]
        node_list = [[author_id]]
        for _ in range(max_hop_dist):
            edges = []
            for aut_id in author_ids:
                edges.extend(list(self.graph[aut_id].keys()))
            author_ids = list(set(edges).difference(set(subgraph_ids)))
            node_list.append(list(set(author_ids)))
            subgraph_ids.extend(author_ids)
        subgraph = self.graph.subgraph(subgraph_ids)
        return subgraph, node_list

    def aris_distance(self, author_id: int):
        '''
        Gets the shortest distance between author_id and Aris
        Args:
            author_id: The integer id of an author
        Returns:
            A path as a tuple where element 0 is the author id, 
            element 1 is the distance between the author and aris
            and element 2 is the authors name.
            If author_id does not exist on graph it returns None
        '''

        aris_node = None
        # Find Aris
        for node in self.graph.nodes():
            author_name = self.graph.node[node]['data']['author']['name']
            if author_name.lower() == 'aris anagnostopoulos':
                aris_node = node
                break
        if aris_node is None:
            print('Aris not found')
            return None
        distances, prev = self.shortest_path(start=aris_node, finish=author_id, graph=self.graph)
        if prev is not None:
            try:
                prev[author_id]
            except KeyError:
                return None
            path = [(author_id, distances[author_id], self.get_author_name(author_id))]
            control = prev[author_id]
            while control != aris_node:
                aut_name = self.get_author_name(control)
                path.append((control, distances[control], aut_name))
                control = prev[control]
            path.append((aris_node, 0, 'Aris Anagnostopoulos'))
            return path[::-1]
        else:
            return None

    def shortest_path(self, start: int, graph: nx.Graph, finish=None):
        '''
        Dijkstra algorithm for finding the shortest path.
        If finish is not set it finds the the shortest path between start and
        all the other nodes in graph.
        Args:
            start: The root node to find the shortest path from
            graph: The graph object to look for the shortest path
            finish (int): The destination node to find the shortest path
        Returns:
            A tuple where element 0 dict is the shortest path between start
            and all the other nodes, and element 1 is a dict with the node as
            a key and the value is the previous node on the path to that node.
            If finish is given the iteration stops when finds finish but it still
            returns the same tuple
        '''

        distances = {}
        prev = {}
        for node in graph.nodes():
            distances[node] = float('inf')
        distances[start] = 0
        if not self.__check_node(start) or finish is not None and not self.__check_node(finish):
            return distances, None
        p_queue = []
        hp.heappush(p_queue, (0, start))
        visited = set()
        while p_queue:
            dist, node = hp.heappop(p_queue)
            if finish is not None:
                if node == finish:
                    return distances, prev
            if node not in visited:
                visited.add(node)
                for edge in graph.edges(node, data=True):
                    neighbour = edge[1]
                    weigth = edge[2]['weight']
                    _dist = dist + weigth
                    if _dist < distances[neighbour]:
                        distances[neighbour] = _dist
                        prev[neighbour] = node
                    if neighbour not in visited:
                        hp.heappush(p_queue, (_dist, neighbour))
        return distances, prev

    def set_group_number(self, nodes_list: list):
        '''
        Sets the group numbers for the nodes on the graph.
        The group numbers can be accessed on the group_numbers attribute
        The group number is the min shortest path between the node and the nodes
        on nodes_list.
        Args:
            nodes_list: an integer list with nodes id
        '''
        self.group_numbers = {}
        nodes_list = [node for node in nodes_list if self.__check_node(node)]
        nodes = self.graph.nodes()
        dists = []
        for sub_node in tqdm.tqdm(nodes_list, desc="Setting group numbers..."):
            distances, _ = self.shortest_path(start=sub_node, graph=self.graph)
            dists.append(distances)
        for node in nodes:
            self.group_numbers[node] = min([dist[node] for dist in dists]) \
                if nodes_list else float('inf')
        print("Finished\n")

    def get_centralities(self, graph: nx.Graph):
        '''
        Gets centralities measures from a NetworkX graph object.
        Args:
            graph: The graph to get the measures from
        Returns:
            A tuple of dictionaries with degree, closeness and
            betweenness centralities for each on graph
        '''
        degree = nx.degree(graph)
        closeness = nx.closeness_centrality(graph)
        betweenness = nx.betweenness_centrality(graph)
        return degree, closeness, betweenness

    def __save_graph(self, reduced: bool = False):
        '''
        Saves the graph object locally for later reuse
        Args:
            reduced: If the graph being save is the reduced one or not
        '''
        filename = RED_GRAPH if reduced else GRAPH
        with open(filename, 'wb') as output:
            pickle.dump(self.graph, output, pickle.HIGHEST_PROTOCOL)

    def __load_graph(self, reduced: bool = False):
        '''
        Loads the graph object from local folder
        Args:
            reduced: If the graph being loaded is the reduced one or not
        Return:
            The graph object
        '''
        filename = RED_GRAPH if reduced else GRAPH
        with open(filename, 'rb') as input_graph:
            return pickle.load(input_graph)
    
    def __check_node(self, node: int):
        '''
        Check if node exists on graph.
        Args:
            node: id of the node to be checked
        Return:
            True if node exists on graph, false otherwise
        '''
        try:
            self.graph.node[node]
            return True
        except KeyError:
            print("Author id {} does not exist on graph".format(str(node)))
            return False

    def get_author_name(self, author_id: int):
        '''
        Get author name from graph
        Args:
            author_id: id of the author
        Return:
            The name of the author as a string
        '''
        return self.graph.node[author_id]['data']['author']['name'].title()
