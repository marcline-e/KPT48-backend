from app.database.mongo import mongodb

try:
    print(mongodb.list_collection_names())
    print("MongoDB Connected!")

except Exception as e:
    print("Connection Failed")
    print(e)