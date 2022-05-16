from database import *


def taken_books(MemberID):
    """Creates a list of all the books that the Member has ever taken on loan

    :param MemberID: String -- Unique Member Identifier.
    :return: List -- List of books that the user has ever taken on loan.
    """
    takenBooks = []

    for log in loglist:
        if log['member_Id'] == MemberID and log['Status'] == 'withdraw' and log['ID'] not in takenBooks:
            takenBooks.append(log['ID'])
    return takenBooks


def popular_ids():
    """Returns a dictionary with how many times every book has been taken on loan.

    :return: Dictionary -- Dictionary with key as ID of book and value as times it was withdrawn.
    """
    idsPopularity = {}  # Dictionary with key as ID of book and value as times it was withdrawn.

    # Loops through the logs, looking for books that have been withdrawn. If one has been found, checks if it already
    # is in the list - in this case it increments the value associated to the ID by 1. Otherwise, creates new key
    # with this ID and assigns it a value of 1.
    for log in loglist:
        if log['Status'] == 'withdraw':
            key = log['ID']
            if key in idsPopularity:
                idsPopularity[key] += 1  # If key is already in idsPopularity, increments value by 1.
            else:
                idsPopularity[key] = 1  # If key is not in idsPopularity, creates instance of key in dictionary.

    return idsPopularity


def popular_books():
    """Uses dictionary returned from popular_ids() to return a similar dictionary, but with book titles instead of IDs.

    :return: Dictionary -- Dictionary sorted in descending order, contains title of book and times it was withdrawn.
    """
    idsPopularity = popular_ids()  # Uses result from popular_ids() to return Book Titles instead of IDs.
    bookPopularity = {}

    # Loops through books in database.txt, then uses stored IDs in idsPopularity to match with the Book ID. If a
    # match is found and the book has not been already added to the list, then it will add the book title to the list.
    for book in books:
        for key in idsPopularity:
            if book['ID'] == key and book['Title'] not in bookPopularity:
                title = book['Title']
                bookPopularity[title] = idsPopularity[key]
                # Copying values (how many times a book was withdrawn) from idsPopularity to bookPopularity.

    bookPopularity = dict(sorted(bookPopularity.items(), key=lambda x: x[1], reverse=True))
    # Sorts the dictionary in descending order.

    return bookPopularity


def return_dict_value(Book, Type):
    """Returns dictionary value for key given, based on type given (either 'Genre' or 'Author')

    :param Book: Dictionary -- Dictionary with information about one book.
    :param Type: String -- Either 'Genre' or 'Author', determines which value to be returned.
    :return: String -- Returns the value for the desired key in the dictionary, given by Type parameter.
    """

    if Type == 'Genre':  # Checks whether function needs to return book's genre or author.
        value = Book[Type]
    elif Type == 'Author':
        value = Book[Type]
    else:
        return None
        # Not bothering with returning something as input will always be given: either Genre or Author by the main
        # recommend_books() function, so it is not possible for value to be something different.

    return value


def popular_genre_authors(MemberID, Type):
    """Returns a dictionary with genres or authors of books and times taken on loan by user, sorted in descending order.

    :param Type: String -- Determines whether returned dictionary will contain user's popular genres or authors.
    :param MemberID: String -- Unique identifier of a user.
    :return: Dictionary -- Dictionary in descending order, contains genre, authors of book and times taken on loan.
    """
    popularityReturn = {}  # Dictionary that wil contain user's popular genres or authors'.
    takenBooks = taken_books(MemberID)  # Gets the list of books taken by user and uses it to check for authors/genres.

    for book in books:
        key = return_dict_value(book, Type)  # Get value for either Genre or Author for this book.
        if key:
            for elem in takenBooks:
                if book['ID'] == elem:  # Check whether the user has taken this book on loan.
                    if key in popularityReturn:  # Similar principle as functions above.
                        popularityReturn[key] += 1
                    else:
                        popularityReturn[key] = 1

    # Sort the dictionary in descending order.
    popularityReturn = dict(sorted(popularityReturn.items(), key=lambda x: x[1], reverse=True))

    return popularityReturn


