
from urllib.parse import urlparse
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV
from difflib import SequenceMatcher, get_close_matches
import requests
##will affect requirements: TODO   
import urllib.request
import json
from threading import Thread

def getPrice(name):
    name = name.lower()
    if(name == "netflix"):
        return "9.99"
    elif(name == "disney+"):
        return "7.99"
    elif(name == "hbo max"):
        return "9.99"
    elif(name == "hulu"):
        return "6.99"
    elif(name == "prime"):
        return "14.99"
    elif(name == "paramount"):
        return "4.99"
    elif(name == "hoopla"):
        return "3.99"
    elif(name == "showtime (via amazon prime"):
        return "14.99"
    elif(name == "showtime"):
        return "3.99"
    elif(name == "fubotv"):
        return "69.99"
    elif(name == "spectrum on demand"):
        return "44.99"
    else:
        print(name)
        return "-1"

class Y_TIT(): 
    def __init__(self, title = "", id = "", type = "", year = "", ratio = 0, posterPath = "" ) -> None:
        self.title = title
        self.id = id
        self.type = type
        self.year = year
        self.ratio = ratio
        self.posterPath = posterPath
    def __str__(self) -> str:
        # return "title: " + self.title + " id: " + self.id + " type: " +  self.type + " year: " + self.year + " Poster path: " + self.posterPath
        return self.title + "<*" + self.id + "<*" +  self.type + "<*" + self.year + "<*" + self.posterPath

#need to add unit
#more sorting
#limit to 6 return 
#provider, link to the steaming service, price, seasons, purchaseOptions, 
class rowAttrributes(): 
    def __init__(self, provider = "", link = "", price = "", seasons = "", purchaseOption = "", format = "", priceUnit = ""):
        self.provider = provider
        if(price is None):
            self.price = getPrice(provider.lower())
        else:
            self.price = price
        self.link = link
        self.seasons = seasons
        if(self.seasons is None):
            self.seasons = "Movie"
        #print(self.seasons)
        self.purchaseOption = purchaseOption[0].upper() + purchaseOption[1:]
        self.format = format
        self.priceUnit = priceUnit
    def __str__(self) -> str:
        return self.provider + "\t\t" + str(self.price) + "\t\t" + str(self.seasons) + "\t\t" + self.purchaseOption + "\t\t" + self.format
    def toDict(self):
        return {"provider":self.provider, "link":self.link , "price": self.price, "purchaseOption": self.purchaseOption, "format": self.format, "seasons": self.seasons, "priceUnit": self.priceUnit}
