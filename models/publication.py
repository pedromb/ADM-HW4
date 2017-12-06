'''
Model to represent a Publication
'''

class Publication:

    '''
    Class to represent a publication
    Args:
        id_str: string id of the publication
        id_int: integer id of the publication
        title: title of the publication
    '''

    def __init__(self, id_str: str, id_int: int, title: str):
        self.id_str = id_str
        self.id_int = id_int
        self.title = title

    def print(self):
        '''
        Print publication information
        '''
        print("Id: {}".format(self.id_str))
        print("Id Int: {}".format(self.id_int))
        print("Title: {}".format(self.title))

