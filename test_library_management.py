import unittest
from datetime import datetime, timedelta
from library_management import Book, Library, MembershipPlan, User, Reservation, BookReview, NotificationSystem, SearchSystem
from unittest.mock import patch
from io import StringIO
import sys

class TestBook(unittest.TestCase):
    def test_check_out(self):
        book = Book("001", "1984", "George Orwell", "9780451524935")
        book.check_out()
        self.assertTrue(book.is_checked_out)
        self.assertIsNotNone(book.due_date)

    def test_check_in(self):
        book = Book("001", "1984", "George Orwell", "9780451524935")
        book.check_out()
        book.check_in()
        self.assertFalse(book.is_checked_out)
        self.assertIsNone(book.due_date)

    def test_str_representation(self):
        book = Book("001", "1984", "George Orwell", "9780451524935")
        self.assertEqual(str(book), "001: 1984 by George Orwell, ISBN: 9780451524935")

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book1 = Book("001", "1984", "George Orwell", "9780451524935")
        self.book2 = Book("002", "To Kill a Mockingbird", "Harper Lee", "9780060935467")

    def test_add_book(self):
        self.library.add_book(self.book1)
        self.assertIn("001", self.library.books)

    def test_remove_book(self):
        self.library.add_book(self.book1)
        self.library.remove_book("001")
        self.assertNotIn("001", self.library.books)

    def test_find_book(self):
        self.library.add_book(self.book1)
        found_book = self.library.find_book("001")
        self.assertEqual(found_book, self.book1)

    def test_check_out_book(self):
        self.library.add_book(self.book1)
        self.library.check_out_book("001")
        self.assertTrue(self.book1.is_checked_out)

    def test_check_in_book(self):
        self.library.add_book(self.book1)
        self.library.check_out_book("001")
        self.library.check_in_book("001")
        self.assertFalse(self.book1.is_checked_out)

    # def test_list_books(self):
    #     self.library.add_book(self.book1)
    #     self.library.add_book(self.book2)
    #     #expected_output = "001: 1984 by George Orwell, ISBN: 9780451524935 - Available\n" \
    #                       #"002: To Kill a Mockingbird by Harper Lee, ISBN: 9780060935467 - Available\n"
    #     self.assertEqual(self.library.list_books(), "expected_output")



class TestMembershipPlan(unittest.TestCase):
    def test_initialization(self):
        """Test if MembershipPlan initializes correctly with valid inputs."""
        plan = MembershipPlan("Gold", 5, 0.15)
        self.assertEqual(plan.plan_name, "Gold")
        self.assertEqual(plan.checkout_limit, 5)
        self.assertAlmostEqual(plan.discount_rate, 0.15)



class TestUser(unittest.TestCase):

    def setUp(self):
        self.book1 = Book("001", "1984", "George Orwell", "9780451524935")
        self.book2 = Book("002", "To Kill a Mockingbird", "Harper Lee", "9780060935467")
        self.user=User(123, "Alex")
        self.user.checked_out_books=[]
        # self.user.checked_in_books=[]

    def test_initialization(self):
        self.assertEqual(self.user.user_id,123)
        self.assertEqual(self.user.name,"Alex")
        self.assertEqual(self.user.checked_out_books,[])

    def test_check_out_book(self):
        self.book1.is_checked_out = False
        self.book1.title = "Test Book"
        self.user.checked_out_books = []
        self.user.check_out_book(self.book1)
        self.assertIn(self.book1, self.user.checked_out_books)
    
    def test_check_in_book(self):
        self.user.checked_out_books.append(self.book1)
        self.user.checked_out_books.append(self.book2)
        self.user.check_in_book(self.book1)
        self.assertNotIn(self.book1, self.user.checked_out_books)

    # def test_list_checked_out_books(self):
    #     self.user.checked_out_books.append(self.book1)
    #     self.user.checked_out_books.append(self.book2)
    #     # self.user.list_checked_out_books=[]
    #     captured_output = StringIO()
    #     sys.stdout = captured_output
        
    #     # Call the method to test
    #     self.user.list_checked_out_books()
        
    #     # Assert the correct output
    #     self.assertIn("Books checked out by Alex", captured_output.getvalue())
    #     self.assertIn("Book 1", captured_output.getvalue())
    #     self.assertIn("Book 2", captured_output.getvalue())
        
        # Reset stdout
        # sys.stdout = sys.__stdout__


