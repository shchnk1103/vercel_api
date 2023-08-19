import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = 'mongodb+srv://doubleshy0n:xpRyw23yv6D9o8vy@cluster0.capiy3n.mongodb.net/?retryWrites=true&w=majority'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
