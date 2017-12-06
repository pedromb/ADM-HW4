'''
Model to represent an Author
'''

class Author:

    '''
    Class to represent an author
    Args:
        name: name of the author
        id: id of the author
    '''

    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id