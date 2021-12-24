import unittest
from src.domain.Book import Book
from src.domain.Client import Client


class BookObjectTests(unittest.TestCase):
    def setUp(self):
        self.new_book = Book(123, "1984", "George Orwell")
        unittest.TestCase.setUp(self)

    def test_set_author__valid_name__save_name(self):
        self.new_book.set_author("John St")
        self.assertEqual(self.new_book.author, "John St")

    def test_title__correct__return_attribute(self):
        self.assertEqual(self.new_book.title, "1984")

    def test_author__valid__return_name(self):
        self.assertEqual(self.new_book.author, "George Orwell")

    def test_set_author__incorrect_input__raise_error(self):
        try:
            self.new_book.set_author("John 5")
            assert False
        except ValueError:
            pass

    def test_book_id__valid_input__return_id(self):
        self.assertEqual(self.new_book.book_id, 123)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


class ClientObjectTests(unittest.TestCase):
    def setUp(self):
        self.new_client = Client(12345, "John K")
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_set_name__valid_input__save_name(self):
        self.new_client.set_name("new name")
        self.assertEqual(self.new_client.name, "new name")


if __name__ == '__main__':
    unittest.main()