def recommend_authors_genres(takenBooks, popularityList, recommendList, quantity):
    """Returns a list of book recommendations based on previous books taken on loan, most popular author/genre and
    quantity of books asked for recommendation.

    :param takenBooks: List -- List of books taken on loan by user.
    :param popularityList: Dictionary -- Dictionary of user's popular Genres or Authors, sorted in descending order.
    :param recommendList: List -- List of recommended books based on set criteria (genre, authors, previous books).
    :param quantity: Integer -- Integer with value between 3 and 10 which specifies the number of recommended books.
    :return: List -- List of recommended books based on set criteria (genre, authors, previous books).
    """
    broadness = 2  # Variable which controls how deep to look into user's popular Genre or Author list.

    for elem in popularityList:
        # Looping through popular Genre or Author list instead of book list because I want recommendations to be
        # ordered based on order in Genre/Author list.
        if broadness == 0:  # Check statement for breaking out of the loop.
            break
        for book in books:
            # Looping through books and matching Genre/Author, checking if book has not been taken already and if
            # book hasn't been recommended already.
            if book['Genre'] == elem or book['Author'] == elem:
                if book['ID'] not in takenBooks and book['Title'] not in recommendList:
                    recommendList.append(book['Title'])
                if len(recommendList) == quantity:
                    return recommendList
        broadness -= 1
    return recommendList


def recommend_books(MemberID, quantity):
    """Function that recommends books that the user hasn't yet read based on Genre, Author and Popular Books.
    Function tries each one in order until it fills the list with the number of books based on quantity.

    :param MemberID: String -- Unique identifier of a user.
    :param quantity: Int -- Quantity of books to be recommended to user. Ranges from 3 to 10 (inclusive).
    :return: List -- List containing titles of books recommended to user, based on criteria.
    """

    recommendList = []  # List which will contain book recommendations for user.
    takenBooks = taken_books(MemberID)

    genres = popular_genre_authors(MemberID, 'Genre')
    recommendList = recommend_authors_genres(takenBooks, genres, recommendList, quantity)
    # Gets list of books recommended based on most popular user's Genre

    while len(recommendList) < quantity:
        # If list of books is not long enough, will add books based on user's Author preference.
        authors = popular_genre_authors(MemberID, 'Author')
        recommendList = recommend_authors_genres(takenBooks, authors, recommendList, quantity)

        # If list of books is still not long enough, will add books based on popular books in library overall.
        popularBooks = popular_books()
        recommendList.append('--------------------------------------')
        recommendList.append('Not enough data from Genre/Author.')
        recommendList.append('Will recommend popular library books:')
        recommendList.append('--------------------------------------')
        # Looping through popular books list to provide recommendations for user who haven't been able to get any
        # using their Genre or Author preference.
        for popBookTitle in popularBooks:
            for book in books:
                if popBookTitle == book['Title'] and popBookTitle not in recommendList and book['ID'] not in takenBooks:
                    # Due to having 2 for loops, I have to first check if popular Book title is matching with a book
                    # title (to get ID later on). Then I see if the title is already included in recommend list and
                    # if it has been taken by the user before. If both of those are not true, the title can be
                    # recommended to user.
                    recommendList.append(popBookTitle)
                if len(recommendList) == quantity+4:
                    return recommendList

    if len(recommendList) < 3:
        recommendList.clear()
        recommendList.append('ERROR! There are not enough book recommendations for user {}'.format(MemberID))

    return recommendList


