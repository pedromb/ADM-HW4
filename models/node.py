'''
Model to represent a node in the graph
'''
from author import Author
from publication import Publication
from conference import Conference

class Node:
    '''
    Class to represent a node in the graph
    Args:
        author: author
    '''

    def __init__(self, author: Author):
        self.author = author
        self.publications = {}
        self.conferences = {}

    def add_publication(self, pub: Publication):
        '''
        Adds a publication to the node publications dictionary
        Args:
            pub: publication to be added to the node
        '''
        self.publications[pub.id_int] = pub

    def add_conference(self, conf: Conference):
        '''
        Adds a conference to the node conferences dictionary
        Args:
            conf: conference to be added to the node
        '''
        self.conferences[conf.id_int] = conf

    def print(self):
        '''
        Print node information
        '''
        print("-----Author-----")
        print(self.author.print())
        print("----Publications----")
        for _, value in self.publications.items():
            value.print()
        print("----Conference----")
        for _, value in self.conferences.items():
            value.print()
        print()
