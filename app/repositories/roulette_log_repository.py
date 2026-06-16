from app.database.mongo import mongodb


def save_roulette_log(document):
    collection = mongodb["ROULETTE_LOG"]

    result = collection.insert_one(document)

    return str(result.inserted_id)