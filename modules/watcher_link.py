class Cell():
    def __init__(self) -> None:
        pass


class Watcher_link():
    def __init__(self) -> None:
        self.storage = []
        self.len_storage = 0

    def expand_storage(self):
        pass

    def reduce_storage(self, condition):
        pass

if  __name__ == '__main__':
    watcher = Watcher_link()
    watcher.expand_storage()
    print(watcher.storage , '\n', len(watcher.storage))


