# Client: client_id, name

class Client:
    def __init__(self, client_id=0, name="n/a"):
        self.__client_id = client_id
        self.__name = name

    @property
    def client_id(self):
        return self.__client_id

    @property
    def name(self):
        return self.__name

    def set_name(self, new_name):
        if all(character.isalpha() or character.isspace() for character in new_name):
            self.__name = new_name
        else:
            raise ValueError("The name must be a string and contain only letters!!!")

    def __str__(self):
        return '{self._Client__name} has the client id {self._Client__client_id}.'.format(self=self)