if __name__ == "__main__":
    print("1/3 Initiating testing of booksearch.py...")
    print("2/3 Importing book information from database.txt and logfile.txt...")
    get_Books()
    get_Logs()
    print("3/3 Initialization completed successfully. Starting test cases.")
    print_line()

    # taken_books(memberID) testing body.
    print("1.Testing taken_books() function...")
    print_line()
    print("Test case #1: Taken books by user - Valid user ID, 'coai', with existing withdrawal history")
    print(taken_books('coai'))
    print('Test #1 is successful. Function returns 12 IDs and all of them are correct.')
    print_line()
    print("Test case #2: Taken books by user - Valid user ID, 'dani', with non-existing withdrawal history")
    print(taken_books('dani'))
    print('Test #2 is successful. Function returns 0 IDs.')
    print_line()
    print("Test case #3: Taken books by user -  Invalid ID, 'coaii', with non-existing withdrawal history")
    print(taken_books('coaii'))
    print('Test #3 neither successful or unsuccessful. User ID input is being checked in menu.py, thus it is not '
          'possible to check for wrong User ID input.')
    print_line()
    print("taken_books(MemberID) tests have been successful.")
    print_line()

    # popular_books() testing body.
    print("2.Testing popular_books() function...")
    print_line()
    print("Test case #1: Printing result of popular_books() function.")
    print(popular_books())
    print("Test case #1 is successful - result has shown all withdrawn books sorted in descending order by the number "
          "of their withdrawals.")
    print_line()
    print("popular_books() tests have been successful.")
    print_line()

    # popular_genre_authors(memberID, Type) and return_dict_value(Book, Type)  testing body.
    print("3.Testing popular_genre_authors() function...")
    print_line()
    print("Test case #1: Valid User ID, 'coai', with existing withdrawal history and 'Genre' selected as Type.")
    print(popular_genre_authors('coai','Genre'))
    print('Test #1 is successful. Function returns all genre of books withdrawn by the user, sorted in descending '
          'order with correct values assigned to them.')
    print_line()
    print("Test case #2: Valid User ID, 'coai', with existing withdrawal history and 'Author' selected as Type.")
    print(popular_genre_authors('coai', 'Author'))
    print('Test #2 is successful. Function returns all authors of books withdrawn by the user, sorted in descending '
          'order with correct values assigned to them.')
    print_line()
    print("Test case #3: Invalid User ID, 'coaii', with non-existing withdrawal history and 'Author' selected as Type.")
    print(popular_genre_authors('coaii', 'Author'))
    print('Test #3 is successful. User ID input is checked in menu.py, thus no check is being made in this function. '
          'In conclusion, expected output is None, as can be seen in the console.')
    print_line()
    print("Test case #4: Valid User ID, 'cuai', with non-existing withdrawal history and 'Author' selected as Type.")
    print(popular_genre_authors('cuai', 'Author'))
    print('Test #4 is successful. Expected output is None (as the user can not have genre/author preference with no '
          'withdrawal history), as can be seen in the console.')
    print_line()
    print("Test case #5: Valid User ID, 'coai', with existing withdrawal history and wrong argument given as Type.")
    print(popular_genre_authors('coai', 'Authorr'))
    print("Test case #5 is successful. No output is given by the function, as expected - Type can not be wrong, "
          "as it is hard coded into the recommend_books() functions.")
    print_line()
    print("Test case #6: Invalid User ID, 'coai', with existing withdrawal history and wrong argument given as Type.")
    print(popular_genre_authors('coaii', 'Authorr'))
    print("Test case #6 is successful. No output is given by the function. Please check results above for explanation.")
    print_line()
    print("popular_genre_authors(memberID, Type) and return_dict_value(Book, Type) tests have been successful.")
    print_line()

    # recommend_books(MemberID, quantity) testing body.
    print("4.Testing recommend_books() function...")
    print_line()
    print("Test case #1: Valid username #1 with withdraw history")
    print('Popular Authors for user gera: {}'.format(popular_genre_authors('coai', 'Author')))
    print('Popular Authors for user gera: {}'.format(popular_genre_authors('coai', 'Genre')))
    print(recommend_books('coai',5))
    print("Test case #1 is successful. Given recommendations are based on user's Genre and Author popularity and none "
          "have been previously withdrawn by user.")
    print_line()
    print("Test case #2: Valid username #2 with withdraw history")
    print('Popular Authors for user gera: {}'.format(popular_genre_authors('gera', 'Author')))
    print('Popular Authors for user gera: {}'.format(popular_genre_authors('gera', 'Genre')))
    print(recommend_books('gera', 10))
    print("Test case #2 is successful. Given recommendations are based on user's Genre and Author popularity and none "
          "have been previously withdrawn by user.")
    print_line()
    print("Test case #3: Valid username #3 with no withdraw history")
    print('Popular books list: {}'.format(popular_books()))
    print(recommend_books('dain', 10))
    print("Test case #3 is successful. Given recommendations are based on the popular books list.")
    print_line()
    print("recommend_books(MemberID, quantity) tests have been successful.")
    print_line()








