from books import Book
from users import User
from library import Library

my_library = Library()

book1 = Book("001", "OOP Fundamentals", "Jhon L", "BBC")
book2 = Book("002", "Python for Dummies", "Stef Maruzuh", "For Dummies")
my_library.add_book(book1)
my_library.add_book(book2)

user1 = User("001", "Zavala", "1234")
my_library.add_user(user1)

my_library.show_books()

my_library.borrow_book("001", "001")
my_library.borrow_book("001", "001")

my_library.show_books()

my_library.return_book("001")

my_library.show_books()

#Requeriments
# 1. The system must allow register books
# 2. The system must allow register users
# 3. The system must allow a book to be borrowed by user
# 4. A book that has already been borrowed cannot be borrowed again
# 5. The system must allow a book to be returned
