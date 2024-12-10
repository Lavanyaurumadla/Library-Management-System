import datetime

class Book:
    def __init__(self, id, title, author, isbn):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False
        self.due_date = None

    def check_out(self, days=14):
        if not self.is_checked_out:
            self.is_checked_out = True
            self.due_date = datetime.datetime.now() + datetime.timedelta(days=days)
        else:
            print("Book already checked out.")

    def check_in(self):
        if self.is_checked_out:
            self.is_checked_out = False
            self.due_date = None
        else:
            print("Book was not checked out.")

    def __str__(self):
        return f"{self.id}: {self.title} by {self.author}, ISBN: {self.isbn}"

class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        if book.id in self.books:
            print("Book already exists in the library.")
        else:
            self.books[book.id] = book

    def remove_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
        else:
            print("Book not found in the library.")

    def find_book(self, book_id):
        return self.books.get(book_id, None)

    def check_out_book(self, book_id):
        book = self.find_book(book_id)
        if book and not book.is_checked_out:
            book.check_out()
        elif book:
            print("Book is already checked out.")
        else:
            print("Book not found.")

    def check_in_book(self, book_id):
        book = self.find_book(book_id)
        if book and book.is_checked_out:
            book.check_in()
        elif book:
            print("Book is not checked out.")
        else:
            print("Book not found.")

    def list_books(self):
        for book in self.books.values():
            status = "Checked out" if book.is_checked_out else "Available"
            print(f"{book} - {status}")

class OverdueManager:
    def __init__(self, library):
        self.library = library
        self.overdue_fee_per_day = 0.50  # fee per day for overdue books

    def calculate_overdue_fee(self, book):
        if book.is_checked_out and book.due_date < datetime.datetime.now():
            overdue_days = (datetime.datetime.now() - book.due_date).days
            return overdue_days * self.overdue_fee_per_day
        return 0.0

    def report_overdue_books(self):
        print("Overdue Books Report:")
        for book in self.library.books.values():
            if book.is_checked_out and book.due_date < datetime.datetime.now():
                overdue_fee = self.calculate_overdue_fee(book)
                print(f"{book.title} by {book.author} is overdue by {(datetime.datetime.now() - book.due_date).days} days. Fee: ${overdue_fee:.2f}")


class MembershipPlan:
    def __init__(self, plan_name, checkout_limit, discount_rate):
        self.plan_name = plan_name
        self.checkout_limit = checkout_limit
        self.discount_rate = discount_rate  # Discount on late fees

class MembershipManager:
    def __init__(self):
        self.memberships = {}

    def add_membership_plan(self, plan_name, checkout_limit, discount_rate):
        if plan_name not in self.memberships:
            self.memberships[plan_name] = MembershipPlan(plan_name, checkout_limit, discount_rate)
            print(f"Membership plan {plan_name} added.")
        else:
            print("Membership plan already exists.")

    def get_plan_details(self, plan_name):
        if plan_name in self.memberships:
            plan = self.memberships[plan_name]
            print(f"Plan {plan_name}: Checkout Limit - {plan.checkout_limit}, Discount Rate - {plan.discount_rate * 100}%")
        else:
            print("Plan not found.")



class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.checked_out_books = []

    def check_out_book(self, book):
        if not book.is_checked_out:
            self.checked_out_books.append(book)
            book.check_out()
            print(f"Book {book.title} checked out by {self.name}.")
        else:
            print("Book is already checked out.")

    def check_in_book(self, book):
        if book in self.checked_out_books:
            self.checked_out_books.remove(book)
            book.check_in()
            print(f"Book {book.title} checked in by {self.name}.")
        else:
            print("This book was not checked out by this user.")

    def list_checked_out_books(self):
        if self.checked_out_books:
            print(f"Books checked out by {self.name}:")
            for book in self.checked_out_books:
                print(book.title)
        else:
            print("No books currently checked out.")

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.user_id not in self.users:
            self.users[user.user_id] = user
            print(f"User {user.name} added to the library system.")
        else:
            print("User already exists.")

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            print("User removed from the library system.")
        else:
            print("User not found.")

    def find_user(self, user_id):
        return self.users.get(user_id, None)


class Reservation:
    def __init__(self, book, user):
        self.book = book
        self.user = user
        self.active = True

class ReservationManager:
    def __init__(self):
        self.reservations = []

    def reserve_book(self, book, user):
        if not book.is_checked_out and all(res.book != book for res in self.reservations):
            self.reservations.append(Reservation(book, user))
            print(f"Book {book.title} reserved by {user.name}.")
        else:
            print("Book is currently checked out or already reserved.")

    def process_reservations(self):
        for reservation in self.reservations:
            if not reservation.book.is_checked_out:
                reservation.user.check_out_book(reservation.book)
                reservation.active = False
        self.reservations = [res for res in self.reservations if res.active]


class SearchSystem:
    def __init__(self, library):
        self.library = library

    def search_by_title(self, title):
        found_books = [book for book in self.library.books.values() if title.lower() in book.title.lower()]
        return found_books

    def search_by_author(self, author):
        found_books = [book for book in self.library.books.values() if author.lower() in book.author.lower()]
        return found_books

    def search_by_isbn(self, isbn):
        found_books = [book for book in self.library.books.values() if book.isbn == isbn]
        return found_books

    def search_by_genre(self, genre):
        found_books = [book for book in self.library.books.values() if book.genre and genre.lower() in book.genre.lower()]
        return found_books

    def display_search_results(self, books):
        if books:
            for book in books:
                print(book)
        else:
            print("No books found matching the criteria.")


class NotificationSystem:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def send_due_date_reminder(self, user, book):
        if book.is_checked_out and book.due_date:
            print(f"Reminder: The book '{book.title}' is due on {book.due_date.strftime('%Y-%m-%d')}. Please return it on time.")

    def send_reservation_notification(self, user, book):
        print(f"Notification: The book '{book.title}' you reserved is now available for checkout.")


class BookReview:
    def __init__(self, book, user, rating, review):
        self.book = book
        self.user = user
        self.rating = rating
        self.review = review

class ReviewManager:
    def __init__(self):
        self.reviews = []

    def add_review(self, book, user, rating, review):
        new_review = BookReview(book, user, rating, review)
        self.reviews.append(new_review)
        print(f"Review added for {book.title} by {user.name}.")

    def show_reviews(self, book):
        book_reviews = [review for review in self.reviews if review.book == book]
        if book_reviews:
            for review in book_reviews:
                print(f"Rating: {review.rating}/5 - {review.review} by {review.user.name}")
        else:
            print("No reviews yet for this book.")




def main():
    library = Library()
    library.add_book(Book("001", "1984", "George Orwell", "9780451524935"))
    library.add_book(Book("002", "To Kill a Mockingbird", "Harper Lee", "9780060935467"))

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Check Out Book")
        print("4. Check In Book")
        print("5. List All Books")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            id = input("Enter book ID: ")
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            library.add_book(Book(id, title, author, isbn))
        elif choice == '2':
            book_id = input("Enter book ID to remove: ")
            library.remove_book(book_id)
        elif choice == '3':
            book_id = input("Enter book ID to check out: ")
            library.check_out_book(book_id)
        elif choice == '4':
            book_id = input("Enter book ID to check in: ")
            library.check_in_book(book_id)
        elif choice == '5':
            library.list_books()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    main()