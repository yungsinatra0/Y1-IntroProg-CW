from tkinter import *
from tkinter import messagebox
import sys

sys.path.append('../modules')

import booksearch
import bookcheckout
import bookreturn
import bookrecommend
import database


def open_search_window():
    global enter_book_search
    global searchWindow

    searchWindow = Toplevel(window)
    searchWindow.title("Search for a title")
    searchWindow.geometry("500x400")

    title = Label(searchWindow, text='Insert book title: ', font="Courier 10 bold")
    title.grid(row=0, column=0)
    search_button = Button(searchWindow, text='Search for a book', font=('Arial', 10, 'bold'),
                           command=display_search_results)
    search_button.grid(row=1, column=0)
    enter_book_search = Entry(searchWindow, width=20)
    enter_book_search.grid(row=0, column=1)
    enter_book_search.focus_set()


def display_search_results():
    search_scrollbar = Scrollbar(searchWindow, orient=VERTICAL)
    search_scrollbar.grid(row=2, column=1, ipady=50)

    bookname = enter_book_search.get()
    results, warnings = booksearch.search_book(bookname)
    bookList = Listbox(searchWindow, width=40, yscrollcommand=search_scrollbar.set)
    bookList.grid(row=2, column=0)

    for book in results:
        s = ""
        for key in book:
            s += book[key] + ' '
        bookList.insert(END, s)
    search_scrollbar.config(command=bookList.yview)

    if warnings:
        msg = '\n'.join(warnings)
        messagebox.showwarning(title="Attention!", message=msg, parent=searchWindow)


def open_withdraw_window():
    global enter_book_withdraw
    global enter_ID_withdraw
    global withdrawWindow

    withdrawWindow = Toplevel(window)
    withdrawWindow.title("Check out a title")
    withdrawWindow.geometry("600x100")

    title = Label(withdrawWindow, text='Enter book & member ID: ', font="Courier 10 bold")
    title.grid(row=0, column=0)
    withdraw_button = Button(withdrawWindow, text='Withdraw the book', font=('Arial', 10, 'bold'),
                             command=withdraw_book_message)
    withdraw_button.grid(row=1, column=0)
    enter_book_withdraw = Entry(withdrawWindow, width=3)
    enter_book_withdraw.grid(row=0, column=1)
    enter_book_withdraw.focus_set()
    enter_ID_withdraw = Entry(withdrawWindow, width=6)
    enter_ID_withdraw.grid(row=0, column=2)


def withdraw_book_message():
    book_id = enter_book_withdraw.get()
    ID = enter_ID_withdraw.get()
    message = bookcheckout.withdraw_book(book_id, ID)
    list = bookcheckout.additional_books(ID)

    response = Label(withdrawWindow, text=message, font='Courier 8 bold')
    response.grid(row=2, column=0)

    if list:
        msg = 'Attention! User {} is holding the following books for more than 60 days: \n'.format(ID)
        for elem in list:
            msg += 'Book {} with ID number {}\n'.format(elem[2],elem[0])
        messagebox.showwarning(title="Attention!", message=msg, parent=withdrawWindow)


def open_return_window():
    global enter_book_return
    global returnWindow

    returnWindow = Toplevel(window)
    returnWindow.title("Return a book")
    returnWindow.geometry("600x100")

    title = Label(returnWindow, text='Enter book ID: ', font="Courier 10 bold")
    title.grid(row=0, column=0)
    return_button = Button(returnWindow, text='Return the book', font=('Arial', 10, 'bold'),
                             command=return_book_message)
    return_button.grid(row=1, column=0)
    enter_book_return = Entry(returnWindow, width=10)
    enter_book_return.grid(row=0, column=1)
    enter_book_return.focus_set()


def return_book_message():
    book_id = enter_book_return.get()
    message = bookreturn.return_book(book_id)

    response = Label(returnWindow, text=message, font='Courier 8 bold')
    response.grid(row=2, column=0)

    days = bookreturn.check_return(book_id)
    if days > 60:
        msg = 'User is returning this book after {} days!'.format(days)
        messagebox.showwarning(title="Attention!", message=msg, parent=returnWindow)

def set_buttons():
    search_window = Button(window, text="Search for a book", font="Arial 14 bold", command=open_search_window)
    search_window.grid(row=1, column=0)
    checkout_window = Button(window, text="Withdraw a book", font="Arial 14 bold", command=open_withdraw_window)
    checkout_window.grid(row=2, column=0)
    return_book_window = Button(window, text="Return a book", font="Arial 14 bold", command=open_return_window)
    return_book_window.grid(row=3, column=0)
    recommend_book_window = Button(window, text="Recommend a book", font="Arial 14 bold")
    recommend_book_window.grid(row=4, column=0)

"""
Start main program
"""

window = Tk()
window.title("Library manager")
window.geometry("250x200")

database.get_Books()
database.get_Logs()
set_buttons()

window.mainloop()
