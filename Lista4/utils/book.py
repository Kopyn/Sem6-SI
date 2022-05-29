class Book():
    def __init__(self, wikipedia_id = "", freebase_id = "", book_title = "", author = "", publication_date = "", genres = "", summary = ""):
        self.wikipedia_id = wikipedia_id
        self.freebase_id = freebase_id
        self.book_title = book_title
        self.author = author
        self.publication_date = publication_date
        self.genres = genres
        self.summary = summary

    def get_wikipedia_id(self):
        return self.wikipedia_id

    def get_freebase_id(self):
        return self.freebase_id

    def get_book_title(self):
        return self.book_title

    def get_author(self):
        return self.author

    def get_publication_date(self):
        return self.publication_date

    def get_genres(self):
        return self.genres

    def get_summary(self):
        return self.summary