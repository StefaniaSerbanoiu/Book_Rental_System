from datetime import date

from src.domain.Book import Book
from src.domain.Client import Client
from src.domain.Rental import Rental
from src.IterableDataStructure import *

import pickle


class RepositoryException(Exception):
    pass


class BookRepository:
    def __init__(self):
        self.books = IterableEntity(list())

    def find_by_id(self, book_id):
        index = 0
        for item in self.books:
            if item.book_id == book_id:
                return item
            index += 1
        return None

    def get_index_by_id(self, book_id):
        index = 0
        for item in self.books:
            if item.book_id == book_id:
                return item, index
            index += 1
        return None

    def add_book(self, book):
        if self.find_by_id(book.book_id) is None:
            self.books.append(book)
        else:
            raise RepositoryException("Book already exists.")

    def remove(self, book_id):
        book_to_remove = self.find_by_id(book_id)
        index = self.get_index_by_id(book_id)
        if index is not None:
            self.books.remove(book_to_remove)  # ->  when not using the iterable structure
            # del self.books[index]

    def remove1(self, book_id):
        #this function is a copy
        book_to_remove = self.find_by_id(book_id)
        index = self.get_index_by_id(book_id)
        if index is not None:
            self.books.remove(book_to_remove)  # ->  when not using the iterable structure
            # del self.books[index]

    def update_book(self, book_id, new_book):
        book_to_update, index = self.get_index_by_id(book_id)
        if book_to_update is not None:
            self.books[index] = new_book

    def print_list_of_books(self):
        # book in self.__books:
        # print(book)

        books_to_print = list()
        for book in self.books:
            books_to_print.append(str(book))
        return books_to_print

    def __getitem__(self, item):
        return self.books[item]

    def __setitem__(self, key, value):
        self.books[key] = value

    def get_all(self):
        return self.books

    def __len__(self):
        return len(self.books)

    def str(self):
        books_to_print = self.print_list_of_books()
        return books_to_print


class BookBinFileRepository(BookRepository):
    def __init__(self):
        super().__init__()

        self._file_name = "books.bin"
        # self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        # self.books = pickle.load(file)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(self.books, file)
        file.close()

    def add_book(self, book):
        super(BookBinFileRepository, self).add_book(book)
        self._save_file()

    def remove(self, book_id):
        super(BookBinFileRepository, self).remove(book_id)
        self._save_file()

    def update_book(self, book_id, new_book):
        super(BookBinFileRepository, self).update_book(book_id, new_book)


class BookFileRepository(BookRepository):
    def __init__(self):
        super().__init__()

        self._file_name = "books.txt"
        # self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rt")

        list_to_read = file.readlines()
        for line in list_to_read:
            book_id, title, author = line.split(sep=',')
            new_book = Book(int(book_id), title, author)
            self.add_book(new_book)

        file.close()

    def _save_file(self):
        file = open(self._file_name, "wt")

        for book in self.books:
            file.write(book.title + " by " + book.author + "-> id " + str(book.book_id) + "\n\n")

    def add_book(self, book):
        super(BookFileRepository, self).add_book(book)
        self._save_file()

    def remove(self, book_id):
        super(BookFileRepository, self).remove(book_id)
        self._save_file()

    def update_book(self, book_id, new_book):
        super(BookFileRepository, self).update_book(book_id, new_book)
        self._save_file()


