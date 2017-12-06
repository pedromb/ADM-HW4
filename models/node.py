'''
Model to represent a node in the graph
'''
from author import Author
from publication import Publication
from conference import Conference

class Node:
    '''
    Class to represent a node in the graph
    '''

    def __init__(self, author: Author, publication: Publication, conference: Conference):
        self.author = author
        self.publication = publication
        self.conference = conference
