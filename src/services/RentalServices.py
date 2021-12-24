import copy

from src.domain.Client import Client
from src.domain.Book import Book
from src.domain.Rental import Rental
from src.repository.repository import BookRepository, ClientRepository, RentalRepository, ClientBinFileRepository, \
    ClientFileRepository, BookFileRepository, BookBinFileRepository, RentalFileRepository, RentalBinFileRepository
import random
from datetime import date


class RentalServices:
    def __init__(self, book_repository, client_repository, rental_repository):
        self.__book_repository = book_repository
        self.__client_repository = client_repository
        self.__rental_repository = rental_repository

    def is_book_available(self, book_id):
        if self.__book_repository.find_by_id(book_id) is not None:
            return True
        return False

    def generate_rental_id(self):
        generated_id = random.randint(100, 1000000)
        while self.__rental_repository.find_by_id(generated_id) is not None:
            generated_id = random.randint(100, 1000000)
        return generated_id

    def get_rental_id_by_book_id_and_client_id(self, book_id, client_id):
        return self.__rental_repository.get_rental_id_by_book_id_and_client_id(book_id, client_id)

    def add_rental(self, rental):
        self.__rental_repository.add_rental(rental)

    def rent_book(self, book_id, client_id, rented_date):
        if not self.does_client_exist(client_id):
            raise ValueError("The client doesn't exist.")
        if not self.is_book_available(book_id):
            raise ValueError("The book is not available.")
        rental_id = self.generate_rental_id()
        self.__rental_repository.add_rental(Rental(rental_id, book_id, client_id, rented_date))

    def is_book_rented(self, rental_id):
        if self.__rental_repository.find_by_id(rental_id) is None:
            return False
        return True

    def does_client_exist(self, client_id):
        if self.__client_repository.find_client_by_id(client_id) is not None:
            return True
        return False

    def returned_day_function(self, index_of_rental):
        self.__rental_repository.returned_date_function(index_of_rental)

    def change_returned_date(self, book_id, client_id, returned_date):
        rental_id = self.__rental_repository.get_rental_id_by_book_id_and_client_id(book_id, client_id)
        index_of_rental = self.__rental_repository.get_index_by_id(rental_id)
        self.__rental_repository[index_of_rental].returned_date = returned_date

        self.__rental_repository.returned_date_function(index_of_rental)

    def return_book(self, book_id, client_id, returned_date):
        if not self.is_book_available(book_id):
            raise ValueError("The book is not available.")
        rental_id = self.__rental_repository.get_rental_id_by_book_id_and_client_id(book_id, client_id)
        if not self.is_book_rented(rental_id):
            raise ValueError("The book hasn't been rented yet.")
        if not self.does_client_exist(client_id):
            raise ValueError("The client doesn't exist.")
        index_of_rental = self.__rental_repository.get_index_by_id(rental_id)
        print(str(rental_id) + ',' + str(returned_date.day))
        self.__rental_repository[index_of_rental].returned_date = returned_date
        self.__rental_repository.returned_date_function(index_of_rental)

    def delete_rental(self, book_id, client_id):
        self.__rental_repository.delete_rental(book_id, client_id)

    def print_all_rentals(self):
        rental_list = self.__rental_repository.print_list_of_rentals()
        return rental_list

    # ~~~~~~~~~~~~~~~~~~~~~~~STATISTICS~~~~~~~~~~~~~~~~~~~~~~~~~~

    def sort_descending_order_most_rented_books(self):
        books_repository = copy.deepcopy(self.__book_repository)
        book_repository_length = len(self.__book_repository)
        length = book_repository_length - 1
        for index2 in range(length):
            first_book_rental_count = self.__rental_repository.get_rental_count_by_book_id(
                books_repository[index2].book_id)
            for index1 in range(index2 + 1, book_repository_length):
                second_book_rental_count = self.__rental_repository.get_rental_count_by_book_id(
                    books_repository[index1].book_id)
                if first_book_rental_count < second_book_rental_count:
                    auxiliary_element = books_repository[index1]
                    books_repository[index1] = books_repository[index2]
                    books_repository[index2] = auxiliary_element
        return books_repository

    @staticmethod
    def calculate_days_between_2_dates(rented_date, returned_date):
        number_of_years = returned_date.year - rented_date.year
        number_of_months = returned_date.month - rented_date.month
        number_of_days = returned_date.day - rented_date.day
        if number_of_days < 0:
            number_of_days += 30
            number_of_months -= 1
        if number_of_months < 0 and number_of_years > 0:
            number_of_months += 12
            number_of_years -= 1
        return number_of_years * 365 + number_of_months * 30 + number_of_days

    def get_client_activity(self, client_id):
        active_days = 0
        rental_repository_length = len(self.__rental_repository)
        for index in range(rental_repository_length):
            if self.__rental_repository[index].client_id == client_id:
                active_days += self.calculate_days_between_2_dates(self.__rental_repository[index].rented_date,
                                                                   self.__rental_repository[index].returned_date)
        return active_days

    def sort_descending_order_most_active_clients(self):
        clients_repository = copy.deepcopy(self.__client_repository)
        client_repository_length = len(self.__client_repository)
        length = client_repository_length - 1
        for index2 in range(length):
            first_client_activity = self.get_client_activity(clients_repository[index2].client_id)
            if first_client_activity:
                for index1 in range(client_repository_length):
                    second_client_activity = self.get_client_activity(clients_repository[index1].client_id)
                    if second_client_activity and first_client_activity < second_client_activity:
                        auxiliary_element = clients_repository[index1]
                        clients_repository[index1] = clients_repository[index2]
                        clients_repository[index2] = auxiliary_element
        return clients_repository

    @staticmethod
    def check_if_author_exists_in_list_of_authors(author, list_of_authors):
        if author in list_of_authors:
            return True
        return False

    def get_list_of_authors(self):
        book_repository_length = len(self.__book_repository)
        author_list = list()
        for book_repository_index in range(book_repository_length):
            author_to_add = self.__book_repository[book_repository_index].author
            if self.check_if_author_exists_in_list_of_authors(author_to_add, author_list) is False:
                author_list.append(author_to_add)
        return author_list

    def get_rented_books_count_by_author(self, author):
        book_repository_length = len(self.__book_repository)
        books = 0
        author = author.lower()
        for book_index in range(book_repository_length):
            author_to_check = self.__book_repository[book_index].author.lower()
            if author == author_to_check:
                books += 1
        return books

    def sort_descending_order_most_rented_authors(self):
        authors_list = self.get_list_of_authors()
        author_list_length_0 = len(authors_list)
        author_list_length = author_list_length_0 - 1
        for index_1 in range(author_list_length):
            rented_books_written_by_author_1 = self.get_rented_books_count_by_author(authors_list[index_1])
            if rented_books_written_by_author_1 > 0:
                for index_2 in range(index_1 + 1, author_list_length_0):
                    rented_books_written_by_author_2 = self.get_rented_books_count_by_author(authors_list[index_2])
                    if rented_books_written_by_author_1 < rented_books_written_by_author_2:
                        auxiliary_element = authors_list[index_1]
                        authors_list[index_1] = authors_list[index_2]
                        authors_list[index_2] = auxiliary_element
        return authors_list


