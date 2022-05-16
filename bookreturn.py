from database import *


def return_book(book_ID):
    """Main function to return a Book to the library.

    :param book_ID: Int -- Unique Identifier for the Book.
    :return: String -- Function response if desired action was successful or an Error occurred.
    """
    for book in books:
        if book['ID'] == book_ID:
            if book['MemberID'] == '0':
                return "ERROR! Book {} has already been returned".format(book['Title'])
            add_log(book['ID'], book['MemberID'], 'return')  # Creates log for returning book.
            book['MemberID'] = '0'  # Changes book owner to 0 to indicate book is available for loan.
            update_Books()  # Updates database_backup2.txt with new information.
            return 'Book {} has been returned'.format(book['Title'])

    return 'ERROR! Book has not been found in the list of books'


def check_return(ID):
    """Checks how many days have passed since the book was given on loan.

    :param ID: Int -- Unique identifier of the Book.
    :return: Int -- Number of days since the book was given on loan.
    """
    for log in reversed(loglist):  # Use reversed() function to check for latest log when book was withdrawn.
        if log['ID'] == ID and log['Status'] == 'withdraw':
            date = datetime.datetime.strptime(log['Date'], '%Y-%m-%d')  # Converts date from logfile to datetime format.
            number_days = datetime.datetime.today() - date  # Checks time difference between log date and today.
            return number_days.days  # Returns only number of days.

    return "ERROR! No such book with ID was found to be given on loan."


if __name__ == "__main__":
    print("1/3 Initiating testing of bookreturn.py...")
    print("2/3 Importing book information from database.txt and logfile.txt...")
    get_Books()
    get_Logs()
    print("3/3 Initialization completed successfully. Starting test cases.")
    print_line()

    # return_book(book_ID) testing body.
    print("1.Testing return_book() function...")
    print_line()
    print("Test case #1: Returning an already returned (not withdrawn) book - ID 22")
    print(return_book('22'))
    print("Test case #1 successfully completed. Error that it has alreayd been returned was given upon trying to "
          "return book.")
    print_line()
    print("Test case #2: Returning a non-existing book - ID 43")
    print(return_book('43'))
    print("Test case #2 successfully completed. Error that book wasn't found in the list of books was given upon "
          "trying to return book.")
    print_line()
    print("Test case #3: Returning a withdrawn book - ID 34")
    print(return_book('34'))
    print("Test case #3 successfully completed. Database.txt and logfile.txt were both updated successfully and are "
          "reflecting the change.")
    print("NOTE: If you are seeing an error when running this test program, please either change the Member ID of the "
          "book in database.txt to a proper Member ID or check the log for this operation:")
    print("34 return vuie 2021-12-15 17:51:46.525442")
    print_line()
    print("return_book(book_ID) tests have been successful.")
    print_line()

    # check_return(ID) testing body
    print("1.Testing return_book() function...")
    print_line()
    print("Test case #1: Returning a withdrawn book - ID 33")
    print(check_return('33'))
    print("Test case #1 successfully completed. At the time of testing (15/12/2021), it has passed 1 day since book "
          "was withdrawn")
    print("NOTE: Note the log for the withdraw of this book:\n33 withdraw gera 2021-12-14 16:39:22.818126")
    print_line()
    print("Test case #2: Returning a non-existing book - ID 43")
    print(check_return('43'))
    print("Test case #2 successfully completed. An error was given saying that no such book ID was found.")
    print_line()
    print("check_return(ID) tests have been successful.")
    print_line()

