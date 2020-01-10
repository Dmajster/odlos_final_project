from UserItemData import UserItemData
from statistics import mean

class AveragePredictor:
    def __init__(self, b: int):
        self.b = b

    def fit(self, x: UserItemData):
        self.data = x.data

        rating_sums = x.data.groupby(['movieID'])['rating'].sum()
        rating_counts = x.data.groupby(['movieID'])['rating'].count()
        g_avg = mean(x.data['rating'])

        movie_ids = x.data['movieID']
        rating_averages = [(rating_sums[movie_id] + self.b * g_avg) / (rating_counts[movie_id] + self.b) for movie_id in movie_ids]

        self.data['average'] = rating_averages

    def predict(self, user_id: int):
        return dict(zip(self.data['movieID'], self.data['average']))
