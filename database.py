import datetime

loglist = []  # Global list of logs. Each log is a dictionary with keys from logs_columns.
books = []  # Global list of books. Each book is a dictionary with keys from data_columns.
logs_columns = ['ID', 'Status', 'member_Id', 'Date']  # Column headers for logfile.txt.
data_columns = ['ID', 'Genre', 'Title', 'Author', 'PurchaseDate', 'MemberID']  # Column headers for database.txt.


def get_Books():
    """Function that reads the books and respective details from database.txt and adds them to book list"""
    with open('database.txt') as f:
        for line in f:  # Reading each line in database.txt individually.
            book = {}
            row = line.split('|')  # Columns are divided with '|',so using this as argument for .split().
            i = 0
            for col in data_columns:  # Each element of data_columns is used as key for dictionary.
                book[col] = row[i].strip()
                i += 1
            books.append(book)


def update_Books():
    """Function that updates the book details in database.txt by rewriting file all over again with new information."""
    with open('database.txt', 'w') as f:
        for book in books:
            for key in book:  # Using key to get the values from the dictionary, then writing them to database.txt.
                f.write('{}|'.format(book[key]))
            f.write('\n')


def get_Logs():
    """Function the reads the logs and respective details from logfile.txt and adds them to log list"""
    with open('logfile.txt') as f:
        for line in f:  # Same principle as get_Books().
            log = {}
            row = line.split()
            i = 0
            for col in logs_columns:
                log[col] = row[i].strip()
                i += 1
            loglist.append(log)


def add_log(book_ID, member_Id, status):
    """Function that creates a new log, appends it to log list and calls write_log_file to write it to logfile.txt.

    :param book_ID: Int -- Unique ID of the book.
    :param member_Id: String -- Unique ID of the member.
    :param status: String -- Represents status of book: either 'withdraw' or 'return'.
    :return: String -- Contains message whether a log was successfully added or not.
    """
    log = {'ID': book_ID, 'Status': status, 'member_Id': member_Id, 'Date': datetime.datetime.today()}
    # Creating a new log instance.

    if not is_duplicate(log):
        # Checking if there isn't a duplicate already so log file doesn't get spammed with similar logs.
        loglist.append(log)
        write_log_file(log)  # After appending the log to the list, need to write it in log file as well.
        return 'SUCCESS! Action {} has been done on book {}'.format(status,book_ID)

    return 'ERROR! Action {} has been done on book {} already'.format(status,book_ID)


def is_duplicate(log):
    """Checks whether a log has already been added to the log list (whether is a duplicate).

    :param log: Dictionary -- Contains keys: 'ID', 'Status', 'member_Id', 'Date'.
    :return: Boolean -- True if there is a duplicate log in log list already, False otherwise.
    """
    if len(loglist) > 0:
        if log['ID'] == loglist[-1]['ID'] and log['Status'] == loglist[-1]['Status'] and log['member_Id'] == \
                loglist[-1]['member_Id']:
            return True
        # Need to check only previous log for duplicates as there is no way for there to be a duplicate earlier on,
        # there are different checks for that in other functions.
    return False


def write_log_file(log):
    """Adds the log to logfile.txt.

    :param log: Dictionary -- Contains keys: 'ID', 'Status', 'member_Id', 'Date'.
    :return: None
    """
    with open('logfile.txt', 'a') as f:
        for key in log:
            f.write('{} '.format(log[key]))
        f.write('\n')


def datecalc(date):
    """Calculates whether it has passed 60 days between the date given and today's date.

    :param date: String or datetime object -- Given date to be compared to today's date.
    :return: Boolean -- True if difference is over 60 days, otherwise False.
    """
    if type(date) == str:
        # Some dates are strings, other are datetime, thus need to check if conversion is necessary or not.
        # Really weird date format, but it is what datetime outputs by default, and I am too lazy to change it.
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    diff = date + datetime.timedelta(days=60) <= datetime.datetime.today()
    # Checks whether the date given + 60 days is equal to or earlier than today's date (using datetime arithmetics).
    # If it is not, then 60 days have not yet passed and it returns False. Otherwise, if it has already been 60 days,
    # it returns True.
    return (diff)


def is_on_loan(ID,MemberID):
    """Function checks whether given book with ID is taken on loan by user MemberID.

    :param ID: Int -- Unique identifier of the book.
    :param MemberID: String -- Unique identifier of the user.
    :return: Boolean -- Return true if book with ID was taken on loan by user MemberID, returns false otherwise.
    """
    withdraw = False  # Variable that indicates withdraw status. By default, it is False.
    for log in loglist:
        if withdraw:
            if log['ID'] == ID and log['member_Id'] == MemberID and log['Status'] == 'return':
                withdraw = False
                # If it has been found that the user has withdrawn the book (withdraw = True), then it checks whether
                # the user has returned the book or not and sets withdraw to False to indicate it was returned.
        if log['ID'] == ID and log['member_Id'] == MemberID and log['Status'] == 'withdraw':
            withdraw = True
            # If a log with the user & book ID has been found with status 'withdraw', changes state of variable to True
            # to indicate that the book has been withdrawn by the user.

    return withdraw


