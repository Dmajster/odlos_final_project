'''
from ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender

rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)

rec_items = rp.similarItems(4993, 10)
print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')

for key, value in rec_items.items():
    print("Film: {}, ocena: {}".format(md.get_title(key), value))
'''
'''
from UserItemData import UserItemData 
from MovieData import MovieData

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1000)

from SlopeOnePredictor import SlopeOnePredictor
from Recommender import Recommender

rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))
'''

'''
top_similar = rp.similarities.stack().nlargest(20)
top_similar_keys = top_similar.index.tolist()
top_similar_value = top_similar.tolist()

for keys, value in zip(top_similar_keys, top_similar_value):
    print("Film1: {}, Film2: {}, Similarity: {}".format(md.get_title(keys[0]), md.get_title(keys[1]), value))
'''

'''
print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)

for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))
'''

from UserItemData import UserItemData 
from MovieData import MovieData

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1000)

from SlopeOnePredictor import SlopeOnePredictor
from Recommender import Recommender

rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))