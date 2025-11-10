import requests
from typing import Dict, List, Any
import json
import logging
import time
from utils.config import Config


class MovieDBClient:
    def __init__(self, base_url: str, api_token: str):
        self.api_token = api_token
        self.base_url = base_url
        self.session: requests.Session | None = None

    def _init_http_session(self) -> None:
        """
        Initializes the HTTP session for requests
        """
        self.session = requests.Session()

    def _request(
        self, method: str, endpoint_or_url: str, **kwargs: Any
    ) -> requests.Response:
        """
        Internal method to perform an HTTP request using the session.
        Returns the response text.
        """
        if self.session is None:
            self._init_http_session()
        headers: Dict[str, str] = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_token}"

        if endpoint_or_url.startswith(("http://", "https://")):
            url = endpoint_or_url
        else:
            url = f"{self.base_url}" f'/{endpoint_or_url.lstrip("/")}'

        assert self.session is not None
        response = self.session.request(method, url, headers=headers, **kwargs)
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response headers: {response.headers}")
        logging.debug(f"Response content: {response.content!r}")
        response.raise_for_status()
        return response

    def get(self, endpoint_or_url: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", endpoint_or_url, **kwargs)

    def discover_movies(self, page: int = 1):
        """
        Fetches a list of movies from the MovieDB API for a specific page.

        Args:
            page (int): The page number to fetch movies from. Defaults to 1.

        Returns:
            dict: A dictionary containing the JSON response from the API, which includes movie details.
        """
        endpoint = f"discover/movie?page={page}"
        response = self.get(endpoint)
        return response.json()

    def get_list_of_movies_ids(self, count: int) -> List[int]:
        """
        Retrieves a list of movie IDs from the MovieDB API.

        Args:
            count (int): The number of movie IDs to retrieve.

        Returns:
            List[int]: A list of movie IDs, limited to the specified count.
        """
        movie_ids = []
        page = 1
        while len(movie_ids) < count:
            data = self.discover_movies(page=page)
            movie_ids.extend(
                [movie["id"] for movie in data.get("results", [])]
            )
            page += 1
        return movie_ids[:count]

    def get_movie_details(self, movie_id: int):
        """
        Fetches detailed information about a specific movie from the MovieDB API.

        Args:
            movie_id (int): The ID of the movie to fetch details for.

        Returns:
            dict: A dictionary containing details about the movie, such as its title, overview, release date, and rating.
        """
        time.sleep(5)
        endpoint = f"movie/{movie_id}"
        response = self.get(endpoint)
        json_response = response.json()
        details = {
            "id": json_response.get("id", None),
            "title": json_response.get("title", ""),
            "overview": json_response.get("overview", ""),
            "release_date": json_response.get("release_date", ""),
            "rating": json_response.get("vote_average", None),
        }
        return details

if __name__ == "__main__":
    client = MovieDBClient(
        base_url=Config.get_moviedb_base_url(),
        api_token=Config.get_moviedb_token(),
    )
    movie_ids = client.get_list_of_movies_ids(1)
    for movie_id in movie_ids:
        details = client.get_movie_details(movie_id)
        print(json.dumps(details, indent=4))
