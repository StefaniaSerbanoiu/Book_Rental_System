# Book: book_id, title, author

class Book:
    def __init__(self, book_id=0, title="n/a", author="n/a"):
        self.__book_id = book_id
        self.__title = title
        self.__author = author

    @property
    def book_id(self):
        return self.__book_id

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    def set_book_id(self, new_id):
        if not isinstance(new_id, int):
            raise ValueError("The id must be an integer number!!!")
        else:
            self.__book_id = new_id

    def set_title(self, new_title):
        self.__title = new_title

    def set_author(self, new_author):
        if all(character.isalpha() or character.isspace() for character in new_author):
            self.__author = new_author
        else:
            raise ValueError("The name of the author must be a string and contain only letters!!!")

    def __str__(self):
        return '{self._Book__title} by {self._Book__author} has the id {self._Book__book_id}.'.format(self=self)

