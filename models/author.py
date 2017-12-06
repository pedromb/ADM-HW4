'''
Model to represent an Author
'''

class Author:

    '''
    Class to represent an author
    Args:
        name: name of the author
        id_int: id of the author
    '''

    def __init__(self, name: str, id_int: int):
        self.name = name
        self.id_int = id_int

    def print(self):
        '''
        Print author information
        '''
        print("Name: {}".format(self.name))
        print("Id: {}".format(str(self.id_int)))
