from src.repository.repository import BookRepository, ClientRepository, RentalRepository
from src.services.BookServices import BookServices
from src.services.ClientServices import ClientServices
from datetime import date
from src.services.RentalServices import RentalServices


class UndoRedo:
    __undo_list = []
    __redo_list = []

    def __init__(self, book_service, client_service, rental_service):
        super().__init__()
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service

    def undo_add_book(self, book_id):
        self.__book_service.remove_book(book_id)

    def undo_remove_book(self, removed_book):
        self.__book_service.add_new_book(removed_book)

    def undo_update_book(self, non_updated_book):
        self.__book_service.update_book(non_updated_book.book_id, non_updated_book)

    def undo_add_client(self, client_id):
        self.__client_service.remove_client(client_id)

    def undo_remove_client(self, removed_client):
        self.__client_service.add_new_client(removed_client)

    def undo_update_client(self, non_updated_client):
        self.__client_service.update_client(non_updated_client.client_id, non_updated_client)

    def undo_return_book(self, book_id, client_id):
        returned_date = date(1, 1, 1)
        self.__rental_service.change_returned_date(book_id, client_id, returned_date)

    def redo_return_book(self, book_id, client_id, returned_date):
        self.__rental_service.change_returned_date(book_id, client_id, returned_date)

    def redo_rent_book(self, rental):
        self.__rental_service.add_rental(rental)

    def undo_rent_book(self, book_id, client_id):
        self.__rental_service.delete_rental(book_id, client_id)

    @staticmethod
    def add_command_to_undo(command_and_arguments):
        UndoRedo.__undo_list.append(command_and_arguments)

    @staticmethod
    def clear_redo_list():
        if UndoRedo.__redo_list:
            for element in UndoRedo.__redo_list:
                UndoRedo.__redo_list.remove(element)

    def redo_last_command(self):
        # the commands will call functions corresponding with the undo of the undo_last_command
        # in other words, the complementary action of the undone operation

        if UndoRedo.__redo_list:
            arguments_for_redo = [UndoRedo.__redo_list[-1][1]]

            if UndoRedo.__redo_list[-1][0] == "add_book":
                self.undo_remove_book(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "remove_book":
                self.undo_add_book(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "update_book":
                self.undo_update_book(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "add_client":
                self.undo_remove_client(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "remove_client":
                self.undo_add_client(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "update_client":
                self.undo_update_client(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "rent_book":
                self.redo_rent_book(*arguments_for_redo)
            elif UndoRedo.__redo_list[-1][0] == "return_book":
                self.redo_return_book(*UndoRedo.__redo_list[-1][1])

            UndoRedo.__redo_list.pop()

    def undo_last_command(self):
        if UndoRedo.__undo_list:
            arguments_for_undo = [UndoRedo.__undo_list[-1][1]]
            redo_command = UndoRedo.__undo_list[-1][0]
            redo_argument = UndoRedo.__undo_list[-1][2]

            print(*arguments_for_undo)

            if UndoRedo.__undo_list[-1][0] == "add_book":
                self.undo_add_book(*arguments_for_undo)
            elif UndoRedo.__undo_list[-1][0] == "remove_book":
                self.undo_remove_book(*arguments_for_undo)
            elif UndoRedo.__undo_list[-1][0] == "update_book":
                self.undo_update_book(*arguments_for_undo)
            elif UndoRedo.__undo_list[-1][0] == "add_client":
                self.undo_add_client(*arguments_for_undo)
            elif UndoRedo.__undo_list[-1][0] == "remove_client":
                self.undo_remove_client(*arguments_for_undo)
            elif UndoRedo.__undo_list[-1][0] == "update_client":
                self.undo_update_client(*arguments_for_undo)
            elif UndoRedo.__undo_list[-1][0] == "return_book":
                arguments_for_undo.append(UndoRedo.__undo_list[-1][2])
                self.undo_return_book(*arguments_for_undo)
                redo_argument = [UndoRedo.__undo_list[-1][1], UndoRedo.__undo_list[-1][2], UndoRedo.__undo_list[-1][3]]
            elif UndoRedo.__undo_list[-1][0] == "rent_book":
                arguments_for_undo.append(UndoRedo.__undo_list[-1][2])
                self.undo_rent_book(*arguments_for_undo)
                redo_argument = UndoRedo.__undo_list[-1][3]

            element_of_redo_list = [redo_command, redo_argument]
            UndoRedo.__redo_list.append(element_of_redo_list)
            UndoRedo.__undo_list.pop()