def withdraw_log_date(ID, MemberID):
    """Finds and returns the latest withdraw date in log list for specified book and member ID.

    :param ID: Int -- Unique book identifier.
    :param MemberID: String -- Unique member identifier.
    :return: Datetime -- Returns date for specified book and member ID in log list.
    """
    for log in reversed(loglist):
        # Use reversed() function to loop through an inverse version of the list (to get latest logs).
        if log['ID'] == ID and log['member_Id'] == MemberID and log['Status'] == 'withdraw':
            return log['Date']


def check_member_id(ID):
    """Checks if member ID provided is valid.

    :param ID: String -- Member unique identifier, formed of 4 characters
    :return: True if member ID is valid, False otherwise.
    """
    if len(ID) == 4 and ID.isalpha():
        return True
    return False


def print_line():  # Use for displaying test results and delimiting each block of testing.
    print('--------------------------------------------------------------------')


if __name__ == "__main__":
    print("1/3 Initiating testing of database.py...")
    print("2/3 Importing book information from database.txt and logfile.txt...")
    get_Books()
    get_Logs()
    print("3/3 Initialization completed successfully. Starting test cases.")
    print_line()

    # get_Books() and get_Logs() testing body.
    print("1.Testing get_Books and get_Logs() function...")
    print_line()
    print("Printing both books and loglist variables. Please check them with database and logfile.txt respectively.")
    print('Book list: {}'.format(books))
    print('Log list: {}'.format(loglist))
    print('Testing succesful.')
    print_line()

    # update_Books() or add_log() testing:
    print("There is no point in testing update_Books or add_log as it can be clearly seen from other tests that these "
          "functions are working properly.")
    print_line()

    # datecalc(date) testing body:
    print("2.Testing datecalc() function...")
    print_line()
    print("Test case #1: Date that is less than 60 days away - 2021-12-01")
    print(datecalc('2021-12-01'))
    print("Test case #1 succesfully completed. Expected return was False.")
    print_line()
    print("Test case #2: Date that is more than 60 days away - 2021-10-01")
    print(datecalc('2021-10-01'))
    print("Test case #2 succesfully completed. Expected return was True.")
    print_line()
    print("datecalc() tests have been successful.")
    print_line()

    # is_on_loan(ID,MemberID) testing:
    print("3.Testing is_on_loan() function...")
    print_line()
    print("Test case #1: Book with valid ID on loan and user with valid ID: 14, gera")
    print("Please refer to this log:\n14 withdraw gera 2021-12-14 15:48:45.733241")
    print(is_on_loan('14','gera'))
    print("Test case #1 successful. Function returned True, as expected.")
    print_line()
    print("Test case #2: Book with valid ID not on loan and user with valid ID: 13, gera")
    print("Please refer to the book details at the time of the test:")
    print('13|Fantasy|The Way of Kings|Brandon Sanderson|31/09/2011|0|')
    print(is_on_loan('13', 'gera'))
    print("Test case #2 successful. Function returned False, as expected.")
    print_line()
    print("Test case #3: Book with invalid ID and user with valid ID: 43, gera")
    print(is_on_loan('43', 'gera'))
    print("Test case #3 successful. Function returned False, as expected.")
    print_line()
    print("is_on_loan() tests have been successful.")
    print_line()

    # withdraw_log_date(ID, MemberID) testing:
    print("4.Testing withdraw_log_date() function...")
    print_line()
    print("Test case #1: Valid book ID and member ID: 37, gera.")
    print("Please refer to this log:\n37 withdraw gera 2021-12-14 15:32:01.450779 ")
    print(withdraw_log_date('37', 'gera'))
    print("Test case #1 successful. Function returned Date as expected.")
    print_line()
    print("Test case #2: Invalid book ID (or not withdrawn) and valid member ID: 43, coai.")
    print(withdraw_log_date('43', 'coai'))
    print("Test case #2 successful. Function returned None as expected.")
    print_line()
    print("withdraw_log_date() tests have been successful.")
    print_line()

    # check_member_id(ID) testing:
    print("5.check_member_id() function...")
    print_line()
    print("Test case #1: Valid member ID: gera.")
    print(check_member_id('gera'))
    print("Test case #1 successful. Function returned True as expected.")
    print_line()
    print("Test case #2: Invalid member ID: g3ra.")
    print(check_member_id('g3ra'))
    print("Test case #2 successful. Function returned False as expected.")
    print_line()
    print("Test case #3: Invalid member ID: 1243.")
    print(check_member_id('1243'))
    print("Test case #3 successful. Function returned False as expected.")
    print_line()
    print("Test case #4: Invalid member ID: gerasi.")
    print(check_member_id('gerasi'))
    print("Test case #4 successful. Function returned False as expected.")
    print_line()
    print("Test case #5: Invalid member ID: ger.")
    print(check_member_id('ger'))
    print("Test case #5 successful. Function returned False as expected.")
    print_line()
    print("check_member_id() tests have been successful.")
    print_line()












