from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)


MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "MOVIE"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

@app.route('/api/movies', methods=['GET'])
def get_movies():
    
    pipeline = [
        {"$match": {"year": {"$gte": 2000}, "imdb.rating": {"$gte": 6.0}}},
        {"$project": {"_id": 1, "plot": 1, "cast": 1, "directors": 1, "awards": 1, "imdb": 1}}
    ]


    result = db.movies.aggregate(pipeline)

    
    data = list(result)

    
    df = pd.DataFrame(data)

    
    df['wins'] = df['awards'].apply(lambda x: x.get('wins', None))
    df['nominations'] = df['awards'].apply(lambda x: x.get('nominations', None))
    df['imdb rating'] = df['imdb'].apply(lambda x: x.get('rating', None))
    df['cast'] = df['cast'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    df['directors'] = df['directors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    
    df.drop(['awards', 'imdb'], axis=1, inplace=True)

    
    output_file = "filename.xlsx"


    df.to_excel(output_file, index=False)

    
    return jsonify({"message": "Data exported to Excel successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
