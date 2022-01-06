import copy

from src.IterableDataStructure import filter_entity
from src.repository.repository import BookRepository
from src.domain.Book import Book
from src.IterableDataStructure import IterableEntity
import random


class BookServices:
    def __init__(self, book_repo):
        self.__repo = book_repo

    def add_new_book(self, book):
        self.__repo.add_book(book)

    def get_repository_item(self, item):
        return self.__repo[item]

    def list_books(self):
        list_to_print = self.__repo.print_list_of_books()
        return list_to_print

    def remove_book(self, book_id):
        self.__repo.remove(book_id)

    def update_book(self, book_id, new_book):
        self.__repo.update_book(book_id, new_book)

    def generate_book_id(self):
        generated_id = random.randint(100, 1000000)
        while self.__repo.find_by_id(generated_id) is not None:
            generated_id = random.randint(100, 1000000)
        return generated_id

    # ~~~~~~~~~~~~~~~~~~~~~~~SEARCH~~~~~~~~~~~~~~~~~~~~~~~~

    def search_by_id(self, book_id):
        length = len(self.__repo)
        index = 0
        while index < length :
            if self.__repo[index].book_id == book_id:
                return self.__repo[index]
            index += 1

    @staticmethod
    def acceptance_function_for_title(element, title):
        title_to_check = element[0].lower()

        if title_to_check == title or title in title_to_check:
            return True

        return False

    def get_list_of_titles_and_indexes(self):
        list_to_filter = list()

        for item in self.__repo:
            list_to_filter.append([item.title, item.author, item.book_id])

        return list_to_filter

    def filter_by_title(self, title):
        list_to_filter = self.get_list_of_titles_and_indexes()
        title = title.lower()
        filtered_list = filter_entity(list_to_filter,  self.acceptance_function_for_title, title)

        return filtered_list

    def search_by_title(self, title):
        length = len(self.__repo)
        index = 0
        title = title.lower()
        search_results = list()

        while index < length:
            title_to_check = self.__repo[index].title.lower()
            if title_to_check == title or title in title_to_check:
                search_results.append(str(self.__repo[index]))
            index += 1

        return search_results

    def get_list_of_authors(self):
        list_to_filter = list()

        for item in self.__repo:
            list_to_filter.append([item.author, item.title, item.book_id])

        return list_to_filter

    @staticmethod
    def acceptance_function_for_author(element, author):
        author_to_check = element[0].lower()

        if author_to_check == author or author in author_to_check:
            return True

        return False

    def filter_by_author(self, author):
        list_to_filter = self.get_list_of_authors()
        author = author.lower()
        filtered_list = filter_entity(list_to_filter, self.acceptance_function_for_title, author)
        return filtered_list

    def search_by_author(self, author):
        length = len(self.__repo)
        index = 0
        author = author.lower()
        search_results = list()
        while index < length:
            author_to_check = self.__repo[index].author.lower()
            # print(author_to_check)
            if author_to_check == author or author in author_to_check:
                search_results.append(str(self.__repo[index]))
            index += 1
        return search_results


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

