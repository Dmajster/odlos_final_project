from UserItemData import UserItemData 
from MovieData import MovieData
from RandomPredictor import RandomPredictor
from AveragePredictor import AveragePredictor
from ViewsPredictor import ViewsPredictor
from ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender

md = MovieData('data/movies.dat')
uim = UserItemData('data/user_ratedmovies.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)

#print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", rp.similarity(1580, 2716))
#print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", rp.similarity(1580, 527))
#print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", rp.similarity(1580, 780))