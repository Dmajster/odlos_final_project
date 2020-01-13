from UserItemData import UserItemData
from statistics import mean
from math import sqrt

import pandas

class ItemBasedPredictor:
    def __init__(self, min_values: int = 0, threshold: float = 0):
        self.min_values = min_values
        self.threshold = threshold

    def fit(self, x: UserItemData):
        self.data = x.data

        movie_ids = self.data['movieID'].unique()

        self.movie_data_groups = self.data.groupby(['movieID'])
        self.user_data_groups = self.data.groupby(['userID'])
        self.user_rating_averages = self.data.groupby(['userID'])['rating'].mean()

        self.similarities = pandas.DataFrame({ 
            movie_id_1: {
                movie_id_2: self.similarity(movie_id_1, movie_id_2)
                for movie_id_2 in movie_ids }
            for movie_id_1 in movie_ids 
        })

    def predict(self, user_id: int, n: int = 10):
        if user_id not in self.user_data_groups.groups.keys():
            return

        rating_group = self.user_data_groups.get_group(user_id).set_index('movieID')

        movie_ids = self.data['movieID'].unique()

        output = {}

        for movie_id in movie_ids:
            similarities = self.similarities[self.similarities[movie_id] > 0][movie_id].to_frame()
            similarities = similarities.join(rating_group, how='inner')

            if len(similarities) > 0:
                output[movie_id] = sum(similarities[movie_id] * similarities['rating']) / sum(abs(similarities[movie_id]))

        return output

    def similarity(self, movie_id_1: int, movie_id_2: int):
        if movie_id_1 == movie_id_2:
            return 0

        movie_1_group = self.movie_data_groups.get_group(movie_id_1).set_index('userID')
        movie_2_group = self.movie_data_groups.get_group(movie_id_2).set_index('userID')
        movie_both_group = movie_1_group.join(movie_2_group, lsuffix='_1', rsuffix='_2', on='userID', how='inner')

        print(movie_both_group)

        if len(movie_both_group) < self.min_values:
            return 0

        movie_both_group = movie_both_group.join(self.user_rating_averages, how='inner')
        sum_top = sum((movie_both_group['rating_1'] - movie_both_group['rating']) * (movie_both_group['rating_2'] - movie_both_group['rating']))
        sum_bottom_left = sum(pow(movie_both_group['rating_1'] - movie_both_group['rating'], 2))
        sum_bottom_right = sum(pow(movie_both_group['rating_2'] - movie_both_group['rating'], 2))
        simmilarity = sum_top / (sqrt(sum_bottom_left) * sqrt(sum_bottom_right))

        if simmilarity < self.threshold:
            return 0

        return simmilarity

    def similarItems(self, movie_id: int, n):
        simmilar_movies = self.similarities[movie_id].sort_values(ascending=False)[:n]

        return { key: value for key, value in simmilar_movies.items() }