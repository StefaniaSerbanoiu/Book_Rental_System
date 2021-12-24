from src.repository.repository import get_repositories
from src.ui.ui import UI
from src.services.RentalServices import RentalServices, create_book_repo, create_client_repo, create_rental_repository
from src.services.BookServices import BookServices
from src.services.ClientServices import ClientServices
from src.PropertyReader import get_properties


properties = get_properties("settings.properties")
print(properties)
book_repository, client_repository, rental_repository = get_repositories(properties)

book_repository = create_book_repo(book_repository)
client_repository = create_client_repo(client_repository)
rental_repository = create_rental_repository(rental_repository)

book_services = BookServices(book_repository)
client_services = ClientServices(client_repository)
rental_services = RentalServices(book_repository, client_repository, rental_repository)

interface = UI(book_services, client_services, rental_services)
interface.menu()
"""
repository = inmemory
books = ""
clients = ""
rentals = ""



repository = textfiles
books = "books.txt"
clients = "clients.txt"
rentals = "rentals.txt"



repository = binaryfiles
books = "books.pickle"
clients = "clients.pickle"
rentals = "rentals.pickle"






123,1984,George Orwell
1003,land,George Orwell
1093,MobyDick,Herman Melville
1083,land 1,Lisa K
2003,War and peace,Lev Tolstoi
91003,Politics,John S
7863,Economy basics,Hector S
86563,100,SK Smith
993,War journal,anonymous
10452,History - basics,Ivan S



25,john
27,laura
23,lisa
121,Lisa Arn
12001,ANa Al
999,Andrei S
123,LAvinia R
2300,Cornel Muresan
2355,Black White
9976,Andreea popescu


1,1093,25,2012,11,12,2020,1,1
2,1083,25,2012,11,12,1,1,1
3,2003,25,2012,11,12,1,1,1
4,91003,25,2012,11,12,1,1,1
5,7863,25,2012,11,12,1,1,1
6,86563,25,2012,11,12,1,1,1
7,993,25,2012,11,12,1,1,1
8,10452,25,2012,11,12,1,1,1
9,123,25,2012,11,12,1,1,1
10,1003,25,2012,11,12,1,1,1
11,2003,23,2012,11,12,1,1,1



clients:
Z      ](src.domain.ClientClient)}(_Client__client_idK
_Client__namejohnubh)}(hKhlauraubh)}(hKhlisaubh)}(hKyhLisa Arnubh)}(hMá.hANa Alubh)}(hMçhAndrei Subh)}(hK{h	LAvinia Rubh)}(hMühCornel Muresanubh)}(hM3	hBlack Whiteubh)}(hMø&hAndreea popescuube.

"""

