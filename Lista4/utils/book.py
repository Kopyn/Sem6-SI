class Book():
    def __init__(self, book_title = "", genres = "", summary = ""):
        self.book_title = book_title
        self.genres = genres
        self.summary = summary

    def get_book_title(self):
        return self.book_title

    def get_genres(self):
        return self.genres

    def get_summary(self):
        return self.summary