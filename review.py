class Review:
    def __init__(self):
        self.__review = None

    def init(self, review):
        self.__review = review

    def set_review(self, review):
        self.__review = review

    def get_review(self):
        return self.__review

