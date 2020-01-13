class Licitacao:
    __data = {}

    def __init__(self, data: dict):
        self.__data = data

    @property
    def data(self) -> dict:
        return self.__data
