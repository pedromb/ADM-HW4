'''
Model to represent a Conference
'''

class Conference:

    '''
    Class to represent a conference
    Args:
        id_str: string id of the conference
        id_int: integer id of the conference
    '''

    def __init__(self, id_str: str, id_int: int):
        self.id_str = id_str
        self.id_int = id_int

    def print(self):
        '''
        Print conference information
        '''
        print("Id: {}".format(self.id_str))
        print("Id Int: {}".format(self.id_int))

  
