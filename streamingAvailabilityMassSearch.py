import requests
from difflib import SequenceMatcher
from flask import Flask, render_template, url_for, request, redirect
from enum import Enum


def getPrice(name):
    name = name.lower()
    if(name == "netflix"):
        return "    9.99"
    elif(name == "disney"):
        return "    7.99"
    elif(name == "hbo"):
        return "    9.99"
    elif(name == "hulu"):
        return "    6.99"
    elif(name == "prime"):
        return "    14.99"
    elif(name == "paramount"):
        return "    4.99"
    else:
        return "    No Price Available"




class streamingAvailability():
    def __init__(self):
        self.apikeys = ["9ceae2bfe3mshb8ae497f1a3663cp17b583jsnd5da4be710ad", "c28c60212emsh9de81c260cb65e9p158187jsn465d9e3b3e78", 
            "d306efce59msh9ad6c720abe986dp14c4f4jsn9843c8fc295e", "a97b88ac19msheef4c8aaafe509cp18c67ejsnf9ff1d1c51ec",
            "55917d4604msh82c8d1a32cd463ap123f91jsn847c54c8d2f1", "aa62057726msh0eba8f4bda28a71p15a060jsnd12bd1ae735a"]
        self.services = ["netflix", "prime", "hulu", "disney"]
        #   "HBO", "Peacock", "Paramount", "Starz", "Showtime", "Apple", "Mubi", "Stan", "Now"]
        self.url = "https://streaming-availability.p.rapidapi.com/search/basic"
        self.querystring = {"country":"us","service":"netflix","type":"movie","page":"1","keyword":"apples"}
        self.headers = {
            "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com",
            "X-RapidAPI-Key": "05a27f45damsh539de5c651b940ap143eacjsnbb337fb5002a"
        }

    def getResults(self, title):
        title2 = title.lower()
        self.querystring["keyword"] = title
        data = [ ]
        for service in self.services:
            self.querystring["service"] = service.lower()
            response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
            js_response = response.json()
            results = js_response['results']
            for result in results:
                testTitle = result["title"].lower()
                if(SequenceMatcher(None, title2, testTitle).ratio() >= .70):
<<<<<<< HEAD
                    data.append(service)
        xstr = ""
        xstr += '<ul>'
        for e in data:
            xstr+= '<li>' + e + '\t' + getPrice(e) + '</li>'
        xstr += '</ul>'
=======
                    data2 = ["title" , "link" , "price", "service"]
                    data2[0] = testTitle
                    streamingInfo = result['streamingInfo']
                    data2[1] = streamingInfo[service]['us']['link']
                    data2[2] = getPrice(service)
                    data2[3] = service
                    data.append(data2)
                    data2.clear
        ret = ""
        for i in data[0]:
            ret += i + " "
        print(data)
        return ret
>>>>>>> 832745ce659441fc072082b260f5ef750fe55c70

a = streamingAvailability().getResults("cars")
print(a)

                    




    

