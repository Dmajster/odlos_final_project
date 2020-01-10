import pandas

class UserItemData:
    def __init__(self, path: str, from_date: str = None, to_date: str = None, min_ratings: int = None):
        self.path = path
        self.from_date = from_date
        self.to_date = to_date
        self.min_ratings = min_ratings

        self.data = pandas.read_csv(path, sep='\t')

        data_dates = pandas.to_datetime(dict(year=self.data.date_year, month=self.data.date_month, day=self.data.date_day, hour=self.data.date_hour,
                                             minute=self.data.date_minute, second=self.data.date_second)).values

        self.data = self.data.drop(columns=['date_second', 'date_minute', 'date_hour', 'date_day', 'date_month', 'date_year'])
        self.data.insert(3, 'date', data_dates)

        if from_date != None and to_date != None:
            from_date = pandas.to_datetime(from_date, format='%d.%m.%Y')
            to_date = pandas.to_datetime(to_date, format='%d.%m.%Y')
            self.data = self.data.loc[(self.data['date'] > from_date) & (self.data['date'] < to_date)]

        if min_ratings != None:
            movie_rating_count = self.data['movieID'].value_counts().to_dict()
            valid_movie_id_list = [movie_id for movie_id, rating_count in movie_rating_count.items() if rating_count > min_ratings]
            self.data = self.data[self.data['movieID'].isin(valid_movie_id_list)]

    def nratings(self):
        return len(self.data)
