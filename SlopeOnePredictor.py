from UserItemData import UserItemData


class SlopeOnePredictor:
    def __init__(self):
        return

    def fit(self, x: UserItemData):
        self.data = x.data
        self.movie_data_groups = self.data.groupby(['movieID'])
        self.movie_user_groups = self.data.groupby(['userID'])

    def predict_one(self, user_id: int, movie_id: int):
        ru = self.movie_user_groups.get_group(user_id)
        ru = ru.drop(ru[ru['movieID'] == movie_id].index)
        dev = ru.apply(lambda row: self.dev(movie_id, row['movieID']), axis=1)

        return sum(dev + ru['rating']) / (len(ru)+1)

    def predict(self, user_id: int, n: int = 10, rec_seen: bool = True):
        output = {}

        movie_ids = self.data['movieID'].unique()

        for movie_id in movie_ids:
            output[movie_id] = self.predict_one(user_id, movie_id)

        return output

    def dev(self, item_i_id: int, item_j_id: int):
        movie_1_group = self.movie_data_groups.get_group(item_i_id).set_index('userID')
        movie_2_group = self.movie_data_groups.get_group(item_j_id).set_index('userID')
        movie_both_group = movie_1_group.join(movie_2_group, lsuffix='_1', rsuffix='_2', on='userID', how='inner')

        return sum(movie_both_group["rating_1"] - movie_both_group["rating_2"]) / len(movie_both_group)
