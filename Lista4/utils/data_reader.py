from utils.book import Book


class DataReader():
    
    def __init__(self, filename) -> None:
        self.books = []
        self.filename = filename
        self.read_data(filename)

    def read_data(self, filename):
        with open(filename, encoding="utf-8") as file:
            line = file.readline()
            self.validate_book(line)
            while line:
                line = file.readline()
                self.validate_book(line)
            file.close()
        

    def validate_book(self, line : str):
        words = line.split('\t')
        if len(words) != 7:
            return False
        if words[2] != '' and words[5] != '' and words[6] != '':
            b = Book(words[2], words[5], words[6])
            self.books.append(b)

    def get_books(self):
        return self.books