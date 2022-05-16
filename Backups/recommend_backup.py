

def popular_genres(MemberID):
    """Creates a dictionary with all the genre of books and times taken on loan by user, sorted in descending order.

    :param MemberID: String -- Unique identifier of a user.
    :return: Dictionary -- Dictionary sorted in descending order, contains genre of book and times taken on loan.
    """
    popularityReturn = {}
    takenBooks = taken_books(MemberID)  # Gets the list of books taken by user and uses it to check for genres.

    for book in books:
        for elem in takenBooks:
            if book['ID'] == elem:
                key = book['Genre']
                if key in popularityReturn:  # Similar principle as functions above.
                    popularityReturn[key] += 1
                else:
                    popularityReturn[key] = 1

    popularityReturn = dict(sorted(popularityReturn.items(),key= lambda x:x[1], reverse= True))
    # Sorts the dictionary in descending order.

    return popularityReturn


def popular_authors(MemberID):
    """Creates a dictionary with all the authors of books and times taken on loan by user, sorted in descending order.

    :param MemberID: String -- Unique identifier of a user.
    :return: Dictionary -- Dictionary sorted in descending order, contains author of book and times taken on loan.
    """
    authorPopularity = {}
    takenBooks = taken_books(MemberID) # Gets the list of books taken by user and uses it to check for genres.

    for book in books:
        for elem in takenBooks:
            if book['ID'] == elem:
                key = book['Author']
                if key in authorPopularity:  # Similar principle as functions above.
                    authorPopularity[key] += 1
                else:
                    authorPopularity[key] = 1

    authorPopularity = dict(sorted(authorPopularity.items(),key= lambda x:x[1], reverse= True))
    # Sorts the dictionary in descending order.

    return authorPopularity

