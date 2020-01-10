from UserItemData import UserItemData 
from MovieData import MovieData

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1300)

from ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender

from ZeepohPredictor import ZeepohPredictor

rp = ZeepohPredictor()
rec = Recommender(rp)
rec.fit(uim)

'''
print()

columns = rp.similarities.columns

column = columns[0]

print(rp.similarities[column])

'''

print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)

for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))


