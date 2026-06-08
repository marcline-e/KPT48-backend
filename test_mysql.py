from app.database.mongo import mongodb

try:
    print(mongodb.list_collection_names())

    print("MongoDB Connected!")

    # Menutup koneksi
    connection.close()

except Exception as e:
    print("Connection Failed")
    print(e)