class allTogether():
    def __init__(self) -> None:
        self.tmdb = TMDb()
        self.tmdb.api_key = 'cc680ed9d9b43c2a5127f13faa251e40'
        self.url = "https://mdblist.p.rapidapi.com/"
        self.querystringTitle = {"s":"None"}
        self.querystringID = {"i":"none"}
        self.headers = {
            "X-RapidAPI-Host": "mdblist.p.rapidapi.com",
            "X-RapidAPI-Key": "d306efce59msh9ad6c720abe986dp14c4f4jsn9843c8fc295e"
        }


    def threadGetPosterPath(self, index):
        # index = indexList[0]
        # print(index)
        urlForPoster = "https://www.omdbapi.com/?i="
        urlForPoster = urlForPoster + self.finalValues[index].id + "&apikey=3b6efd31"
        link = urllib.request.urlopen(urlForPoster)
        data = json.loads(link.read().decode())
        link.close()
        poster = "https://www.csaff.org/wp-content/uploads/csaff-no-poster.jpg"
        try:
            poster = data['Poster']
            # print(data['Poster'])
        except:
            pass 
        if(poster == "N/A"):
            poster = "https://www.csaff.org/wp-content/uploads/csaff-no-poster.jpg"
        self.finalValues[index].posterPath = poster
        

    def getIMDB_WithTitle (self, title): #id that start with tt ----- 
        self.querystringTitle['s'] = title
        response = requests.request("Get", url= self.url, headers= self.headers, params=self.querystringTitle)
        jsonRep = response.json()
        search = ""
        try:
            search = jsonRep['search']
        except:
            return []
        self.finalValues = []
        #https://www.omdbapi.com/?i=tt0903747&apikey=3b6efd31"
        threads = []
        count = 0
        for option in search:
            if(count == 14):
                break

            rat = SequenceMatcher(None, option['title'], title).ratio()
            # print(option) 
            if(rat > .4):
                
                titObject = Y_TIT(option['title'], str(option['id']),option['type'],str(option['year']), rat)
                self.finalValues.append(titObject)
                thd = Thread(target=self.threadGetPosterPath, args=[count])
                thd.start()
                count += 1
                threads.append(thd)

            
        # finalValues.sort(key=lambda x: x.ratio, reverse=True)
        # threads = [Thread(target=self.threadGetPosterPath , args=(count)) for count in range(len(self.finalValues[:14]))]

        for thread in threads:
            thread.join()

        # for i in finalValues[:14]:

            

            # urlForPoster = urlForPoster + i.id + "&apikey=3b6efd31"
            # link = urllib.request.urlopen(urlForPoster)
            # data = json.loads(link.read().decode())
            # link.close()
            # poster = "https://www.csaff.org/wp-content/uploads/csaff-no-poster.jpg"
            # try:
            #     poster = data['Poster']
            #     # print(data['Poster'])
            # except:
            #     pass 
            # i.posterPath = poster
            # urlForPoster = "https://www.omdbapi.com/?i="
            # print(i)

        return self.finalValues


    def getTMDBID(self, otherID):
        self.querystringID['i'] = otherID
        response = requests.request("Get", url = self.url, headers=self.headers, params = self.querystringID)
        jsonRes = response.json()
        # print(jsonRes)
        # print(otherID)
        ret = "" 
        try: 
            ret = jsonRes["tmdbid"]
        except: 
            pass
        return ret
        

    def getResults(self, type, id, toDict = False):
        if(type == "show"):
            type = "tv"
        else:
            type = "movie"
        watchModeURL = "https://api.watchmode.com/v1/title/" + type + "-" + str(id) +"/sources/?apiKey=sq1G9gKN5rJbjtxuxRHkK4V3jLXOaqUzqCZMjYI1"
        # watchModeURL = "https://api.watchmode.com/v1/title/%s-%s/sources/?apiKey=NAjFF0MM3qS5fl2xPjgpwq87cyVTgbsXfJX3KYLD" 
        # print(watchModeURL)
        link = urllib.request.urlopen(watchModeURL)
        
        data = json.loads(link.read().decode())
        # print(data)
        # print()
        # link.close()
        listOfRowAtt = []
        for service in data:
            # print(service)
            purUnit = ""
            if((service['type'] == "buy" or service['type'] == "rent") ):
                if(type == "tv"):
                    purUnit = "/episode"    
                else:
                    purUnit = "" 
            elif(service['type'] == "sub"):
                purUnit = "/month"
                
            row = rowAttrributes(service['name'], service['web_url'], str(service['price']), service['seasons'], service['type'], service['format'], purUnit)
            if(row.purchaseOption == "Sub" or row.purchaseOption == "tve"):
                row.price = getPrice(service['name'])
                # print(service['name'])
            # print(row)
            
            if(toDict):
                row = row.toDict()
            listOfRowAtt.append(row)

        return listOfRowAtt

    



    #check: if they own the service provider then the cost would be owned(yes/no)
    #return array of platform, type(buy, rent, sub), 
    #buy: provider, price, seasons, episodes, links
    #rent: provider, price, seasons, episodes, links
    #sub: provider,  price(other function), seasons, episodes, links
    # def getResultsShow(self, title):
    #     pass

    #check: NONE FOR NOW  JUST 
    #return: RETURNS THE LIST
    def showRec(self, id):
        show = TV()
        rec = show.recommendations(tv_id=id)
        ret = []
        
        for i in rec: 
            appen = Y_TIT(i.name, str(i.id), "show", i.first_air_date, 0,  "https://image.tmdb.org/t/p/original"+i.poster_path)
            ret.append(appen)
        return ret

    def movieRec(self, id): 
        movie = Movie()
        rec = movie.recommendations(movie_id=id)
        ret = []
        
        for i in rec: 
            appen = Y_TIT(i.title, str(i.id), "movie", i.release_date, 0,  "https://image.tmdb.org/t/p/original"+i.poster_path)
            ret.append(appen)

        # for i in ret:
        #     print(i)
        

        return ret
    ##########################################

if __name__ == "__main__":
    testAllTogether = allTogether()
    # ret = testAllTogether.movieRec(578)
    # for i in ret:
    #     print(i)
    # ret = testAllTogether.showRec(1396)
    # for j in ret: 
    #     print(j)

    # for i in print(testAllTogether.showRec(1396)):
    #     print(str(i))
    # for j in print(testAllTogether.movieRec(578)):
    #     print(j)
    # a = testAllTogether.getIMDB_WithTitle("50 greatest harry potter moments")
    # print(testAllTogether.getTMDBID("tt2006673"))
    # print(testAllTogether.getTMDBID())
    # print(testAllTogether.getResults("movie", 483898, True))
    #print(a)
    # for value in a:
    # testAllTogether.getResults("show", "1396")