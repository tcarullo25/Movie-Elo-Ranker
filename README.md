# Movie Elo Ranker

This project implements a movie Elo ranker, inspired by the Elo rating system used in chess. The Elo rating system is a method for calculating the relative skill levels of players in two-player games. In this case, we apply it to rank movies based on user preferences.

## How it Works

1. **Initialization**: The project reads the movie ratings from a file (`movies.txt`) and organizes them into brackets for the ranking process. Each movie is assigned an Elo rating, which represents its relative strength.
2. **New Movie Entry**: The user is prompted to enter a new movie for ranking. The movie is then added to the ranking process.
3. **Match Calibration**: The system selects two movies, one from the existing rankings and the other being the new movie. The user is asked to choose which movie they prefer. Based on the outcome, the Elo ratings of the movies are updated using the Elo rating formula.
4. **Ratings Stability**: The system checks if the ratings have stabilized by calculating the margin of error for the Elo rating changes. This ensures that the rankings have reached a stable state.
5. **Ranking Update**: Once the rankings have stabilized, the movies are sorted based on their Elo ratings and written back to the `movies.txt` file.
6. **Iteration**: The process continues until the user decides not to enter any more movies.

## Functions Overview

- `getChoice(old_movie, new_movie)`: Prompts the user to select their preferred movie between two options.
- `calculate_expected_probability(new_movie_rating, old_movie_rating)`: Calculates the expected probability of the new movie winning against the old movie based on their Elo ratings.
- `update_ratings(new_movie_rating, old_movie_rating, outcome)`: Updates the Elo ratings of the new and old movies based on the match outcome.
- `calculate_tolerance(total_movies, confidence_level)`: Calculates the tolerance value for rating stability based on the total number of movies and desired confidence level.
- `ratings_stable(rating_changes, confidence_level=.90, tolerance=5)`: Checks if the rating changes have stabilized based on the confidence level and tolerance.
- `getNewMatch(movies, match_count)`: Selects an old movie for a match, giving priority to movies with fewer matchups.
- `flatten_movies(movies, new_movie, new_movie_elo)`: Flattens the movies into a list of tuples (movie, Elo rating) for easier processing.
- `update_movies(movies)`: Updates the `movies.txt` file with the new rankings.
- `game_logic(movies, new_movie, start_new_movie_rating, total_movies)`: Implements the game logic for match calibration and ranking updates.
- `parse_movies_and_elos()`: Reads movie ratings from `movies.txt` and returns a list of movie-Elo rating tuples.
- `get_movies(movies_and_elos)`: Sorts movies based on their Elo ratings and returns a list of movie dictionaries representing the brackets.
- `print_movies(movies)`: Prints the movies with their respective Elo ratings.
