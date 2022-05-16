import datetime

loglist = []
books = []
logs_columns = ['ID', 'Status', 'member_Id', 'Date']
data_columns = ['ID', 'Genre', 'Title', 'Author', 'PurchaseDate', 'MemberID']


def get_Books():
    with open('database_backup2.txt') as f:
        for line in f:
            book = {}
            row = line.split()
            i = 0
            for col in data_columns:
                book[col.strip()] = row[i].strip()
                i += 1
            books.append(book)


def update_Books():
    with open('database_backup2.txt', 'w') as f:
        for book in books:
            for key in book:
                f.write('{} '.format(book[key]))
            f.write('\n')


def add_log(book_ID, member_Id, status):
    log = {}
    log['ID'] = book_ID
    log['Status'] = status
    log['member_Id'] = member_Id
    log['Date'] = datetime.datetime.today()

    if not is_duplicate(log):
        loglist.append(log)
        write_log_file(log)

    return 'ERROR! Action {} has been done on book {} already'.format(status,book_ID)


def is_duplicate(log):
        if log['ID'] == loglist[-1]['ID']:
            if log['status'] == loglist[-1]['Status']:
                if log['member_Id'] == loglist[-1]['member_Id']:
                    return True
        return False


def write_log_file(log):
    with open('../logfile.txt', 'a') as f:
        for key in log:
            f.write('{} '.format(log[key]))
        f.write('\n')


def datecalc(date):
    formatted_date = datetime.datetime.strptime(date, '%d/%m/%Y')
    diff = formatted_date + datetime.timedelta(days=60) <= datetime.datetime.today()
    return (diff)

def is_on_loan(ID,MemberID):
    withdraw = False

    for log in loglist:
        if withdraw:
            if log['ID'] == ID and log['member_Id'] == MemberID and log['status'] == 'return':
                withdraw = False
        if log['ID'] == ID and log['member_Id'] == MemberID and log['status'] == 'withdraw':
            withdraw = True
    if withdraw:
        return True
    return False

def log_date(ID, MemberID):
    for log in reversed(loglist):
        if log['ID'] == ID and log['member_Id'] == MemberID and log['status'] == 'withdraw':
            return log['Date']


def search_Book(title):
    lst = []
    warning = []
    for book in books:
        if book['Title'] == title:
            lst.append(book)
            if is_on_loan(book['ID'],book['MemberID']):
                date = log_date(book['ID'],book['MemberID'])
                if datecalc(date):
                    warning.append("Warning! Book {} with ID number {} has been on loan for more than 60 days!"\
                                   .format(book['Title'], book['ID']))
    return lst, warning


def check_memberid(ID):
    if len(ID) == 4 and ID.isalpha():
        return True
    return False


# def hold_60days(ID):
#      for book in books:
#          if book['MemberID'] == ID and


def withdraw_Book(title, ID):
    if not check_memberid(ID):
        return "ERROR! Please insert a valid ID!"

    for book in books:
        if book['Title'] == title and book['MemberID'] == '0':
            book['MemberID'] = ID
            update_Books()
            print(add_log(book['ID'], ID, 'withdraw'))
            return "Book {} has been successfully withdrawn by user {}".format(book['Title'], book['MemberID'])

    return 'ERROR! There are no available copies of {} for loan'.format(title)


def return_Book(book_ID):
    for book in books:
        if book['ID'] == book_ID:

            if book['MemberID'] == '0':
                return "ERROR! Book {} has already been returned".format(book['Title'])

            print(add_log(book_ID, book['MemberID'], 'return'))
            book['MemberID'] = '0'
            update_Books()

            return 'Book {} has been returned'.format(book['Title'])

    return 'ERROR! Book has not been found in the list of books'


get_Books()

print(withdraw_Book('Book_1','coai'))
print(withdraw_Book('Book_1','coaie'))
# withdraw_book('Book_1','coai3')
# withdraw_book('Book_1','ctai')
# withdraw_book('Book_1','cbai')
# withdraw_book('Book_1','cpai')
# withdraw_book('Book_1','coei')

#return_book('1')
# return_book('11')

lst, warning = search_Book("Book_1")

print(warning)
print(lst)
