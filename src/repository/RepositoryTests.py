import datetime
import unittest
from src.domain.Book import Book
from src.domain.Client import Client
from src.domain.Rental import Rental
from src.repository.repository import BookRepository, ClientRepository, RentalRepository, RepositoryException, \
    create_book_repository
from src.services.ClientServices import create_client_repository
from datetime import date


class BookRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repo = BookRepository()
        self.repo.add_book(Book(123, "1984", "George Orwell"))
        self.repo.add_book(Book(1003, "land", "George Orwell"))
        self.repo.add_book(Book(1093, "MobyDick", "Herman Melville"))
        self.repo.add_book(Book(1083, "land 1", "Lisa K"))

        unittest.TestCase.setUp(self)

    def test_get_index_by_id__valid_input__return_number(self):
        self.assertEqual(self.repo.get_index_by_id(123), (self.repo[0], 0))
        self.assertEqual(self.repo.get_index_by_id(1093), (self.repo[2], 2))

    def test_find_by_id__valid_id__return_item(self):
        self.assertEqual(self.repo.find_by_id(1003), self.repo[1])

    def test_find_by_id__invalid_id__return_None(self):
        self.assertIsNone(self.repo.find_by_id(999))

    def test_get_index_by_id__nonexistent_id__return_None(self):
        self.assertIsNone(self.repo.get_index_by_id(1000) )

    def test_add_book__valid_input__save_object(self):
        self.repo.add_book(Book(2003, "War and peace", "Lev Tolstoi"))
        self.assertEqual(self.repo[4].book_id , 2003)

    def test_add_book__already_existing_book__raise_RepositoryException(self):
        try:
            self.repo.add_book(Book(123, "title", "author"))
            assert False
        except RepositoryException:
            pass

    def test_delete_book__valid_object__remove_successfully(self):
        self.repo.delete_book(1003)
        self.assertEqual(self.repo[1].book_id,1093)

    def test_delete_book__nonexistent_object__remove_unsuccessful(self):
        self.assertEqual(len(self.repo) , 4)
        self.repo.delete_book(999)
        self.assertEqual( len(self.repo) , 4)

    def test_get_all__correct_case__return_list(self):
       self.assertEqual(self.repo.get_all(),[self.repo[0], self.repo[1], self.repo[2], self.repo[3]])

    def tearDown(self):
        unittest.TestCase.tearDown(self)


class ClientRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.client_repository = ClientRepository()
        self.client_repository.add_client(Client(121, "Lisa Arn"))
        self.client_repository.add_client(Client(12001, "ANa Al"))
        self.client_repository.add_client(Client(999, "Andrei S"))

        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_find_client_by_id__correct_id__return_client(self):
        self.assertEqual(self.client_repository.find_client_by_id(12001) ,self.client_repository[1])

    def test_find_client_by_id__incorrect_id__return_None(self):
        self.assertIsNone(self.client_repository.find_client_by_id(1201))

    def test_get_index_by_id__invalid_id__returns_None(self):
        self.assertIsNone(self.client_repository.get_index_by_id(1201))

    def test_get_index_by_id__valid_id__returns_correctly(self):
        self.assertEqual(self.client_repository.get_index_by_id(12001) , (self.client_repository[1], 1))

    def test_get_all(self):
        self.assertEqual(self.client_repository.get_all_clients(), [self.client_repository[0], self.client_repository[1], self.client_repository[2]])

    def test_add_client__valid_input__saves_object(self):
        self.client_repository.add_client(Client(1111, "new client name"))
        self.assertEqual( self.client_repository[3].client_id, 1111)

    def test_add_client__invalid_input__raise_RepositoryException(self):
        try:
            self.client_repository.add_client(Client(12001, "new client name"))
            assert False
        except RepositoryException:
            pass

    def test_delete_client__valid_object__removes_correctly(self):
        self.client_repository.delete_client(12001)
        self.assertEqual(self.client_repository[1].client_id , 999)

    def test_delete_client__nonexistent_object__unsuccessful_remove(self):
        self.assertEqual(len(self.client_repository) , 3)
        self.client_repository.delete_client(1210)
        self.assertEqual(len(self.client_repository) , 3)


class RentalRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.client_repository = create_client_repository()
        self.book_repository = create_book_repository()
        self.rental_repository = RentalRepository()
        self.rental_repository.add_rental(Rental(1000, 123, 121, date(2020, 7, 11), date(2020, 7, 20)))
        self.rental_repository.add_rental(Rental(1001, 123, 121, date(2019, 7, 11), date(2019, 7, 20)))
        self.rental_repository.add_rental(Rental(1002, 123, 121, date(2015, 7, 11), date(2016, 7, 20)))
        self.rental_repository.add_rental(Rental(1003, 123, 121, date(2017, 9, 30), date(2017, 10, 30)))

        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_find_by_id__correct_id__returns_item(self):
        self.assertEqual(self.rental_repository.find_by_id(1001), self.rental_repository[1])

    def test_find_by_id__nonexistent_id__returns_None(self):
        self.assertIsNone(self.rental_repository.find_by_id(1005))

    def test_get_index_by_id__nonexistent_id__returns_None(self):
        self.assertIsNone(self.rental_repository.get_index_by_id(1005) )

    def test_get_index_by_id__valid_id__returns_integer(self):
        self.assertEqual(self.rental_repository.get_index_by_id(1001) ,1)

    def test_get_rental_id_by_book_id__valid_id__returns_id(self):
        self.assertEqual(self.rental_repository.get_rental_id_by_book_id(123) , 1000)

    def test_get_rental_id_by_book_id__nonexistent_id__returns_None(self):
        self.assertIsNone(self.rental_repository.get_rental_id_by_book_id(12003))

    def test_add_rental__already_existing_object__raises_RepositoryException(self):
        try:
            self.rental_repository.add_rental(Rental(1000))
            assert False
        except RepositoryException:
            pass

    def test_add_rental__valid_object__saves_object(self):
        self.rental_repository.add_rental(Rental(1201))
        self.assertEqual(self.rental_repository[4].rental_id, 1201)

    def test_get_rental_count_by_book_id__valid_id__returns_integer(self):
        self.assertEqual(self.rental_repository.get_rental_count_by_book_id(123) , 4)

    def test_get_rental_count_by_book_id__invalid_id__returns_zero(self):
        self.assertEqual(self.rental_repository.get_rental_count_by_book_id(1235) , 0)


if __name__ == '__main__':
    unittest.main()
