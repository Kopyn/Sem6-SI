class Book():
    def __init__(self, genre = "", summary = ""):
        self.genre = genre
        self.summary = summary

    def get_genres(self):
        return self.genre

    def get_summary(self):
        return self.summary

    def set_genres(self, genre):
        self.genre = genre

    def set_summary(self, summary):
        self.summary = summary