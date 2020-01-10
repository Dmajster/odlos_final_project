from UserItemData import UserItemData
from statistics import mean
from math import sqrt

class ItemBasedPredictor:
    def __init__(self, min_values: int = 0, threshold: float = 0):
        self.min_values = min_values
        self.threshold = threshold
    
    def fit(self, x: UserItemData):
        self.data = x.data

        movies_rated_by_group = self.data.groupby(['movieID'])
        users_rated_movie_1 = movies_rated_by_group.get_group(1580).set_index('userID')
        users_rated_movie_2 = movies_rated_by_group.get_group(2716).set_index('userID')
        users_rated_both = users_rated_movie_1.join(users_rated_movie_2, lsuffix='_1', rsuffix='_2', on='userID', how='inner')
        print(users_rated_both)


    def recommend(self, user_id: int, n: int = 10, rec_seen: bool = True):
        return

    def similarity(self, movie_id_1: int, movie_id_2: int):
        users_rated_movie_1 = self.data['userID'].loc[self.data['movieID'] == movie_id_1].unique()
        users_rated_movie_2 = self.data['userID'].loc[self.data['movieID'] == movie_id_2].unique()

        users_rated_both = self.data['userID'].loc[
            self.data['userID'].isin(users_rated_movie_1) &
            self.data['userID'].isin(users_rated_movie_2)
        ].unique()

        sum_top = 0
        sum_bottom_left = 0
        sum_bottom_right = 0

        for user_id in users_rated_both:
            user_ratings = self.data.loc[self.data['userID'] == user_id]
            user_average_rating = mean(user_ratings['rating'])
            user_rating_movie_1 = user_ratings.loc[self.data['movieID'] == movie_id_1, ['rating']].values[0][0]
            user_rating_movie_2 = user_ratings.loc[self.data['movieID'] == movie_id_2, ['rating']].values[0][0]

            sum_top += (user_rating_movie_1 - user_average_rating) * (user_rating_movie_2 - user_average_rating)
            sum_bottom_left += pow(user_rating_movie_1 - user_average_rating, 2)
            sum_bottom_right += pow(user_rating_movie_2 - user_average_rating, 2)

        return sum_top / ( sqrt(sum_bottom_left) * sqrt(sum_bottom_right) )
            