from UserItemData import UserItemData
from random import randint

class RandomPredictor:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def fit(self, x: UserItemData):
        self.data = x.data

    def predict(self, user_id: int):
        unique_movie_ids = self.data['movieID'].unique()

        return {movie_id: randint(self.min, self.max) for movie_id in unique_movie_ids}
