import random
from src.domain.Book import Book
from src.domain.Client import Client
from datetime import date

from src.domain.Rental import Rental
from src.services.Undo_and_Redo import UndoRedo


class UI:
    def __init__(self, book_services, client_services, rental_services):
        self.__book_services = book_services
        self.__client_services = client_services
        self.__rental_services = rental_services
        self.__undo_redo_service = UndoRedo(self.__book_services, self.__client_services, self.__rental_services)

    @staticmethod
    def print_menu():
        print("1. To add a new book, press 1.\n"
              "2. To remove a book, press 2.\n"
              "3. To update a book, press 3.\n"
              "4. To list all books, press 4.\n"
              "5. To add a new client, press 5.\n"
              "6. To remove a client, press 6.\n"
              "7. To update a client, press 7.\n"
              "8. To list all clients, press 8.\n"
              "9. To rent a book, press 9.\n"
              "10. To return a book, press 10.\n"
              "11. To search for a book by its id, press 11.\n"
              "12. To search for a book by its title, press 12.\n"
              "13. To search for a book by the name of the author, press 13.\n"
              "14. To search for a client by its id, press 14.\n"
              "15. To search for a client by its name, press 15.\n"
              "16. To see the statistics for the most rented books, press 16.\n"
              "17. To see the statistics for the most active clients, press 17.\n"
              "18. To see the statistics for the most rented author, press 18.\n"
              "19. To undo, press 19.\n"
              "20. To redo, press 20.\n"
              "21. To exit, press -1.\n"
              "21. rentals -> 999")

    def add_book_ui(self):
        book_id = self.__book_services.generate_book_id()
        title = input("Introduce title")
        author = input("Introduce author")
        new_book = Book(book_id)
        new_book.set_title(title)
        new_book.set_author(author)
        self.__undo_redo_service.add_command_to_undo(["add_book", book_id, new_book])
        self.__book_services.add_new_book(new_book)

    def remove_book_ui(self):
        book_id = int(input("Introduce book id:"))
        self.__undo_redo_service.add_command_to_undo(["remove_book", self.__book_services.search_by_id(book_id), book_id])
        self.__book_services.remove_book(book_id)

    def update_book_ui(self):
        book_id = int(input("Introduce book id:"))
        title = input("Introduce title")
        author = input("Introduce author")

        updated_book = Book(book_id)
        updated_book.set_title(title)
        updated_book.set_author(author)

        self.__undo_redo_service.add_command_to_undo(["update_book", self.__book_services.search_by_id(book_id),
                                                      updated_book])
        self.__book_services.update_book(book_id, updated_book)

    def list_books_ui(self):
        list_to_print = self.__book_services.list_books()
        print(*list_to_print, sep='\n')

    def add_client_ui(self):
        client_id = self.__client_services.generate_client_id()
        name = input("Introduce the name of the client: ")
        new_client = Client(client_id)
        new_client.set_name(name)

        self.__undo_redo_service.add_command_to_undo(["add_client", client_id, new_client])
        self.__client_services.add_new_client(new_client)

    def remove_client_ui(self):
        client_id = int(input("Introduce the client's id: "))
        self.__undo_redo_service.add_command_to_undo(["remove_client", self.__client_services.search_by_id(client_id),
                                                      client_id])
        self.__client_services.remove_client(client_id)

    def update_client_ui(self):
        client_id = int(input("Introduce the client's id: "))
        name = input("Introduce the name of the client: ")

        updated_client = Client(client_id)
        updated_client.set_name(name)

        self.__undo_redo_service.add_command_to_undo(["update_client", self.__client_services.search_by_id(client_id),
                                                      updated_client])
        self.__client_services.update_client(client_id, updated_client)

    def list_clients_ui(self):
        list_to_print = self.__client_services.list_clients()
        print(*list_to_print, sep='\n')

    def rent_book_ui(self):
        client_id = int(input("Introduce the client's id: "))
        book_id = int(input("Introduce the id of the book to be rented: "))
        day = int(input("Introduce the day: "))
        month = int(input("Introduce the month: "))
        year = int(input("Introduce the year: "))
        rented_date = date(year, month, day)

        self.__rental_services.rent_book(book_id, client_id, rented_date)

        rental_id = self.__rental_services.get_rental_id_by_book_id_and_client_id(book_id, client_id)
        print(rental_id)

        self.__undo_redo_service.add_command_to_undo(["rent_book", book_id, client_id, Rental(
            rental_id, book_id, client_id,
            rented_date)])

    def return_book_ui(self):
        client_id = int(input("Introduce the client's id: "))
        book_id = int(input("Introduce the id of the book to be rented: "))
        day = int(input("Introduce the day: "))
        month = int(input("Introduce the month: "))
        year = int(input("Introduce the year: "))
        returned_date = date(year, month, day)
        self.__undo_redo_service.add_command_to_undo(["return_book", book_id, client_id, returned_date])
        self.__rental_services.return_book(book_id, client_id, returned_date)

    def search_book_by_id_ui(self):
        book_id = int(input("Introduce book id: "))
        if not isinstance(book_id, int):
            print("Invalid format")
        else:
            book = self.__book_services.search_by_id(book_id)
            if book:
                print(book)
            else:
                print("The book was not found.")

    def search_book_by_author_ui(self):
        author = input("Introduce the author's name: ")
        # book = self.__book_services.search_by_author(author)
        book = self.__book_services.filter_by_author(author)
        if book:
            print(*book, sep='\n')
        else:
            print("The book was not found.")

    def search_book_by_title_ui(self):
        title = input("Introduce the title: ")
        book = self.__book_services.filter_by_title(title)
        # book = self.__book_services.search_by_title(title)
        if book:
            print(*book, sep='\n')
        else:
            print("The book was not found.")

    def search_client_by_id_ui(self):
        client_id = int(input("Introduce client id: "))
        if not isinstance(client_id, int):
            print("Invalid format")
        else:
            client = self.__client_services.search_by_id(client_id)
            if client:
                print(client)
            else:
                print("The client was not found.")

    def search_client_by_name_ui(self):
        name = input("Introduce the client's name: ")
        # client = self.__client_services.search_by_name(name)
        client = self.__client_services.filter_by_name(name)
        if client:
            print(*client, sep='\n')
        else:
            print("The client was not found.")

    def statistics_most_rented_books_ui(self):
        most_rented_books_printable = self.__rental_services.sort_descending_order_most_rented_books_shell_sort().\
            print_list_of_books()
        print(*most_rented_books_printable, sep='\n')

    def statistics_most_rented_authors_ui(self):
        list_of_authors = self.__rental_services.sort_descending_order_most_rented_authors_shell_sort()
        print(*list_of_authors, sep='\n')

    def statistics_most_active_clients_ui(self):
        list_of_clients = self.__rental_services.sort_descending_order_most_active_clients_shell_sort().\
            print_list_of_clients()
        print(*list_of_clients, sep='\n')

    def print_all_rentals(self):
        list_to_print = self.__rental_services.print_all_rentals()
        print(*list_to_print, sep='\n')

    def menu(self):
        keep_menu_running = True

        while keep_menu_running:
            print("\n\n")
            self.print_menu()
            print("\n\n")
            menu_option = int(input("Choose an option: "))

            if menu_option == 1:
                self.add_book_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 2:
                self.remove_book_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 3:
                self.update_book_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 4:
                self.list_books_ui()
            elif menu_option == 5:
                self.add_client_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 6:
                self.remove_client_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 7:
                self.update_client_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 8:
                self.list_clients_ui()
            elif menu_option == 9:
                self.rent_book_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 10:
                self.return_book_ui()
                self.__undo_redo_service.clear_redo_list()
            elif menu_option == 11:
                self.search_book_by_id_ui()
            elif menu_option == 12:
                self.search_book_by_title_ui()
            elif menu_option == 13:
                self.search_book_by_author_ui()
            elif menu_option == 14:
                self.search_client_by_id_ui()
            elif menu_option == 15:
                self.search_client_by_name_ui()
            elif menu_option == 16:
                print("~~~~MOST RENTED BOOKS~~~~")
                self.statistics_most_rented_books_ui()
            elif menu_option == 17:
                print("~~~~MOST ACTIVE CLIENTS~~~~")
                self.statistics_most_active_clients_ui()
            elif menu_option == 18:
                print("~~~~MOST RENTED AUTHORS~~~~")
                self.statistics_most_rented_authors_ui()
            elif menu_option == 19:
                self.__undo_redo_service.undo_last_command()
            elif menu_option == 20:
                self.__undo_redo_service.redo_last_command()
            elif menu_option == -1:
                keep_menu_running = False
                print("Closed program.")
            elif menu_option == 999:
                self.print_all_rentals()
            else:
                print("Invalid option!!!")



