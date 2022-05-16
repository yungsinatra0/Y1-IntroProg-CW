from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import bookrecommend
import booksearch
import bookcheckout
import bookreturn
import database


def open_search_window():
    """Clears current window and creates Tkinter widgets necessary for searching a book in library database."""

    global enter_book_search  # Global because it is used by function below.
    delete_buttons()  # Clears menu buttons.

    # Creating widgets for the search part of the program.

    # Text label accompanying the entry widget.
    title = Label(window, text='Insert book title: ', font="Courier 10 bold")
    title.grid(row=0, column=0)
    # Search button that will trigger display_search_results().
    search_button = Button(window, text='Search for a book', font=('Arial', 10, 'bold'),
                           command=display_search_results)
    search_button.grid(row=0, column=2, sticky='w')
    # Entry widget to enter book title.
    enter_book_search = Entry(window, width=20)
    enter_book_search.grid(row=0, column=1)
    enter_book_search.focus_set()
    # Back button to go back to main menu
    back_button = Button(window, text='<- Back', font=('Arial', 10, 'bold'), command=reset_buttons)
    back_button.grid(row=6, column=0)


def display_search_results():
    """Reads input from enter_book_search and displays results of book title search in the book database."""

    bookname = enter_book_search.get().strip()  # Get book Title from Entry widget in the window.

    # Creating widgets for displaying search results and warnings (if applicable).

    # Scrollbar to scroll through search results.
    search_scrollbar = Scrollbar(window, orient=VERTICAL)
    search_scrollbar.grid(row=3, column=1, ipady=50, sticky='w')

    results, warnings = booksearch.search_book(bookname)
    # Text label accompanying the listbox widget.
    bookListTitle = Label(window, text='Search results: ', font="Courier 10 bold")
    bookListTitle.grid(row=2, column=0)
    # Listbox widget will display search results.
    bookList = Listbox(window, width=120, yscrollcommand=search_scrollbar.set)
    bookList.grid(row=3, column=0)

    # Creating widgets for displaying warning messages for the librarian.
    warningList = Listbox(window, width=80)
    warningList.grid(row=5, column=0)
    warningListTitle = Label(window, text='Warnings for the librarian: ', font="Courier 10 bold")
    warningListTitle.grid(row=4, column=0)

    # Writing database header columns to the first line of listbox widget.
    s = ''  # Temporary string variable for displaying header columns.
    for column in database.data_columns:
        s += column + ' | '
    bookList.insert(END, s)

    # Loop for writing search results to Listbox widget.
    for book in results:
        s = ''  # Temporary string variable for displaying search results
        for key in book:
            s += book[key] + ' | '  # Adding all elements of the book dictionary to the temporary string variable.
        bookList.insert(END, s)  # Writing temporary string variable to the listbox widget.
    search_scrollbar.config(command=bookList.yview)  # Adding scrollbar to listbox.

    if warnings:
        # Displays warnings in warningList widget.
        for warning in warnings:
            warningList.insert(END, warning)


def open_withdraw_window():
    """Clears current window and creates Tkinter widgets necessary for withdrawing a book from the library database."""

    global enter_book_withdraw  # Variables have global scope because they are used by function below.
    global enter_ID_withdraw
    global withdraw_response
    # Also made withdraw_response global because otherwise program will keep making new label widgets, which makes them
    # overlap if used multiple times.
    delete_buttons()

    # Creating widgets for withdraw part of the program.

    # Text label accompanying the book ID entry widget.
    title = Label(window, text='Enter book ID: ', font="Courier 10 bold")
    title.grid(row=0, column=0, sticky='w')
    # Withdraw button that will trigger withdraw_book_message().
    withdraw_button = Button(window, text='Withdraw the book', font=('Arial', 10, 'bold'),
                             command=withdraw_book_message)
    withdraw_button.grid(row=0, column=4, sticky='w')
    # Entry widget to enter book ID.
    enter_book_withdraw = Entry(window, width=6)
    enter_book_withdraw.grid(row=0, column=1, sticky='w')
    enter_book_withdraw.focus_set()
    # Text label accompanying the member ID entry widget.
    title2 = Label(window, text='Enter member ID: ', font="Courier 10 bold")
    title2.grid(row=1, column=0, sticky='w')
    # Entry widget to enter member ID.
    enter_ID_withdraw = Entry(window, width=6)
    enter_ID_withdraw.grid(row=1, column=1, sticky='w')
    # Back button to go back to main menu
    back_button = Button(window, text='<- Back', font=('Arial', 10, 'bold'), command=reset_buttons)
    back_button.grid(row=3, column=0)
    # Text label to display warnings for withdrawing to librarian.
    withdraw_response = Label(window, font='Courier 8 bold')
    withdraw_response.grid(row=0, column=5)


