from src.repository.repository import ClientRepository
from src.domain.Client import Client
import random


class ClientServices:
    def __init__(self, client_repository):
        self.__repository = client_repository

    def add_new_client(self, client):
        self.__repository.add_client(client)

    def get_repository_item(self, item):
        return self.__repository[item]

    def list_clients(self):
        list_to_print = self.__repository.print_list_of_clients()
        return list_to_print

    def remove_client(self, client_id):
        self.__repository.delete_client(client_id)

    def update_client(self, client_id, new_client):
        self.__repository.update_client(client_id, new_client)

    def generate_client_id(self):
        generated_id = random.randint(100, 1000000)
        while self.__repository.find_client_by_id(generated_id) is not None:
            generated_id = random.randint(100, 1000000)
        return generated_id

    # ~~~~~~~~~~~~~~~~~~~~~~~~SEARCH~~~~~~~~~~~~~~~~~~~~~~~~

    def search_by_id(self, client_id):
        length = len(self.__repository)
        index = 0
        while index < length:
            if self.__repository[index].client_id == client_id:
                return self.__repository[index]
            index += 1

    def search_by_name(self, name):
        length = len(self.__repository)
        index = 0
        name = name.lower()
        search_results = list()
        while index < length:
            name_to_check = self.__repository[index].name.lower()
            if name_to_check == name or name in name_to_check:
                search_results.append(str(self.__repository[index]))
            index += 1
        return search_results
