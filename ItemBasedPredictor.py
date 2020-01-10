from UserItemData import UserItemData
from statistics import mean
from math import sqrt
import pandas
from timeit import default_timer as timer

class ItemBasedPredictor:
    def __init__(self, min_values: int = 0, threshold: float = 0):
        self.min_values = min_values
        self.threshold = threshold
    
    def fit(self, x: UserItemData):
        self.data = x.data
        
        movie_ids = self.data['movieID'].unique()

        print(movie_ids)

        self.data.set_index('userID', inplace=True)
        self.movie_data_groups = self.data.groupby(['movieID'])
        self.user_data_groups = self.data.groupby(['userID'])

        for movie_id_1 in movie_ids:
            for movie_id_2 in movie_ids:
                if movie_id_1 == movie_id_2:
                    continue
                
                print("ids: \t\t", movie_id_1, movie_id_2)

                start = timer()
                simmilarity = self.similarity(movie_id_1, movie_id_2)
                end = timer()

                print("simmilarity \t", simmilarity)

                print("time: \t\t", end - start, "\n")


    def recommend(self, user_id: int, n: int = 10, rec_seen: bool = True):
        return

    def similarity(self, movie_id_1: int, movie_id_2: int):
        movie_1_group = self.movie_data_groups.get_group(movie_id_1)
        movie_2_group = self.movie_data_groups.get_group(movie_id_2)
        movie_both_group = movie_1_group.join(movie_2_group, lsuffix='_1', rsuffix='_2', on='userID', how='inner')        

        if  len(movie_both_group) < self.min_values:
            return 0

        sum_top = 0
        sum_bottom_left = 0
        sum_bottom_right = 0

        for user_id, user_rating_data in movie_both_group.iterrows():
            user_average_rating = mean(self.user_data_groups.get_group(user_id)['rating'])
            user_rating_movie_1 = user_rating_data['rating_1']
            user_rating_movie_2 = user_rating_data['rating_2']

            sum_top += (user_rating_movie_1 - user_average_rating) * (user_rating_movie_2 - user_average_rating)
            sum_bottom_left += pow(user_rating_movie_1 - user_average_rating, 2)
            sum_bottom_right += pow(user_rating_movie_2 - user_average_rating, 2)

        simmilarity = sum_top / ( sqrt(sum_bottom_left) * sqrt(sum_bottom_right) )

        if simmilarity < self.threshold:
            return 0

        return simmilarity
            