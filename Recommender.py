from UserItemData import UserItemData
import pandas
from math import sqrt

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
        test_rating_user_groups = test_data.data.groupby('userID')

        predictor_rating_user_groups = self.predictor.data.groupby('userID')

        rmse = 0
        mae = 0
        precision = 0
        recall = 0
        f = 0

        rmse_count = 0
        mae_count = 0
        precision_count = 0
        recall_count = 0

        for name, group in test_rating_user_groups:
            user_id = group['userID'].iloc[0]

            if user_id not in self.predictor.data['userID']:
                continue

            if user_id not in predictor_rating_user_groups.groups.keys():
                continue

            user_predictions = self.recommend(user_id, n=n)

            predicted_data_ratings = pandas.DataFrame(user_predictions, columns=['movieID','rating']).set_index('movieID')
            actual_data_ratings = group.set_index('movieID').drop(columns=['userID'])
            joined_data_ratings = predicted_data_ratings.join(actual_data_ratings, lsuffix='_predicted', rsuffix='_actual', how='inner')
            joined_data_ratings['rating_average'] = actual_data_ratings['rating'].mean()

            if len(joined_data_ratings) == 0:
                continue

            rmse += sqrt(sum(((joined_data_ratings['rating_predicted'] - joined_data_ratings['rating_actual']) ** 2) / len(joined_data_ratings)))
            rmse_count += 1

            mae += sum( abs(joined_data_ratings['rating_predicted'] - joined_data_ratings['rating_actual']) ) / len(joined_data_ratings)
            mae_count += 1

            true_positives = joined_data_ratings[
                (joined_data_ratings['rating_predicted'] > joined_data_ratings['rating_average']) & 
                (joined_data_ratings['rating_actual'] > joined_data_ratings['rating_average'])
            ]

            false_positives = joined_data_ratings[
                (joined_data_ratings['rating_predicted'] > joined_data_ratings['rating_average']) & 
                (joined_data_ratings['rating_actual'] <= joined_data_ratings['rating_average'])
            ]

            false_negatives = joined_data_ratings[
                (joined_data_ratings['rating_predicted'] <= joined_data_ratings['rating_average']) & 
                (joined_data_ratings['rating_actual'] > joined_data_ratings['rating_average'])
            ]

            if (len(true_positives) + len(false_positives)) > 0:
                precision += len(true_positives) / (len(true_positives) + len(false_positives))
                precision_count += 1

            if (len(true_positives) + len(false_negatives)) > 0:
                recall += len(true_positives) / (len(true_positives) + len(false_negatives))
                recall_count += 1
           

        rmse /= rmse_count
        mae /= mae_count
        precision /= precision_count
        recall /= recall_count
        f = 2 * ((recall * precision) / (precision + recall))

        return (rmse, mae, precision, recall, f)