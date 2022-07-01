###################################################
#                     coloumn(in)                 #  
# row(out)     0        1        2        3       #
#         +--------+--------+--------+--------+   #
#   0     |  None  | Bezier | Bezier |  None  |   #
#         +--------+--------+--------+--------+   #
#   1     |  None  | Bezier |  None  | Bezier |   #
#         +--------+--------+--------+--------+   #
#   2     |  None  |  None  |  None  |  None  |   #
#         +--------+--------+--------+--------+   #
#   3     | Bezier |  None  |  None  |  None  |   #
#         +--------+--------+--------+--------+   #
#                                                 #
#   storage =[                                    #              
#            [Non,Bezier,Bezier,None],            #
#            [None, Bezier, None, Bezier],        #
#            [None, None, None, None],            #
#            [Bezier, None, None, None]           #
#            ]                                    #
###################################################

from numpy import outer


def _logger(func):
    def wrapper(*args, **kwargs):
        rezult = func(*args, **kwargs)
        zip = '-'
        print(f'Storage: {args[0].storage}', '\n', f'Len: {args[0].len_storage}', '\n', f'{zip*25}')
        return rezult
    return wrapper

class Watcher_link():
    def __init__(self) -> None:
        self.storage = []
        self.len_storage = 0

    @_logger
    def expand_storage(self):
        '''Увеличение хранилища'''
        bimbo = False
        if not self.storage:
            self.storage.append([bimbo])
        else:
            for row in self.storage:
               row.append(bimbo)
            self.storage.append([bimbo]*(self.len_storage+1))
        self.len_storage += 1
    
    @_logger   
    def reduce_storage(self, index: int):
        '''Уменьшение хранилища'''
        if index < self.len_storage:
            for row in self.storage:
                row.pop(index)
            self.storage.pop(index)
        self.len_storage -= 1

    @_logger
    def add_link_in_storage(self, out_condition, in_condition, link):
        '''Добавление связи в хранилище'''
        if self.storage[out_condition][in_condition] == False:
            self.storage[out_condition][in_condition] = link
            return True
        else:
            return False

    @_logger
    def del_link_in_storage(self, link):
        '''Удаление связи в хранилище'''
        for i in self.storage:
            for j in self.storage[i]:
                if self.storage[i][j] == link:
                    break
        self.storage[i][j] = False

    def get_list_of_bezie(self, index):
        inner = []
        outer = []
        for row in self.storage:
            if row[index] != False:
                inner.append(row[index])
        for val in self.storage[index]:
            if val != False:
                outer.append(val)
        return outer, inner