class RentalRepository:
    def __init__(self):
        self._rental_list = IterableEntity(list())

    def returned_date(self, index):
        return self._rental_list[index].__returned_date

    def returned_date_function(self, index):
        pass

    def __getitem__(self, index_of_rental):
        return self._rental_list[index_of_rental]

    def __len__(self):
        return len(self._rental_list)

    def find_by_id(self, rental_id):
        index = 0
        for item in self._rental_list:
            if item.rental_id == rental_id:
                return item
            index += 1
        return None

    def get_index_by_id(self, rental_id):
        index = 0
        for item in self._rental_list:
            if item.rental_id == rental_id:
                return index
            index += 1
        return None

    def get_rental_id_by_book_id(self, book_id):
        index = 0
        for rental in self._rental_list:
            if rental.book_id == book_id:
                return rental.rental_id
            index += 1
        return None

    def get_rental_id_by_book_id_and_client_id(self, book_id, client_id):

        for rental in self._rental_list:
            if rental.book_id == book_id and rental.client_id == client_id:
                return rental.rental_id

    def get_last_rental_id_by_book_id_and_client_id(self, book_id, client_id):
        rental_to_return = None

        for rental in self._rental_list:
            if rental.book_id == book_id and rental.client_id == client_id:
                rental_to_return = rental.rental_id

        return rental_to_return

    def add_rental(self, rental):
        if self.find_by_id(rental.rental_id) is None:
            self._rental_list.append(rental)
        else:
            raise RepositoryException("Rental already exists.")

    def get_rental_count_by_book_id(self, book_id):
        index = 0
        rental_count = 0
        for rental in self._rental_list:
            if rental.book_id == book_id:
                rental_count += 1
            index += 1
        return rental_count

    def delete_rental(self, book_id, client_id):
        rental_to_remove = self.find_by_id(self.get_last_rental_id_by_book_id_and_client_id(book_id, client_id))
        if rental_to_remove is not None:
            self._rental_list.remove(rental_to_remove)

    def print_list_of_rentals(self):
        rentals_to_print = list()
        for rental in self._rental_list:
            rentals_to_print.append(str(rental))
        return rentals_to_print


class RentalBinFileRepository(RentalRepository):
    def __init__(self):
        super().__init__()

        self._file_name = "rentals.bin"
        # self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        # self._rental_list = pickle.load(file)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(self._rental_list, file)
        file.close()

    def add_rental(self, rental):
        super(RentalBinFileRepository, self).add_rental(rental)
        self._save_file()

    def delete_rental(self, book_id, client_id):
        super(RentalBinFileRepository, self).delete_rental(book_id, client_id)
        self._save_file()

    def returned_date_function(self, index):
        super(RentalBinFileRepository, self).returned_date_function(index)
        self._save_file()


class RentalFileRepository(RentalRepository):
    def __init__(self):
        super().__init__()

        self._file_name = "rentals.txt"
        # self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rt")
        """
        lines_from_file = file.readlines()
        for line in lines_from_file:
            rental_id, book_id, client_id, rented_year, rented_month, rented_day, returned_year, returned_month, returned_day = line.split(sep=',')
            rental_id = int(rental_id)
            book_id = int(book_id)
            client_id = int(client_id)
            rented_year = int(rented_year)
            rented_month = int(rented_month)
            rented_day = int(rented_day)
            returned_year = int(returned_year)
            returned_month = int(returned_month)
            returned_day = int(returned_day)
            rented_date = date(rented_year, rented_month, rented_day)
            returned_date = date(returned_year, returned_month, returned_day)
            new_rental = Rental(rental_id, book_id, client_id, rented_date, returned_date)
            self.add_rental(new_rental)
        """
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wt")

        for rental in self._rental_list:
            if rental.returned_date == date(1, 1, 1):
                file.write(str(rental) + "\n\n")
            else:
                file.write(str(rental) + "\n\n")

    def add_rental(self, rental):
        super(RentalFileRepository, self).add_rental(rental)
        self._save_file()

    def delete_rental(self, book_id, client_id):
        super(RentalFileRepository, self).delete_rental(book_id, client_id)
        self._save_file()

    def returned_date_function(self, index):
        super(RentalFileRepository, self).returned_date_function(index)
        self._save_file()


