'''
Model to represent a node in the graph
'''
from models.author import Author
from models.publication import Publication
from models.conference import Conference

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
