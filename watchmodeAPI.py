import urllib.request
import json

# num = 1396
# with urllib.request.urlopen("https://api.watchmode.com/v1/title/tv-1396/sources/?apiKey=NAjFF0MM3qS5fl2xPjgpwq87cyVTgbsXfJX3KYLD") as url:
#     data = json.loads(url.read().decode())
#     print(data)

# this class could just be made into another function in another class, but this provides some order for now
class episodeNums():
    def getEpisode(id, type): 
        # type is going to either be movie or show
        #id can really be anything
        url = "https://api.watchmode.com/v1/title/tv-%s/sources/?apiKey=NAjFF0MM3qS5fl2xPjgpwq87cyVTgbsXfJX3KYLD" %id
        link = urllib.request.urlopen(url)
        data = json.loads(link.read().decode())
        #TODO:
        # 200	OK	The request was successful.
        # 400	Bad request	Bad request
        # 401	Unauthorized	Your API key is invalid.
        # 402	Over quota	Over plan quota on this API Key.
        # 404	Not found	The resource does not exist.
        # 429	Too Many Requests	The rate limit was exceeded.
        # 50X	Internal Server Error	An error occurred with our API.

        returnValue = ["service" , "type" , "episode", "season"]
        for service in data:
            serv = service['name']
            type = service['type']
            seasons = service['seasons']
            episodes = service['episodes']
            returnValue[0] = serv   
            returnValue[1] = type
            returnValue[2] = episodes
            returnValue[3] = seasons
        


