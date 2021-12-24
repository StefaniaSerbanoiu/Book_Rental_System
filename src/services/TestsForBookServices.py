import unittest
from src.domain.Book import Book
from src.repository.repository import RepositoryException
from src.services.BookServices import BookServices, create_book_repository


class BookServicesTests(unittest.TestCase):
    def setUp(self):
        self.book_repository = create_book_repository()
        self.book_services = BookServices(self.book_repository)

        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    # .BookServicesTests.test_add_new_book_valid_input__saves_object

    def test_update_book__valid_input__updates_data(self):
        self.assertEqual(self.book_repository[2].title , "MobyDick")
        new_book = Book(438, "A Clockwork Orange", "Anthony Burgess")
        self.book_services.update_book(1093, new_book)
        self.assertEqual(self.book_repository[2].title , "A Clockwork Orange")

    def test_add_new_book__valid_input__saves_object(self):
        book_to_add = Book(1112, "Assasin's apprentice", "Robin Hobb")
        self.book_services.add_new_book(book_to_add)
        self.assertEqual(self.book_repository[10].book_id, 1112)

    def test_add_new_book__invalid_book__raise_RepositoryException(self):
        try:
            book_to_add = Book(123, "1984", "George Orwell")
            self.book_services.add_new_book(book_to_add)
            assert False
        except RepositoryException:
            pass

    def test_remove_book__valid_book__remove_object(self):
        self.book_services.remove_book(123)
        self.assertEqual(self.book_repository[0].book_id ,1003)

    def test_remove_book__nonexistent_book__unsuccessful_deletion(self):
        self.assertEqual( len(self.book_repository), 10)
        self.book_services.remove_book(122)
        self.assertEqual(len(self.book_repository) , 10)

    def test_search_by_id__valid_input__returns_object(self):
        self.assertEqual(self.book_services.search_by_id(123).book_id , 123)
        self.assertEqual( self.book_services.search_by_id(123).title, "1984")

    def test_search_by_title__valid_input__returns_list(self):
        self.assertEqual( self.book_services.search_by_title("wAr"),[str(self.book_repository[4]), str(self.book_repository[8])])

    def test_search_by_author__valid_input__returns_list(self):
        self.assertEqual(self.book_services.search_by_author("geOrge ORWELL") , [str(self.book_repository[0]), str(self.book_repository[1])])


if __name__ == '__main__':
    unittest.main()
