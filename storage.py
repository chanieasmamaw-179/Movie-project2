import json
import os
from fuzzywuzzy import fuzz, process

# Define the path to the JSON file for persistent storage
DATA_FILE = 'movies.json'

def get_movies():
    """Load movies from the JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading movies: {e}")
        return {}
    except FileNotFoundError:
        print("Movies file not found.")
        return {}

def save_movies(movies):
    """Save movies to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(movies, file, indent=4)

def add_movie(movies, title, rating, genre, year, **kwargs):
    """Add a movie with additional properties to the dictionary."""
    title_lower = title.lower()
    if title_lower in movies:
        print(f"Movie {title} already exists.")
    else:
        movie = {"title": title, "rating": rating, "genre": genre, "year": year}
        movie.update(kwargs)  # Add additional properties
        movies[title_lower] = movie
        print(f"Added {title} ({year}) to {genre} with a rating of {rating}. Additional properties: {kwargs}")
        save_movies(movies)  # Save after adding

def delete_movie(movies, movie_title):
    """Delete a movie from the dictionary."""
    movie_title_lower = movie_title.lower()
    movie_titles = list(movies.keys())
    best_match, score = process.extractOne(movie_title_lower, movie_titles, scorer=fuzz.partial_ratio)
    if score >= 50:  # Threshold for a good match
        del movies[best_match]
        print(f"Deleted movie: {best_match.title()} (Score: {score})")
        save_movies(movies)  # Save after deleting
    else:
        print(f"Movie {movie_title} not found.")

def update_movie(movies, old_movie_title, new_movie_title, new_movie_rating, new_movie_genre, new_movie_year, **kwargs):
    """Update a movie's details including additional properties."""
    old_movie_title_lower = old_movie_title.lower()
    if old_movie_title_lower in movies:
        movie = {
            "title": new_movie_title,
            "rating": new_movie_rating,
            "genre": new_movie_genre,
            "year": new_movie_year
        }
        movie.update(kwargs)  # Update with additional properties
        movies[old_movie_title_lower] = movie
        print(f"Updated {old_movie_title} to {new_movie_title} ({new_movie_year}) with a rating of {new_movie_rating} in {new_movie_genre}. Additional properties: {kwargs}")
        save_movies(movies)  # Save after updating
    else:
        print(f"{old_movie_title} is not found.")
