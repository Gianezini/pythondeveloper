import datetime
import pprint
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@pythondeveloper.z99dipy.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Você está conectado ao MongoDB")
except Exception as e:
    print(e)

db = client.test


mauricio = {
    "id":1,
    "nome":"Mauricio",
    "cpf":"12345678910",
    "endereco":["Oiapoc,1257"],
    "agencia":1241246,
    "tipo":"Conta Corrente",
    "saldo":1500,
}
cliente = db.cliente
cliente_id = cliente.insert_many(mauricio)
print(cliente_id)

print(db.list_collection_names())

print(db.client.find_one())
pprint.pprint(db.cliente.find_one())

print("Recuperar informação:")
pprint.pprint(db.cliente.find_one({"nome":"Mauricio"}))

for post in cliente.find():
    print("------------------")
    pprint.pprint(post)

print(cliente.count_documents({}))

print(cliente.count_documents({"cliente":"Mauricio"}))

for clientes in cliente.find({}).sort("date"):
    pprint.pprint(mauricio)

result = db.profiles.create_index([('nome', pymongo.ASCENDING)], unique=True)

# print(sorted(list(db.profiles.index_information())))

user_profile_user = [
    {"user_id":100, "nome": "Jose"},
    {"user_id":200, "nome": "Maria"}
]

result = db.profile_user.insert_many(user_profile_user)
print("resultado")
pprint.pprint(result)