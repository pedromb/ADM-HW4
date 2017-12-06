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
        pubs: dictionary of publications for the author (id_int should be key)
        confs: dictionary of conferences for the author (id_int should be key)
    '''

    def __init__(self, author: Author, pubs: Publication=None,
                 confs: Conference=None):
        self.author = author
        self.publications = pubs
        self.conferences = confs

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