def withdraw_book_message():
    """Reads input from enter_book_withdraw and enter_ID_withdraw and displays response of withdraw_book() function."""

    # Getting values for book & user ID and also clearing the entry widgets for further introduction of data.
    book_id = enter_book_withdraw.get().strip()
    memberID = enter_ID_withdraw.get().strip().lower()
    enter_book_withdraw.delete(0, END)
    enter_ID_withdraw.delete(0, END)
    enter_book_withdraw.focus_set()

    # Check if MemberID given is valid or not. If it is not, will not display any other withdraw related widgets and
    # instead will display an error message to the user.
    if not database.check_member_id(memberID):
        withdraw_response.config(text='ERROR! Please insert a valid ID - it must be 4 English alphabet letters!')
    else:
        # Calling withdraw_book() and additional_books() functions and displaying their responses.
        message = 'Result: ' + bookcheckout.withdraw_book(book_id, memberID)
        booklist = bookcheckout.additional_books(memberID)
        withdraw_response.config(text=message)

        # Creating widget for displaying warning messages for holding books >60 days.
        warningList = Listbox(window, width=40)
        warningList.grid(row=4, column=5)
        warningListTitle = Label(window, text='User {} is holding these books for >60 days: '.format(memberID),
                                 font="Courier 10 bold")
        warningListTitle.grid(row=3, column=5)

        # If there are any additional books held by the user for more than 60 days, displays a warning with their
        # respective IDs
        if booklist:
            for elem in booklist:
                # Adding message line for each book held for more than 60 days.
                msg = 'Book with ID number {}'.format(elem)
                warningList.insert(END, msg)


def open_return_window():
    """Clears current window and creates Tkinter widgets necessary for returning a book."""

    global enter_book_return  # Usage of global scope as in the withdraw function above.
    global return_response
    global return_warning
    delete_buttons()

    # Creating widgets for return part of the program

    # Text label accompanying the book ID entry widget.
    title = Label(window, text='Enter book ID: ', font="Courier 10 bold")
    title.grid(row=0, column=0)
    # Return button that will trigger return_book_message().
    return_button = Button(window, text='Return the book', font=('Arial', 10, 'bold'),
                           command=return_book_message)
    return_button.grid(row=1, column=0)
    # Entry widget to enter book ID.
    enter_book_return = Entry(window, width=10)
    enter_book_return.grid(row=0, column=1)
    enter_book_return.focus_set()
    # Back button to go back to main menu
    back_button = Button(window, text='<- Back', font=('Arial', 10, 'bold'), command=reset_buttons)
    back_button.grid(row=3, column=0)
    # Text label to display return results to librarian.
    return_response = Label(window, font='Courier 8 bold')
    return_response.grid(row=0, column=3)
    # Text label to display warnings for withdrawing to librarian.
    return_warning = Label(window, font='Courier 8 bold')
    return_warning.grid(row=1, column=3)


def return_book_message():
    """Reads input from enter_book_return and displays response of return_book() function."""

    # Getting values for book ID and also clearing the entry widget for further introduction of data.
    book_id = enter_book_return.get().strip()
    enter_book_return.delete(0, END)
    enter_book_return.focus_set()

    # Calling return_book() function and displaying the response.
    message = 'Result: ' + bookreturn.return_book(book_id)
    return_response.config(text=message)

    days = bookreturn.check_return(book_id)
    if 'ERROR!' not in message and days > 60:
        # If there is no error in returning the book and more than 60 days have passed since it has been taken on
        # loan, display a warning message to librarian that user is returning book after more than 60 days.
        msg = 'Warning! User is returning this book after {} days!'.format(days)
        return_warning.config(text=msg)
    else:
        return_warning.config(text='')


