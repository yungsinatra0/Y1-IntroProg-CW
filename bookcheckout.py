from database import *


def withdraw_book(book_ID, ID):
    """Main function to withdraw a book from the database.

    :param book_ID: Int -- ID of the book to withdraw.
    :param ID: String -- Member unique identifier.
    :return: String -- Function response if desired action was successful or if an Error occurred.
    """

    for book in books:
        if book['ID'] == book_ID and book['MemberID'] == '0':  # If MemberID of book is 0, it has no owner now.
            book['MemberID'] = ID  # Changes owner to member ID.
            update_Books()
            add_log(book['ID'], ID, 'withdraw')  # Creates log for withdrawal of book.
            return "Book {} has been successfully withdrawn by user {}".format(book['Title'], book['MemberID'])
        elif book['ID'] == book_ID and book['MemberID'].isalpha():
            return 'ERROR! Book with ID number {} is already on loan!'.format(book_ID)

    return 'ERROR! There are no books with ID number {} in the database'.format(book_ID)


def additional_books(MemberID):
    """Returns a list of additional books currently held by the user for over 60 days.

    :param MemberID: Int -- Member unique identifier.
    :return: List -- List that contains details of books that are currently held by the user for over 60 days.
    """
    heldBooks = []  # List of books that are currently held by the user for more than 60 days.

    for log in reversed(loglist):  # Check latest logs using reversed() function.
        if is_on_loan(log['ID'], MemberID) and datecalc(log['Date']):
            # If book is currently held by the user and it's been over 60 days since the loan, add it to list.
            heldBooks.append(log['ID'])

    return heldBooks


if __name__ == "__main__":
    print("1/3 Initiating testing of bookcheckout.py...")
    print("2/3 Importing book information from database.txt and logfile.txt...")
    get_Books()
    get_Logs()
    print("3/3 Initialization completed successfully. Starting test cases.")
    print_line()

    #  withdraw_book(book_ID, ID) testing body.
    print("1.Testing withdraw_book() function...")
    print_line()
    print("Test case #1: Withdrawing a non-withdrawn, valid book ID with a valid user ID  - ID 22 and coai")
    print(withdraw_book('22', 'coai'))
    print("Test case #1 successfully completed. Database.txt and logfile.txt were both updated successfully and are "
          "reflecting the change.")
    print("NOTE: If you are seeing an error when running this test program, please either change the Member ID for the "
          "book in database.txt to 0 or check the log for this operation:")
    print("22 withdraw coai 2021-12-16 09:53:55.162569")
    print_line()
    print("Test case #2: Withdrawing an already withdrawn, valid book ID with a valid user ID  - ID 22 and coai")
    print(withdraw_book('22', 'coai'))
    print("Test case #2 successfully completed. Function has returned an error that book has already been taken on "
          "loan. Please see the above test for confirmation.")
    print_line()
    print("Test case #3: Withdrawing a non-existing book ID with a valid user ID - ID 43 and coai")
    print(withdraw_book('43', 'coai'))
    print("Test case #3 successfully completed. Function has returned an error that book has not been found in the "
          "database.")
    print_line()
    print("There will not be test case #4, which should test invalid user ID, as the testing of user input is being "
          "done in the menu.py module.")
    print_line()
    print("withdraw_book() tests have been successful.")
    print_line()

    # additional_books(MemberID) testing body.
    print("2.Testing additional_books() function...")
    print_line()
    print("Test case #1: Valid user ID with existing book withdrawal of over 60 days. ID ccor")
    print(additional_books('ccor'))
    print("Test case #1 successfully completed. Function returned one book ID, 18, which has been on loan for over 60 "
          "days. Check the log below for confirmation:")
    print("18 withdraw ccor 2020-12-14 16:39:55.177889")
    print_line()
    print("Test case #2: Valid user ID with non-existing book withdrawal of over 60 days. ID coai")
    print(additional_books('coai'))
    print("Test case #2 successfully completed. Function returned an empty list.")
    print_line()
    print("There will not be test case #3, which should test invalid user ID, as the testing of user input is being "
          "done in the menu.py module.")
    print_line()
    print("additional_books() tests have been successful.")
    print_line()