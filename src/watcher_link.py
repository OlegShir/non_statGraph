###################################################
#                     coloumn(in)                 #
# row(out)     0        1        2        3       #
#         +--------+--------+--------+--------+   #
#   0     | False  | Bezier | Bezier | False  |   #
#         +--------+--------+--------+--------+   #
#   1     | False  | Bezier | False  | Bezier |   #
#         +--------+--------+--------+--------+   #
#   2     | False  | False  | False  | False  |   #
#         +--------+--------+--------+--------+   #
#   3     | Bezier | False  | False  | False  |   #
#         +--------+--------+--------+--------+   #
#                                                 #
#   storage =[                                    #
#            [False, Bezier, Bezier, False],      #
#            [False, Bezier, False, Bezier],      #
#            [False, False, False, False],        #
#            [Bezier, False, False, False]        #
#            ]                                    #
###################################################

from settings import DEBUG
import copy


def _logger(func):
    '''Логгер отслеживания состояния хранилища'''
    def wrapper(*args, **kwargs):
        rezult = func(*args, **kwargs)
        if DEBUG:
            zip = '-'
            print(f'Storage: {args[0].storage}', '\n',
                  f'Len: {args[0].len_storage}', '\n', f'{zip*25}')
        return rezult
    return wrapper


class Watcher_link():
    def __init__(self) -> None:
        self.storage = []
        self.len_storage = 0

    @_logger
    def expand_storage(self):
        '''Увеличение хранилища.'''
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
        '''Уменьшение хранилища.'''
        inner, outer = self.get_list_of_bezie(index)
        if index < self.len_storage:
            for row in self.storage:
                row.pop(index)
            self.storage.pop(index)
        self.len_storage -= 1
        return inner, outer

    @_logger
    def add_link_in_storage(self, out_condition: int, in_condition: int, link) -> bool:
        '''Добавление связи в хранилище.'''
        if self.storage[out_condition][in_condition] == False:
            self.storage[out_condition][in_condition] = link
            return True
        else:
            return False

    def get_conditions_index(self, link):
        '''Получение индексов состояний соединенной линий Безье (link).'''
        def index_storage():
            for i in range(len(self.storage)):
                for j in range(len(self.storage[i])):
                    yield i, j
        for i, j in index_storage():
            if self.storage[i][j] == link:
                break
        return i, j

    def get_ful_conditions_index(self, links: list) -> set:
        '''Получение всех индексов состояний соединенных линиями Безье (links).'''
        indexs_conditions: list = []
        for link in links:
            for i in range(len(self.storage)):
                for j in range(len(self.storage[i])):
                    if self.storage[i][j] == link:
                        indexs_conditions.extend([i, j])
        indexs_conditions = set(indexs_conditions)
       
        return indexs_conditions

    @_logger
    def del_link_in_storage(self, link):
        '''Удаление связи в хранилище.'''
        i, j = self.get_conditions_index(link)
        self.storage[i][j] = False
        return i, j

    def change_element_in_storage(self, new_condition: int, link, direction: str) -> None:
        '''Изменение связи в хранилище.'''
        i, j = self.del_link_in_storage(link)
        if direction == 'in':
            in_condition = new_condition
            out_condition = i
            print('in', out_condition, in_condition)
        else:
            in_condition = j
            out_condition = new_condition
        self.add_link_in_storage(out_condition, in_condition, link)

    def get_list_of_bezie(self, index: int):
        '''Получение списка входящих и исходящих 
        линий Безье из состояния index.'''
        inner = []
        outer = []
        for row in self.storage:
            if row[index] != False:
                inner.append(row[index])
        for val in self.storage[index]:
            if val != False:
                outer.append(val)
        return outer, inner

    def export_storage(self) -> list:
        '''Медод экстортирует значения законов распределения в новый список.

           Так как объекты в storage являются сложными и написаны на Cython,
           (not deepcopy) создается новое пустое хранилище и затем заполняется'''
        new_storage: list = []
        size = self.len_storage
        for _ in range(size):
            new_storage.append([False]*size)
        for i in range(len(self.storage)):
            for j in range(len(self.storage[i])):
                if self.storage[i][j]:
                    new_storage[i][j] = copy.deepcopy(
                        self.storage[i][j].law_param)
        return new_storage
