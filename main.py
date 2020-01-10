from UserItemData import UserItemData 
from MovieData import MovieData

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1300)

from ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender

rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)

print("Predictions for 78: ")
print(rec.predictor.predict(78))

rec_items = rec.recommend(78, n=15, rec_seen=False)

for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))