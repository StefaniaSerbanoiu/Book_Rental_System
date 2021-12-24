import unittest
from src.domain.Client import Client
from src.services.ClientServices import create_client_repository, ClientServices


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client_repository = create_client_repository()
        self.client_services = ClientServices(self.client_repository)

        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_add_new_client__valid_input__saves_object(self):
        self.client_services.add_new_client(Client(122, "new client name"))
        self.assertEqual(self.client_repository[3].client_id ,122)
        self.assertEqual(self.client_repository[3].name , "new client name")

    def test_remove_client__existing_object__removes_successfully(self):
        self.client_repository.delete_client(121)
        self.assertEqual( self.client_repository[0].client_id ,12001)

    def test_update_client__valid_input__updates_data(self):
        self.client_services.update_client(12001, Client(12001, "updated_name"))
        self.assertEqual(self.client_services.search_by_id(12001).name , "updated_name")
        # assert self.client_repository[1].name == "updated_name"

    def test_generate_client_id__unique_id__returns_new_id(self):
        for counting_index in range(100):
            self.assertIsNone(self.client_services.search_by_id(self.client_services.generate_client_id()))

    def test_search_by_id__existent_id__returns_found_object(self):
        self.assertEqual(self.client_services.search_by_id(999) , self.client_repository[2])

    def test_search_by_id__nonexistent_id__returns_None(self):
        self.assertIsNone(self.client_services.search_by_id(990) )

    def test_search_by_name__valid_name__returns_list(self):
        self.assertEqual(self.client_services.search_by_name("L") , [str(self.client_repository[0]), str(self.client_repository[1])])

    def test_search_by_name__nonexistent_name__returns_empty_list(self):
        self.assertEqual(self.client_services.search_by_name("Kora") , [])


if __name__ == '__main__':
    unittest.main()
