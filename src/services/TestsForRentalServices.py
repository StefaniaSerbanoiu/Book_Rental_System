import unittest

from src.domain.Rental import Rental
from src.repository.repository import create_book_repository, RentalRepository
from src.services.ClientServices import create_client_repository
from src.services.RentalServices import create_book_repo, RentalServices
from datetime import date


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client_repository = create_client_repository()
        self.book_repository = create_book_repository()
        self.rental_repository = RentalRepository()
        self.rental_repository.add_rental(Rental(1000, 123, 121, date(2020, 7, 11), date(2020, 7, 20)))
        self.rental_repository.add_rental(Rental(1001, 123, 121, date(2019, 7, 11), date(2019, 7, 20)))
        self.rental_repository.add_rental(Rental(1002, 123, 121, date(2015, 7, 11), date(2016, 7, 20)))
        self.rental_repository.add_rental(Rental(1003, 123, 121, date(2017, 9, 30), date(2017, 10, 30)))
        self.rental_services = RentalServices(self.book_repository, self.client_repository, self.rental_repository)

        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_is_book_available__valid_book_id__true(self):
        self.assertEqual(self.rental_services.is_book_available(1003), True)

    def test_is_book_available__invalid_book_id__false(self):
        self.assertEqual(self.rental_services.is_book_available(120003), False)

    def test_generate_rental_id__correct_case__return_id(self):
        for counting_index in range(100):
            self.assertIsNone(self.rental_repository.find_by_id(self.rental_services.generate_rental_id()))

    def test_rent_book__valid_input__saves_rental(self):
        self.rental_services.rent_book(1003, 121, date(2021, 12, 2))
        self.assertEqual(self.rental_repository[4].rented_date, date(2021, 12, 2))

    def test_is_book_rented__valid_rental_id__false(self):
        self.assertEqual(self.rental_services.is_book_rented(1005), False)

    def test_is_book_rented__valid_rental_id__true(self):
        self.assertEqual(self.rental_services.is_book_rented(1003), True)

    def test_does_client_exist__valid_id__true(self):
        self.assertEqual(self.rental_services.does_client_exist(121), True)

    def test_does_client_exist__valid_id__False(self):
        self.assertEqual(self.rental_services.does_client_exist(1234), False)

    def test_return_book__valid_input__saves_returned_date(self):
        self.rental_services.rent_book(1003, 121, date(2021, 12, 1))
        self.assertEqual(self.rental_repository[4].returned_date, date(1, 1, 1))
        self.rental_services.return_book(1003, 121, date(2021, 12, 2))
        self.assertEqual(self.rental_repository[4].returned_date, date(2021, 12, 2))


if __name__ == '__main__':
    unittest.main()
