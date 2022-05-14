
import csv
from time import sleep
# from urllib import response
import requests

class fillShowData:

    def __init__(self):
        url = "https://streaming-availability.p.rapidapi.com/search/basic"

        startingPage = 1#this will be base off our very last page we used 
        querystring = {"country":"us","service":"netflix","type":"series","page":"1"}
        querystring["page"] = startingPage

        apikeys = ["9ceae2bfe3mshb8ae497f1a3663cp17b583jsnd5da4be710ad", "c28c60212emsh9de81c260cb65e9p158187jsn465d9e3b3e78", 
            "d306efce59msh9ad6c720abe986dp14c4f4jsn9843c8fc295e", "a97b88ac19msheef4c8aaafe509cp18c67ejsnf9ff1d1c51ec",
            "55917d4604msh82c8d1a32cd463ap123f91jsn847c54c8d2f1", "aa62057726msh0eba8f4bda28a71p15a060jsnd12bd1ae735a"]

        headers = {
            "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com",
            "X-RapidAPI-Key": apikeys[2]
        }
        nextAPIkey = 3

        streamingServices = ["Netflix" , "Prime" , "Disney", "HBO" , "Hulu"] 
        countries = ["us"]

    #first iteration of getting the total Pages and results and results
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_responce = response.json()

        pagesToUpdate = json_responce['total_pages'] - startingPage
        results = json_responce['results']

        #we need title, tmdbID, link for movies, service provider, country
        with open('showInformation.csv', 'r+', newline='',encoding= 'utf-8' ) as fileWithMovieInfo:
            print(pagesToUpdate)
            reader = csv.reader(fileWithMovieInfo)
            for movie in reader:
                pass

            movieWriter = csv.writer(fileWithMovieInfo )
            count = 1
            data = ["tmdbID", "title", "link", "Netflix", "US"]
            while pagesToUpdate > 1:
                print(startingPage)

                for movie in results:
                    title = movie['title']
                    tmdbID = movie['tmdbID']
                    streamingInfo = movie['streamingInfo']
                    link = streamingInfo["netflix"]["us"]["link"]

                    data[0] = tmdbID 
                    data[1] = title
                    data[2] = link
                    movieWriter.writerow(data)

                querystring["page"] = startingPage + 1
                count += 1
                #we can only do 10 searches in a second
                sleep(.1)
                if (count % 98 == 0):
                    headers["X-RapidAPI-Key"]=apikeys[nextAPIkey]
                    nextAPIkey+= 1

                response = requests.request("GET", url, headers=headers, params=querystring)
                json_responce = response.json()
                startingPage += 1
                pagesToUpdate = pagesToUpdate - 1
                results = json_responce['results']



fillShowData()



