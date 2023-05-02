import pymongo


client = pymongo.MongoClient("mongodb://havca1970:wIR3UCuOiYtAo9PL@ac-lywmls3-shard-00-00.z3iauxr.mongodb.net:27017,ac-lywmls3-shard-00-01.z3iauxr.mongodb.net:27017,ac-lywmls3-shard-00-02.z3iauxr.mongodb.net:27017/?ssl=true&replicaSet=atlas-d6ldgw-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test
print(db)