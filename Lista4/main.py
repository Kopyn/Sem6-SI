from utils.data_reader import DataReader


if __name__ == "__main__":
    dr = DataReader('booksummaries//booksummaries.txt')
    print(len(dr.get_books()))