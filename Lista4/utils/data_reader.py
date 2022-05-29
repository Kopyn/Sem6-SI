class DataReader():
    
    def __init__(self, filename) -> None:
        self.books = []
        self.filename = filename
        self.read_data(filename)

    def read_data(self, filename):
        with open(filename, encoding="utf-8") as file:
            i = 1
            line = file.readline()
            print(line)
            print(i)
            while line:
                i += 1
                line = file.readline()
                print(line)
                print(i)
            file.close()

    def validate_book(self):
        pass