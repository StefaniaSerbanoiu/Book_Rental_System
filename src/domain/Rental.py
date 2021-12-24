# Rental: rental_id, book_id, client_id, rented_date, returned_date

from src.domain.Book import Book
from src.domain.Client import Client
from datetime import date


class Rental:
    def __init__(self, rental_id=0, book_id=0, client_id=0, rented_date=date(1, 1, 1), returned_date=date(1, 1, 1)):
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rental_id = rental_id
        self.__rented_date = rented_date
        self.__returned_date = returned_date

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def book_id(self):
        return self.__book_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def rented_date(self):
        return self.__rented_date

    @property
    def returned_date(self):
        return self.__returned_date

    def __str__(self):
        if self.__returned_date != date(1, 1, 1) and self.returned_date != date(1, 1, 1):
            return "The rental with the id {self._Rental__rental_id} has the " \
                   "book id -> {self._Rental__book_id} ; the client id" \
                   " -> {self._Rental__client_id} ; rent date: {self._Rental__rented_date} ; return date " \
                   "-> {self._Rental__returned_date}".format(self=self)
        elif self.__rented_date != date(1, 1, 1):
            return "The rental with the id {self._Rental__rental_id} has the book id - {self._Rental__book_id} ; the " \
                   "client id - {self._Rental__client_id} ; rent date: {self._Rental__rented_date}".format(self=self)
        else:
            return "The rental hasn't been established yet."

    def set_rented_date(self, year, month, day):
        if year > 2021 or year < 2010 or not isinstance(year, int):
            raise ValueError("Invalid year")
        if not isinstance(month, int) or month < 1 or month > 12:
            raise ValueError("Invalid month")
        if not isinstance(day, int) or day < 1 or day > 31:
            raise ValueError("Invalid date")
        self.__rented_date = date(year, month, day)

    @returned_date.setter
    def returned_date(self, date):
        if date.year > 2021 or not isinstance(date.year, int):
            raise ValueError("Invalid year")
        if not isinstance(date.month, int) or date.month < 1 or date.month > 12:
            raise ValueError("Invalid month")
        if not isinstance(date.day, int) or date.day < 1 or date.day > 31:
            raise ValueError("Invalid date")
        self.__returned_date = date


def test_set_date():
    rental_test = Rental(100, 15, 16, date(2020, 1, 1), date(2020, 11, 11))
    assert rental_test.rental_id == 100
    assert rental_test.book_id == 15
    assert rental_test.client_id == 16
    assert rental_test.rented_date == date(2020, 1, 1)
    assert rental_test.returned_date == date(2020, 11, 11)


test_set_date()
rental = Rental(100, 15, 15, date(2020, 1, 1), date(2020, 11, 11))
print(rental.returned_date)
