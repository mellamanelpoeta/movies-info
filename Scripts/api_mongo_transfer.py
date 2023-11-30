import requests
from pymongo import MongoClient

#API configuration
bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNDRhZDQ3NTAyNTNiMGIxM2FmMjJjNjIwNmE2MmNmMyIsInN1YiI6IjY1NjZhY2M1ZDk1NDIwMDExYjk1MmE1NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.N2gnv8B7AlaOmB_o4FXvv3T2saPCZU5dDFhs8i8IJJg"
base_url = "https://api.themoviedb.org/3"

#MongoDB configuration
client = MongoClient("mongodb://mongo:27017/")

'''LOCAL client = MongoClient("mongodb://localhost:27017/")'''
#Database name: Movies
#Collections: Movies, Credits
db = client["moviesdb"]

movies_collection = db["movies"]
credits_collection = db["credits"]

#Insert json data to MongoDB
def insert_Mongo(collection, data):
    collection.insert_one(data)

#Get the movies id of the given year
def moviesId_per_year(year):
    url = f"{base_url}/discover/movie"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    list_id = []

    #It gets the information of the top 20 movies of the year
    for i in range(1,2):        
        params ={
        "primary_release_year": f"{year}",
        "page": f"{i}",
        "sort_by": "popularity.desc"
        }
        response = requests.get(url,headers=headers, params=params)
        results = response.json()["results"]
        
        for movie in results:
            list_id.append(movie['id'])
        
    return list_id

def movie_details(list_id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }
   
    total = len(list_id)
    i = 0
    print("Inserting Movies to mongoDB")
    for id in list_id:
        url = f"{base_url}/movie/{id}?language=en-US"
        response = requests.get(url, headers=headers)
        results = response.json()
        if results:
            insert_Mongo(movies_collection, results)
        i += 1
        print(str(round(i/total*100,2))+"%")
    print("100%")
    print("Done")



def movie_credits(list_id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    total = len(list_id)
    i = 0
    print("Inserting Credits to mongoDB")
    for id in list_id:
        url = f"{base_url}/movie/{id}/credits?language=en-US"
        response = requests.get(url, headers=headers)
        results = response.json()
        if results:
            insert_Mongo(credits_collection, results)
        i += 1
        print(str(round(i/total*100,2))+"%")
    print("100%")
    print("Done")

ids = []
k = 0
print("Getting movies id per year")
for year in range(1990,2024):
    print(str(round(k/34*100,2))+"%")
    ids += moviesId_per_year(year)
    k += 1
print("100%")
print("Done")

#Insert movies details to MongoDB in collection "movies", and credits in collection "credits"
movie_details(ids)
movie_credits(ids)

db.movies.updateMany({}, [{ "$set": { "release_date": { "$toDate": "$release_date" } } }])

client.close()