def create_book_repo(repo):
    # repo = BookRepository()
    # repo = BookFileRepository()
    # repo = BookBinFileRepository()

    repo.add_book(Book(1093, "MobyDick", "Herman Melville"))
    repo.add_book(Book(1083, "land 1", "Lisa K"))
    repo.add_book(Book(2003, "War and peace", "Lev Tolstoi"))
    repo.add_book(Book(91003, "Politics", "John S"))
    repo.add_book(Book(7863, "Economy basics", "Hector S"))
    repo.add_book(Book(86563, "100", "SK Smith"))
    repo.add_book(Book(993, "War journal", "anonymous"))
    repo.add_book(Book(10452, "History - basics", "Ivan S"))
    repo.add_book(Book(123, "1984", "George Orwell"))
    repo.add_book(Book(1003, "land", "George Orwell"))

    return repo


def create_client_repo(repo):
    # repo = ClientRepository()
    # repo = ClientFileRepository()
    # repo = ClientBinFileRepository()

    repo.add_client(Client(25, "john"))
    repo.add_client(Client(27, "laura"))
    repo.add_client(Client(23, "lisa"))
    repo.add_client(Client(121, "Lisa Arn"))
    repo.add_client(Client(12001, "ANa Al"))
    repo.add_client(Client(999, "Andrei S"))
    repo.add_client(Client(123, "LAvinia R"))
    repo.add_client(Client(2300, "Cornel Muresan"))
    repo.add_client(Client(2355, "Black White"))
    repo.add_client(Client(9976, "Andreea popescu"))

    return repo


def create_rental_repository(repository):
    # repository = RentalRepository()
    # repository = RentalFileRepository()
    # repository = RentalBinFileRepository()

    repository.add_rental(Rental(1, 1093, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(2, 1083, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(3, 2003, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(4, 91003, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(5, 7863, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(6, 86563, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(7, 993, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(8, 10452, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(9, 123, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(10, 1003, 25, date(2012, 11, 12), date(2012, 11, 20)))
    repository.add_rental(Rental(11, 1003, 23, date(2012, 11, 12), date(1, 1, 1)))

    return repository


"""
def create_rental_services(book_repository, client_repository, rental_repository):
    rental_service = RentalServices(create_book_repo(), client_repository, rental_repository)

    rental_service.rent_book(1093, 25, date(2012, 11, 12))
    rental_service.rent_book(1083, 25, date(2012, 11, 12))
    rental_service.rent_book(2003, 25, date(2012, 11, 12))
    rental_service.rent_book(91003, 25, date(2012, 11, 12))
    rental_service.rent_book(7863, 25, date(2012, 11, 12))
    rental_service.rent_book(86563, 25, date(2012, 11, 12))
    rental_service.rent_book(993, 25, date(2012, 11, 12))
    rental_service.rent_book(10452, 25, date(2012, 11, 12))
    rental_service.rent_book(123, 25, date(2012, 11, 12))
    rental_service.rent_book(1003, 25, date(2012, 11, 12))

    rental_service.rent_book(2003, 23, date(2012, 11, 12))
    rental_service.return_book(2003, 23, date(2012, 11, 20))

    rental_service.return_book(1093, 25, date(2012, 11, 20))
    rental_service.return_book(1083, 25, date(2012, 11, 20))
    rental_service.return_book(2003, 25, date(2012, 11, 20))
    rental_service.return_book(91003, 25, date(2012, 11, 20))
    rental_service.return_book(7863, 25, date(2012, 11, 20))
    rental_service.return_book(86563, 25, date(2012, 11, 20))
    rental_service.return_book(993, 25, date(2012, 11, 20))
    rental_service.return_book(10452, 25, date(2012, 11, 20))
    rental_service.return_book(123, 25, date(2012, 11, 20))
    rental_service.return_book(1003, 25, date(2012, 11, 20))

    rental_service.rent_book(1083, 27, date(2015, 10, 19))

    return rental_service


def empty_rental_service(book_repository, client_repository, rental_repository):
    rental_service = RentalServices(book_repository, client_repository, rental_repository)
    rental_service.print_all_rentals()
    return rental_service
"""
