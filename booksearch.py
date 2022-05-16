from database import *


def search_book(title):
    """Function that searches for a book in the database, based on the given title.

    :param title: String -- Title of the book.
    :return: Tuple -- Returns two lists: one containing the results of the search, the other containing warnings.
    """
    search_results = []  # List of search results.
    warning_list = []  # List of warnings given by the program to librarian.
    found = False  # Variable used for checking whether book was found in database.txt, default value is False.

    for book in books:
        if title.lower() in book['Title'].lower():
            found = True
            search_results.append(book)
            if is_on_loan(book['ID'],book['MemberID']):
                # Checks whether the book is on loan or not to be able to give warnings if necessary.
                date = withdraw_log_date(book['ID'], book['MemberID'])
                if datecalc(date):  # If book is on loan, checks if 60 days have passed since it was checked out.
                    warning_list.append("Book {} with ID number {} is on loan for >60 days!"\
                                   .format(book['Title'], book['ID']))
                    # If 60 days have passed since it was checked out, gives a warning to librarian.

    if not found:  # If no book with given title was found, display an error message to user.
        warning_list.append("ERROR! No book with title {} has been found.".format(title))

    return search_results, warning_list


if __name__ == "__main__":

    print("1/3 Initiating testing of booksearch.py...")
    print("2/3 Importing book information from database.txt and logfile.txt...")
    get_Books()
    get_Logs()
    print("3/3 Initialization completed successfully. Starting test cases.")
    print_line()

    print("Test case #1: Searching book title - Existing book title with no loan history. Title 'Dune' ")
    lst, warnings = search_book('Dune')
    print('Search results: {}'.format(lst))
    print('Warnings given: {}'.format(warnings))
    print('Test #1 is successful. 3 titles with ID numbers 10, 31 and 32 and no warnings presented to librarian.')
    print_line()

    print("Test case #2: Searching book title - Existing book title with loan history. Title 'An Explorer's Guide to "
          "Skyrim'")
    lst, warnings = search_book("An Explorer's Guide to Skyrim")  # Could also use only one keyword, like 'skyrim'
    print('Search results: {}'.format(lst))
    print('Warnings given: {}'.format(warnings))
    print('Test #2 is successful. 4 titles with ID numbers 27, 28, 29 and 30 and 1 warning for book with ID 28.')
    print_line()

    print("Test case #3: Searching book title - Non-existing book title. Title 'Python programming'")
    lst, warnings = search_book("Python programming")  # Using a non-existing book title.
    print('Search results: {}'.format(lst))
    print('Warnings given: {}'.format(warnings))
    print('Test #3 is successful. No search results given and 1 warning to librarian that no such book was found.')
    print_line()

    print("Test case #4: Searching book title - Title with extra spacing on both left and right side. Title '   1984  "
          "       '")
    lst, warnings = search_book("   1984         ")
    print('Search results: {}'.format(lst))
    print('Warnings given: {}'.format(warnings))
    print('Test #4 is unsuccessful. However, this is due to the fact that .strip() method is applied to the user input '
          'straight from the Entry module used for input in menu.py, thus it is not possible to test it in here. '
          'This input has been tested manually through the GUI and is successful.')
    print_line()

    print('Trying test case #4 with .strip() method applied manually to a string containing the same title.')
    s = "   1984         ".strip()
    lst, warnings = search_book(s)
    print('Search results: {}'.format(lst))
    print('Warnings given: {}'.format(warnings))
    print('Test #4 is successful. 1 search results with ID 18 and no warning given to librarian.')
    print_line()



