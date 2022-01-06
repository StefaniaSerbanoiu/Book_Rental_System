import unittest

from src.IterableDataStructure import *


class IterableEntityTests(unittest.TestCase):
    def setUp(self):
        list_to_test = [1, 5, 9, 17, 111, 1, 10]
        self.iterable_entity = IterableEntity(list_to_test)

        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_append__correct_input__saves_data(self):
        self.iterable_entity.append(2000)
        self.assertEqual(self.iterable_entity[7], 2000)

    def test_remove__valid_item__deletes_successfully(self):
        self.assertEqual(self.iterable_entity[5], 1)
        self.iterable_entity.remove(1)
        self.assertEqual(self.iterable_entity[5], 10)

    def test_delitem__valid_index__deletes_successfully(self):
        self.assertEqual(self.iterable_entity[5], 1)
        self.iterable_entity.__delitem__(5)
        self.assertEqual(self.iterable_entity[5], 10)

    def test_len__correct_case__returns_length(self):
        self.assertEqual(len(self.iterable_entity), 7)


if __name__ == '__main__':
    unittest.main()
