from UserItemData import UserItemData


class Recommender:
    def __init__(self, predictor):
        self.predictor = predictor

    def fit(self, x: UserItemData):
        self.predictor.fit(x)

    def recommend(self, user_id: int, n: int = 10, rec_seen: bool = True):
        predictions = self.predictor.predict(user_id)

        # sort prediction dict by value from highest to lowest. 
        prediction_list = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

        # if already seen is allowed
        if rec_seen:
            return prediction_list[:n]

        # get all movie id's of movies the user has already seen
        already_seen_list = self.predictor.data.loc[(self.predictor.data['userID'] == user_id)]['movieID']

        # iterate over the best predictions until we fill N slots
        recommended_list = []
        checked_prediction_index = 0
        while len(recommended_list) < n:
            movie_rating_pair = prediction_list[checked_prediction_index]
            movie_id = movie_rating_pair[0]
            if movie_id not in already_seen_list.values:
                recommended_list.append(movie_rating_pair)
            checked_prediction_index += 1

        return recommended_list

    def evaluate(self, test_data: UserItemData, n: int):
        rating_user_groups = test_data.data.groupby('userID')

        print(rating_user_groups.groups.keys())

        rmse = 0
        mae = 0
        precision = 0
        recall = 0
        f = 0

        return (rmse, mae, precision, recall, f)