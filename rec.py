from tmdbv3api import TMDb
from tmdbv3api import Movie
import tmdbv3api as t 
class reccomendation():
    def __init__(self):
        self.tmdb = TMDb()
        self.tmdb.api_key = "cc680ed9d9b43c2a5127f13faa251e40"
        self.movie = Movie()
        
    def getReccomendationFromMovie(self, id):
        reccomendations = self.movie.recommendations(movie_id=id)
        return reccomendation
        # for reccomendation in reccomendations:
        #     print(reccomendation.title)
        
    def onlyTitleReccomendations(self, id):
        listOfTitles = []
        for reccomendation in self.getReccomendationFromMovie(id):
            listOfTitles.append(reccomendation.title())

# reccomendation().getReccomendationFromMovie(111)
tmdb = TMDb()
tmdb.api_key = "cc680ed9d9b43c2a5127f13faa251e40"


movie = Movie()
a = movie.search("avengers")
for i in a:
    print(i['id'])