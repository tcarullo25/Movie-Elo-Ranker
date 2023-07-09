import math, random, statistics
from scipy.stats import t

#https://www.kosbie.net/cmu/fall-21/15-112/notes/notes-variables-and-functions.html
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def getChoice(old_movie, new_movie):
    while True:
        choice = input(f"Which movie do you prefer?\n1. {new_movie}\n2. {old_movie}\n")
        if choice not in "12":
            print("Please select option 1 or 2")
        elif choice in "1":
            return "1"
        elif choice in "2":
            return "2"

# calculates expected probability of movie winning by using 
def calculate_expected_probability(new_movie_rating, old_movie_rating):
    return 1 / (1 + 10 ** ((old_movie_rating - new_movie_rating) / 400))

def update_ratings(new_movie_rating, old_movie_rating, outcome):
    K = 32
    new_mov_exp_prob = calculate_expected_probability(new_movie_rating, old_movie_rating)
    old_mov_exp_prob = 1 - new_mov_exp_prob
    if outcome == "1":
        new_movie_rating = new_movie_rating + K * (1-new_mov_exp_prob)
        old_movie_rating = old_movie_rating + K * -old_mov_exp_prob
    else:
        new_movie_rating = new_movie_rating + K * -new_mov_exp_prob
        old_movie_rating = old_movie_rating + K * (1-old_mov_exp_prob)
    return roundHalfUp(new_movie_rating), roundHalfUp(old_movie_rating)

def calculate_tolerance(total_movies, confidence_level):
    # Calculate the tolerance dynamically based on the total number of movies
    # and the desired confidence level
    degrees_of_freedom = total_movies - 1
    alpha = 1 - confidence_level
    t_critical = t.ppf(1 - alpha/2, df=degrees_of_freedom)
    tolerance = t_critical / math.sqrt(total_movies)
    return tolerance

def ratings_stable(rating_changes, confidence_level = .90, tolerance = 5):
    if len(rating_changes) <= 1:
        return False
    sample_std_dev = statistics.stdev(rating_changes)
    sample_size = len(rating_changes)
    
    alpha = 1 - confidence_level
    t_critical = t.ppf(1 - alpha/2, df=sample_size-1)
    margin_of_error = t_critical * sample_std_dev / (sample_size**0.5)
    return margin_of_error <= tolerance

def getNewMatch(movies, match_count):
    # change it so that it prioritizes movies that have less match ups
    old_movie = random.choice(list(movies[match_count % 4].keys()))
    old_movie_rating = movies[match_count % 4][old_movie]
    return old_movie, old_movie_rating

def flatten_movies(movies, new_movie, new_movie_elo):
    flattened_list = [(new_movie, new_movie_elo)]
    for bracket in movies:
        for movie, elo in bracket.items():
            flattened_list.append((movie, elo))
    return flattened_list

def update_movies(movies):
    filename = r'movies.txt'
    movies.sort(key=lambda x: x[1], reverse = True)
    with open(filename, "w") as file:
        for movie, rating in movies:
            file.write(f"{movie} - RATING: {rating}\n")

def game_logic(movies, new_movie, start_new_movie_rating, total_movies):
    match_count = 0
    rating_changes = []
    prev_new_movie_rating = start_new_movie_rating 
    while not ratings_stable(rating_changes):
        old_movie, prev_old_movie_rating = getNewMatch(movies, match_count)
        outcome = getChoice(old_movie, new_movie)
        new_movie_rating, old_movie_rating = update_ratings(prev_new_movie_rating, prev_old_movie_rating, outcome)
        rating_changes.append((abs(new_movie_rating - prev_new_movie_rating)))
        movies[match_count % 4][old_movie] = old_movie_rating
        prev_new_movie_rating = new_movie_rating
        print(f"{new_movie}'s new rating: {new_movie_rating}")
        print(f"{old_movie}'s new rating: {old_movie_rating}\n")
        match_count += 1
    print("Match calibration complete!")
    flattened_movies = flatten_movies(movies, new_movie, new_movie_rating)
    update_movies(flattened_movies)
    new_movies, _, _ = get_movies(flattened_movies)
    return new_movies


def parse_movies_and_elos():
    filename = r'movies.txt'
    movies = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.isspace():
                continue
            rating_start = line.find(' - RATING:')
            movie = line[:rating_start]
            elo = int(line[rating_start + len(' - RATING:'):])
            movies.append((movie, elo))
    return movies

def get_movies(movies_and_elos):
    movies_and_elos.sort(key=lambda x: x[1], reverse = True)
    movie_list = [item[0] for item in movies_and_elos]
    elo_list = [item[1] for item in movies_and_elos]
    average_elo = statistics.mean(elo_list)
    total_movies = len(movie_list)
    total_brackets = 4
    movies_per_bracket = total_movies // total_brackets
    leftover_movies = total_movies % total_brackets
    movies = []
    for bracket in range(0, total_movies-leftover_movies, movies_per_bracket):
        movie_dict = dict()
        for i in range(len(movie_list[bracket:movies_per_bracket + bracket])):
            movie = movie_list[bracket:movies_per_bracket + bracket][i]
            movie_dict[movie] = elo_list[bracket + i]
        movies.append(movie_dict)
    for i in range(leftover_movies):
        curr_index = total_movies-leftover_movies+i
        curr_movie = movie_list[curr_index] 
        curr_elo = elo_list[curr_index]
        movies[-1][curr_movie] = curr_elo
    return movies, average_elo, total_movies

def print_movies(movies):
    count = 1
    for bracket in movies:
        for movie in bracket:
            print(f"{count}. {movie} - {bracket[movie]}\n")
            count += 1

def main():
    movies, new_movie_start_rating, total_movies = get_movies(parse_movies_and_elos())
    while True:
        enter_movie = input("Would you like to enter a new movie? (Y/N)\n")
        if enter_movie not in "YN":
            print("Please enter a valid response")
        if enter_movie == "Y":
            new_movie = input("Please enter the movie:\n")
            movies = game_logic(movies, new_movie, new_movie_start_rating, total_movies)
            print_movies(movies)
        elif enter_movie == "N":
            break
main()
