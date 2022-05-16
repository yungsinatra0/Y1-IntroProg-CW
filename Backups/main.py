import datetime

loglist = []
books = []
logs_columns = ['ID', 'Status', 'Date', 'member_Id']
data_columns = []

def get_Books():
    with open('database_backup2.txt') as f:
        s = f.readline()
        data_columns = s.split()

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
        [f.write('{} '.format(col)) for col in data_columns]
        f.write('\n')
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

    loglist.append(log)
    write_log(log)

def write_log(log):
    with open('../logfile.txt', 'a') as f:
        for key in log:
            f.write('{} '.format(log[key]))
        f.write('\n')

def datecalc(PurchaseDate):
    date_PurchaseDate = datetime.datetime.strptime(PurchaseDate, '%d/%m/%Y')
    diff = date_PurchaseDate + datetime.timedelta(days=60) <= datetime.datetime.today()
    return (diff)

def search_Book(title):
    lst = []
    for book in books:
        if book['Title'] == title:
            lst.append(book)
            if datecalc(book['PurchaseDate']):
                print("Warning! Book {} with ID number {} has been on loan for more than 60 days!"\
                      .format(book['Title'], book['ID']))
            # print(datecalc(book['PurchaseDate']))
    return(lst)

def check_memberid(ID):
    if len(ID) == 4 and ID.isalpha():
        return True
    return False

def withdraw_Book(title, ID):
    wsuccess = False

    if not check_memberid(ID):
        return ("error!")

    if check_memberid(ID) is False:
        print("ERROR! Please insert a valid ID!")
    else:
        for book in books:
            if book['Title'] == title:
                if book['MemberID'] == '0':
                    book['MemberID'] = ID
                    print("Book {} has been successfully withdrawn by user {}".format(book['Title'],
                                                                                          book['MemberID']))
                    wsuccess = True
                    update_Books()
                    add_log(book['ID'], ID, 'withdraw')
            if wsuccess:
                break
        if wsuccess is False: print('ERROR! There are no available copies of {} for loan for user {}'.format(title, ID))

def return_Book(book_ID):
    found = False
    for book in books:
        if book['ID'] == book_ID:
            found = True
            if book['MemberID'] == '0':
                print("ERROR! Book {} has already been returned".format(book['Title']))
            else:
                book['MemberID'] = '0'
                add_log(book_ID, book['MemberID'], 'return')
                update_Books()
                break
    if not found:
        print('ERROR! Book has not been found in the list of books')

get_Books()

# print(search_book("Book_1"))

#withdraw_book('Book_1','coai')
#ithdraw_Book('Book_1','coaie')
#withdraw_book('Book_1','coai3')
#withdraw_book('Book_1','ctai')
#withdraw_book('Book_1','cbai')
#withdraw_book('Book_1','cpai')
#withdraw_book('Book_1','coei')

#return_book('1')
# return_book('11')

print(search_Book("Book_1"))