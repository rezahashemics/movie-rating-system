import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.directors import Director
from app.models.genres import Genre
from app.models.movies import Movie
from app.models.movie_genres import movie_genres
from app.models.movie_ratings import MovieRating  # For future, but not seeded

def seed_data():
    db: Session = SessionLocal()

    # Load movies
    movies_df = pd.read_csv('scripts/tmdb_5000_movies.csv')
    credits_df = pd.read_csv('scripts/tmdb_5000_credits.csv')

    # Merge on movie_id/title
    df = movies_df.merge(credits_df, left_on='title', right_on='title', how='inner')

    # Directors (unique)
    directors = {}
    for _, row in df.iterrows():
        crew = eval(row['crew'])  # List of dicts
        director = next((c for c in crew if c['job'] == 'Director'), None)
        if director and director['name'] not in directors:
            dir_obj = Director(name=director['name'], birth_year=None, description=None)  # Birth/desc not in CSV
            db.add(dir_obj)
            db.flush()
            directors[director['name']] = dir_obj.id

    # Genres (unique)
    genres = {}
    for genres_str in df['genres']:
        genre_list = eval(genres_str)
        for g in genre_list:
            if g['name'] not in genres:
                genre_obj = Genre(name=g['name'], description=None)
                db.add(genre_obj)
                db.flush()
                genres[g['name']] = genre_obj.id

    # Movies
    for _, row in df.iterrows():
        crew = eval(row['crew'])
        director = next((c for c in crew if c['job'] == 'Director'), None)
        if not director:
            continue
        dir_id = directors.get(director['name'])
        release_year = int(row['release_date'][:4]) if pd.notnull(row['release_date']) else None
        if not release_year:
            continue

        movie = Movie(
            title=row['title'],
            director_id=dir_id,
            release_year=release_year,
            cast=', '.join([c['name'] for c in eval(row['cast'])[:5]])  # Top 5 cast
        )
        db.add(movie)
        db.flush()

        # Genres association
        genre_list = eval(row['genres'])
        for g in genre_list:
            genre_id = genres.get(g['name'])
            if genre_id:
                db.execute(movie_genres.insert().values(movie_id=movie.id, genre_id=genre_id))

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
