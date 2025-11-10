from utils.config import Config
from utils.moviedb_client import MovieDBClient
from utils.post_simulation_client import PostSimulationClient
from typing import List
from datetime import datetime
from tqdm import tqdm


def main():
    start_time = datetime.now()
    moviedb_client = MovieDBClient(
        base_url=Config.get_moviedb_base_url(),
        api_token=Config.get_moviedb_token(),
    )
    movie_ids: List[int] = moviedb_client.get_list_of_movies_ids(count=5)
    unique_ids: List[str] = []

    for movie_id in tqdm(movie_ids):
        process_movies(moviedb_client, movie_id, unique_ids)

    open("unique_ids.txt", "w").close()
    with open("unique_ids.txt", "w") as f:
        for uid in unique_ids:
            f.write(f"{uid}\n")

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"Total processing time: {elapsed_time}")


def process_movies(
    moviedb_client: MovieDBClient, movie_id: int, list_unique_ids: List[str]
) -> None:
    post_simulation_client = PostSimulationClient(
        base_url=Config.get_post_simulation_url()
    )
    details = moviedb_client.get_movie_details(movie_id)
    unique_id = post_simulation_client.create_post(
        id=details["id"],
        title=details["title"],
        overview=details["overview"],
        release_date=details["release_date"],
        rating=details["rating"],
    )
    list_unique_ids.append(unique_id)


if __name__ == "__main__":
    main()
