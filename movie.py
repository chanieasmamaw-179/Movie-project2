import argparse
import random
import statistics as stat
import matplotlib.pyplot as plt
import sys

sys.path.append('/Users/masterschool/Desktop/Movei_project_2/Movei_project_2/Movei_project2/storage')
from storage import get_movies, add_movie, delete_movie, update_movie


class MovieCollection:
    """Class to manage a collection of movies."""

    def __init__(self):
        self.movies = get_movies()  # Load movies from persistent storage

    def add_movie(self, title, rating, genre, year):
        add_movie(self.movies, title, rating, genre, year)

    def list_movies(self):
        if not self.movies:
            print("No movies in the list.")
        else:
            for movie in self.movies.values():
                print(f"{movie['title']} ({movie['genre']}, {movie['year']}): {movie['rating']} rating")
    
    def update_movie(self, title, new_rating, new_genre):
	    if title in self.movies:
		    self.movies[title]['rating'] = new_rating
		    self.movies[title]['genre'] = new_genre
		    print(f"Updated movie: {title} with rating {new_rating} and genre {new_genre}")
	    else:
		    print(f"Movie {title} not found.")

    def delete_movie(self, title):
        delete_movie(self.movies, title)

    def show_stats(self):
        if self.movies:
            ratings = [movie['rating'] for movie in self.movies.values()]
            average_rating = stat.mean(ratings)
            median_rating = stat.median(ratings)
            best_movie = max(self.movies.values(), key=lambda x: x['rating'])
            worst_movie = min(self.movies.values(), key=lambda x: x['rating'])
            print(f"Average rating: {average_rating:.2f}")
            print(f"Median rating: {median_rating:.2f}")
            print(f"Best rating: {best_movie['rating']} ({best_movie['title']} ({best_movie['year']}))")
            print(f"Worst rating: {worst_movie['rating']} ({worst_movie['title']} ({worst_movie['year']}))")

            # Plotting the ratings of movies
            titles = [movie['title'] for movie in self.movies.values()]
            plt.figure(figsize=(8, 6))
            plt.bar(titles, ratings, color='black')
            plt.xlabel('Movies')
            plt.ylabel('Ratings')
            plt.title('Ratings of Movies')
            plt.xticks(rotation=90)
            plt.show()
        else:
            print("No statistics to calculate.")

    def show_random_movie(self):
        if self.movies:
            random_movie = random.choice(list(self.movies.values()))
            print(
                f"Random movie: {random_movie['title']} ({random_movie['genre']}, {random_movie['year']}): {random_movie['rating']} rating")
        else:
            print("No movies available.")

    def sort_movies_by_rating(self):
        sorted_movies = sorted(self.movies.values(), key=lambda x: x['rating'])
        for movie in sorted_movies:
            print(f"Sorted movie: {movie['title']} ({movie['genre']}, {movie['year']}): {movie['rating']} rating")

    def search_movie(self, title):
        title_lower = title.lower()
        movie_titles = list(self.movies.keys())
        best_match, score = process.extractOne(title_lower, movie_titles, scorer=fuzz.partial_ratio)

        if score >= 50:  # Threshold for a good match
            movie = self.movies[best_match]
            print(
                f"Found {movie['title']} ({movie['genre']}, {movie['year']}): {movie['rating']} rating (Score: {score})")
        else:
            print(f"Movie {title} not found.")


def main():
    """Main function to handle command-line arguments and call the appropriate functions."""

    movie_collection = MovieCollection()

    while True:
        print("\nMenu")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Show statistics")
        print("6. Show random movie")
        print("7. Search movie by title")
        print("8. Show movies sorted by rating")

        choice = input("Enter your choice: ")

        try:
            if choice == "0":
                print("Exiting the program. Bye!")
                break
            elif choice == "1":
                movie_collection.list_movies()
            elif choice == "2":
                title = input("Enter movie title: ")
                rating = float(input("Enter movie rating: "))
                genre = input("Enter movie genre: ")
                year = int(input("Enter movie year: "))
                movie_collection.add_movie(title, rating, genre, year)
            elif choice == "3":
                title = input("Enter the title of the movie to delete: ")
                movie_collection.delete_movie(title)
            elif choice == "4":
                title = input("Enter the title of the movie to update: ")
                new_rating = float(input("Enter the new rating of the movie: "))
                new_genre = input("Enter the new genre of the movie: ")
                movie_collection.update_movie(title, new_rating, new_genre)
            elif choice == "5":
                movie_collection.show_stats()
            elif choice == "6":
                movie_collection.show_random_movie()
            elif choice == "7":
                title = input("Enter the title of the movie to search for: ")
                movie_collection.search_movie(title)
            elif choice == "8":
                movie_collection.sort_movies_by_rating()
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Value error: {e}. Please check your input and try again.")
        except KeyError as e:
            print(f"Key error: {e}. It seems like a movie was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
