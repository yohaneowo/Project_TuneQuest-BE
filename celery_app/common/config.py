class Config:
    def __init__(self):
        self.__dbName = 'pass'
        pass

    @property
    def dbName(self):
        return self.__dbName

config = Config()