def open_recommend_window():
    """Clears current window and creates Tkinter widgets necessary for recommending books for user."""

    global enter_member_recommend  # Same principle applied for global scope as in previous functions.
    global quantity
    global recommend_message
    delete_buttons()

    # Creating widgets for recommendation part of the program

    # Text label accompanying the member ID entry widget.
    title = Label(window, text='Enter member ID: ', font="Courier 10 bold")
    title.grid(row=0, column=0, sticky='w')
    # Recommend button that will trigger display_recommend_results().
    recommend_button = Button(window, text='Recommend books', font=('Courier', 10, 'bold'),
                              command=display_recommend_results)
    recommend_button.grid(row=1, column=2, sticky='w')
    # Entry widget to enter member ID.
    enter_member_recommend = Entry(window, width=10)
    enter_member_recommend.grid(row=0, column=1, sticky='w')
    enter_member_recommend.focus_set()
    # Scale widget to select quantity of book recommendations to display.
    quantity = Scale(window, from_=3, to=10, orient=HORIZONTAL)
    quantity.grid(row=0, column=2, sticky='w')
    # Back button to go back to main menu
    back_button = Button(window, text='<- Back', font=('Arial', 10, 'bold'), command=reset_buttons)
    back_button.grid(row=3, column=0)
    # Text label to display warnings or other messages to librarian.
    recommend_message = Label(window, font=('Courier', 10, 'bold'))
    recommend_message.grid(row=0, column=3)


def display_recommend_results():
    """Reads Member ID as input, then displays list of recommended books based on criteria: Genre, Author, etc."""

    # Getting values for MemberID and quantity from window widgets, then calling recommend_books() function and
    # displaying results.
    memberID = enter_member_recommend.get().strip().lower()
    number = quantity.get()
    results = bookrecommend.recommend_books(memberID, number)

    # Check if MemberID given is valid or not. If it is not, will not display any other recommendation related widgets
    # and instead will display an error message to the user.
    if not database.check_member_id(memberID):
        recommend_message.config(text='ERROR! Please insert a valid ID - it must be 4 English alphabet letters!')
    else:
        # Creating widgets for displaying recommendation results.
        recommend_scrollbar = Scrollbar(window, orient=VERTICAL)
        recommend_scrollbar.grid(row=2, column=1, ipady=50, sticky='n')
        recommend_message.config(text='Recommended book list for user {}'.format(memberID))
        recommend_message.grid(row=1, column=0)
        recommendList = Listbox(window, width=40, yscrollcommand=recommend_scrollbar.set)
        recommendList.grid(row=2, column=0, sticky='n')

        # Adding and displaying results using the recommendList widget.
        for result in results:
            recommendList.insert(END, result)
        recommend_scrollbar.config(command=recommendList.yview)

        # Creating and displaying graph based on genre criteria for user with memberID.
        create_graph(memberID)


def create_graph(MemberID):
    """Creates a Pie Chart based on a User's genre preference

    :param MemberID: String -- Member unique identifier, formed of 4 characters
    :return: None
    """
    genres = bookrecommend.popular_genre_authors(MemberID, 'Genre')  # Get a list of user's popular genres.

    # Create data sets that wil be used for pie chart creation.
    labels = list(genres.keys())
    values = list(genres.values())

    # Creating pie chart figure.
    fig = plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels)
    plt.legend(title="Popular genres for user {}".format(MemberID), loc='lower left', fontsize='x-small',
               bbox_to_anchor=(-0.18, -0.15))

    # Creating canvas for embedding matplotlib pie chart into Tkinter window.
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=2)


def set_buttons():
    """Creates and displays the buttons for the main menu."""

    search_window = Button(window, text="Search for a book", font="Arial 14 bold", command=open_search_window)
    search_window.grid(row=1, column=0, sticky='w')
    checkout_window = Button(window, text="Withdraw a book", font="Arial 14 bold", command=open_withdraw_window)
    checkout_window.grid(row=2, column=0, sticky='w')
    return_book_window = Button(window, text="Return a book", font="Arial 14 bold", command=open_return_window)
    return_book_window.grid(row=3, column=0, sticky='w')
    recommend_book_window = Button(window, text="Recommend a book", font="Arial 14 bold", command=open_recommend_window)
    recommend_book_window.grid(row=4, column=0, sticky='w')
    exit_button = Button(window, text="EXIT", font="Arial 8 bold", command=window.destroy)
    exit_button.grid(row=5, column=1)


def delete_buttons():
    """Deletes all widgets in the window."""

    list = window.grid_slaves()
    for elem in list:
        elem.destroy()


def reset_buttons():
    """Resets the current window to the main menu."""

    delete_buttons()
    window.geometry("1100x800")
    set_buttons()


"""
Start main program
"""

window = Tk()
window.title("Library manager")
window.geometry("1100x800")

database.get_Books()
database.get_Logs()
set_buttons()

window.mainloop()