class ClientRepository:
    def __init__(self):
        self._client_list = IterableEntity(list())

    def find_client_by_id(self, client_id):
        for client in self._client_list:
            if client.client_id == client_id:
                return client
        return None

    def get_index_by_id(self, client_id):
        index = 0
        for item in self._client_list:
            if item.client_id == client_id:
                return item, index
            index += 1
        return None

    def add_client(self, client):
        if self.find_client_by_id(client.client_id) is None:
            self._client_list.append(client)
        else:
            raise RepositoryException("Client already exists.")

    def delete_client(self, client_id):
        client_to_remove = self.find_client_by_id(client_id)
        if client_to_remove is not None:
            self._client_list.remove(client_to_remove)

    def update_client(self, client_id, new_client):
        client_to_update, index = self.get_index_by_id(client_id)
        if client_to_update is not None:
            self._client_list[index] = new_client

    def __getitem__(self, item):
        return self._client_list[item]

    def __setitem__(self, key, value):
        self._client_list[key] = value

    def print_list_of_clients(self):
        clients_to_print = list()
        for client in self._client_list:
            clients_to_print.append(str(client))
        return clients_to_print

    def get_all_clients(self):
        return self._client_list

    def __len__(self):
        return len(self._client_list)


class ClientBinFileRepository(ClientRepository):
    def __init__(self):
        super().__init__()

        self._file_name = "clients.bin"
        # self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rb")

        # self._client_list = pickle.load(file)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(self._client_list, file)
        file.close()

    def add_client(self, client):
        super(ClientBinFileRepository, self).add_client(client)
        self._save_file()

    def delete_client(self, client_id):
        super(ClientBinFileRepository, self).delete_client(client_id)
        self._save_file()

    def update_client(self, client_id, new_client):
        super(ClientBinFileRepository, self).update_client(client_id, new_client)
        self._save_file()


class ClientFileRepository(ClientRepository):
    def __init__(self):
        super().__init__()

        self._file_name = "clients.txt"
        # self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rt")
        """"
        lines_from_file = file.readlines()
        for line in lines_from_file:
            client_id, name = line.split(sep=',')
            new_client = Client(int(client_id), name)
            self.add_client(new_client)
        """
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wt")

        for client in self._client_list:
            file.write(str(client) + '\n')

    def add_client(self, client):
        super(ClientFileRepository, self).add_client(client)
        self._save_file()

    def delete_client(self, client_id):
        super(ClientFileRepository, self).delete_client(client_id)
        self._save_file()

    def update_client(self, client_id, new_client):
        super(ClientFileRepository, self).update_client(client_id, new_client)
        self._save_file()


def get_repositories(properties_dictionary):
    if properties_dictionary['repository'] == 'inmemory':
        book_repository = BookRepository()
        client_repository = ClientRepository()
        rental_repository = RentalRepository()
    elif properties_dictionary['repository'] == 'binaryfiles':
        book_repository = BookBinFileRepository()
        client_repository = ClientBinFileRepository()
        rental_repository = RentalBinFileRepository()
    elif properties_dictionary['repository'] == 'textfiles':
        book_repository = BookFileRepository()
        client_repository = ClientFileRepository()
        rental_repository = RentalFileRepository()
    return book_repository, client_repository, rental_repository


def create_book_repository():
    repo = BookRepository()
    repo.add_book(Book(123, "1984", "George Orwell"))
    repo.add_book(Book(1003, "land", "George Orwell"))
    repo.add_book(Book(1093, "MobyDick", "Herman Melville"))
    repo.add_book(Book(1083, "land 1", "Lisa K"))
    repo.add_book(Book(2003, "War and peace", "Lev Tolstoi"))
    repo.add_book(Book(91003, "Politics", "John S"))
    repo.add_book(Book(7863, "Economy basics", "Hector S"))
    repo.add_book(Book(86563, "100", "SK Smith"))
    repo.add_book(Book(993, "War journal", "anonymous"))
    repo.add_book(Book(10452, "History - basics", "Ivan S"))
    return repo

