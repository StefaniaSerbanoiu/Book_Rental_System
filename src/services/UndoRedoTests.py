import unittest
from datetime import date

from src.domain.Book import Book
from src.domain.Client import Client
from src.domain.Rental import Rental
from src.repository.repository import BookRepository, ClientRepository, RentalRepository
from src.services.BookServices import BookServices
from src.services.ClientServices import ClientServices
from src.services.RentalServices import RentalServices
from src.services.Undo_and_Redo import UndoRedo


class UndoTests(unittest.TestCase):
    def setUp(self):
        self.book_repository = BookRepository()
        self.book_repository.add_book(Book(123, "1984", "George Orwell"))
        self.book_repository.add_book(Book(1003, "land", "George Orwell"))
        self.book_repository.add_book(Book(1093, "MobyDick", "Herman Melville"))
        self.book_repository.add_book(Book(1083, "land 1", "Lisa K"))
        self.book_services = BookServices(self.book_repository)
        self.client_repository = ClientRepository()
        self.client_repository.add_client(Client(121, "Lisa Arn"))
        self.client_repository.add_client(Client(12001, "ANa Al"))
        self.client_repository.add_client(Client(999, "Andrei S"))
        self.client_services = ClientServices(self.client_repository)
        self.rental_repository = RentalRepository()
        self.rental_repository.add_rental(Rental(1000, 123, 121, date(2020, 7, 11), date(2020, 7, 20)))
        self.rental_repository.add_rental(Rental(1001, 123, 121, date(2019, 7, 11), date(2019, 7, 20)))
        self.rental_repository.add_rental(Rental(1002, 123, 121, date(2015, 7, 11), date(2016, 7, 20)))
        self.rental_repository.add_rental(Rental(1003, 123, 121, date(2017, 9, 30), date(2017, 10, 30)))
        self.rental_services = RentalServices(self.book_repository, self.client_repository, self.rental_repository)
        self.undo_redo_service = UndoRedo(self.book_services,self.client_services, self.rental_services)
        unittest.TestCase.setUp(self)

    def test_redo_last_command__delete_client_command__calls_complementary_operation(self):
        self.undo_redo_service.add_command_to_undo(["add_client", 121, Client(121, "Lisa Arn")])
        self.undo_redo_service.redo_last_command()
        self.assertEqual(len(self.client_repository), 3)

    def test_undo_last_command__add_book_command__calls_complementary_operation(self):
        book_to_add = Book(1112, "Assasin's apprentice", "Robin Hobb")
        self.book_services.add_new_book(book_to_add)
        self.assertEqual(len(self.book_repository), 5)
        self.undo_redo_service.add_command_to_undo(["add_book", 1112, book_to_add])
        self.undo_redo_service.undo_last_command()
        self.assertEqual(len(self.book_repository), 4)

    def test_undo_last_command__delete_client_command__calls_complementary_operation(self):
        self.client_repository.delete_client(121)
        self.assertEqual(len(self.client_repository), 2)
        self.undo_redo_service.add_command_to_undo(["add_client", 121, Client(121, "Lisa Arn")])
        self.undo_redo_service.undo_last_command()
        self.assertEqual(len(self.client_repository), 2)

    def test_redo_last_command__add_book_command__calls_complementary_operation(self):
        book_to_add = Book(1112, "Assasin's apprentice", "Robin Hobb")
        self.book_services.add_new_book(book_to_add)
        self.assertEqual(len(self.book_repository), 5)
        self.undo_redo_service.add_command_to_undo(["add_book", 1112, book_to_add])
        self.undo_redo_service.undo_last_command()
        self.assertEqual(len(self.book_repository), 4)
        self.undo_redo_service.redo_last_command()
        self.assertEqual(len(self.book_repository), 5)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


if __name__ == '__main__':
    unittest.main()
