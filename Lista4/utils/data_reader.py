from utils.book import Book
import json
from genres import valid_genres
import string

class DataReader():
    
    def __init__(self, filename) -> None:
        self.books = []
        self.genres_with_occurences = {}
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
        self.genres_with_occurences = dict(sorted(self.genres_with_occurences.items(), key=lambda item:-item[1]))
        
    def validate_book(self, line : str):
        words = line.split('\t')
        if len(words) != 7:
            return
        if words[5] != '' and words[6] != '':
            if len(words[6]) < 100:
                return
            genres = json.loads(words[5])
            if genres:
                values = list(genres.values())
                counter = 0
                chosen_genre = ""
                for valid_genre in valid_genres:
                    if valid_genre in values:
                        counter += 1
                        chosen_genre = valid_genre
                    if counter > 1:
                        return
                if chosen_genre != "":
                    b = Book(chosen_genre, self.replace_invalid_characters(words[6]))
                    self.books.append(b)
                    if chosen_genre in self.genres_with_occurences.keys():
                        self.genres_with_occurences[chosen_genre] = self.genres_with_occurences[chosen_genre] + 1
                    else:
                        self.genres_with_occurences[chosen_genre] = 1

    def replace_invalid_characters(self, description) -> string:
        new_description = description.translate(str.maketrans('', '', string.punctuation))
        return ""

    def get_books(self):
        return self.books
    
    def get_genres(self):
        return self.genres_with_occurences