class TestReservation(unittest.TestCase):
    def test_reservation_creation(self):
        # Create mock book and user objects
        self.book1 = Book("001", "1984", "George Orwell", "9780451524935")
        self.user=User(123, "Alex")
        
        # Create a reservation object
        self.reservation = Reservation(self.book1, self.user)
        
        # Assert that reservation is created correctly
        self.assertEqual(self.reservation.book, self.book1)
        self.assertEqual(self.reservation.user, self.user)
        self.assertTrue(self.reservation.active)


class TestBookReview(unittest.TestCase):
    def test_initialization(self):
        self.book = Book("001", "1984", "George Orwell", "9780451524935")
        self.user=User(123, "Alex")
        self.rating = 5
        self.review = "awesome"

        self.bookreview=BookReview(self.book, self.user, self.rating, self.review)
        # Assert that reservation is created correctly
        self.assertEqual(self.bookreview.book, self.book)
        self.assertEqual(self.bookreview.user, self.user)
        self.assertEqual(self.bookreview.rating, self.rating)
        self.assertEqual(self.bookreview.review, self.review)


class testNotificationSystem(unittest.TestCase):
    def test_init(self):
        self.manager = "Lavanya"
        self.notificationSystem= NotificationSystem(self.manager)
        self.assertEqual(self.notificationSystem.user_manager, self.manager)

    def test_send_due_date_reminder(self):
        # Create mock book and user objects
        book = Book("001", "1984", "George Orwell", "9780451524935")
        book.is_checked_out = True
        book.due_date = datetime(2024, 12, 10)

        user=User(123, "Alex")
        self.notificationSystem= NotificationSystem(user_manager=None)
        
        with patch("builtins.print") as mock_print:
            self.notificationSystem.send_due_date_reminder(user, book)

            # Assert the correct reminder message is printed
            mock_print.assert_called_with("Reminder: The book '1984' is due on 2024-12-10. Please return it on time.")

   
    def test_send_reservation_notification(self):
        book = Book("001", "1984", "George Orwell", "9780451524935")
        user=User(123, "Alex")
        self.notificationSystem= NotificationSystem(user_manager=None)
        
        with patch("builtins.print") as mock_print:
            self.notificationSystem.send_reservation_notification(user, book)

            mock_print.assert_called_with("Notification: The book '1984' you reserved is now available for checkout.")



class TestSearchSystem(unittest.TestCase):
    def setUp(self):
        # Create a library with mock data
        self.library = Library()
        self.library.add_book(Book("001", "1984", "George Orwell", "9780451524935"))
        self.library.add_book(Book("002", "Animal Farm", "George Orwell", "9780451526342"))
        self.library.add_book(Book("003", "To Kill a Mockingbird", "Harper Lee", "9780060935467"))
        self.library.add_book(Book("004", "Brave New World", "Aldous Huxley", "9780060850524"))
        
        # Create SearchSystem instance
        self.search_system = SearchSystem(self.library)

    def test_search_by_title(self):
        results = self.search_system.search_by_title("1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

    def test_search_by_author(self):
        results = self.search_system.search_by_author("George Orwell")
        self.assertEqual(len(results), 2)
        self.assertTrue(any(book.title == "1984" for book in results))
        self.assertTrue(any(book.title == "Animal Farm" for book in results))

    def test_search_by_isbn(self):
        results = self.search_system.search_by_isbn("9780060935467")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "To Kill a Mockingbird")


if __name__ == '__main__':
    unittest.main()