import requests
import logging
from typing import Any, Dict
import hashlib


class PostSimulationClient:
    def __init__(
        self, base_url: str = "https://jsonplaceholder.typicode.com/posts"
    ):
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

        if endpoint_or_url.startswith(("http://", "https://")):
            url = endpoint_or_url
        else:
            url = f"{self.base_url}" f'/{endpoint_or_url.lstrip("/")}'

        assert self.session is not None
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def get(self, endpoint_or_url: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", endpoint_or_url, **kwargs)

    def post(self, endpoint_or_url: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", endpoint_or_url, **kwargs)

    def _unique_string_from_params(self, *params) -> str:
        combined = "_".join(map(str, params))
        return hashlib.md5(combined.encode()).hexdigest()

    def create_post(
        self,
        id: int,
        title: str,
        overview: str,
        release_date: str,
        rating: float,
    ) -> str:
        """
        Creates a new post in the JSONPlaceholder API.

        Args:
            id (int): The ID of the post.
            title (str): The title of the post.
            overview (str): The overview or body of the post.
            release_date (str): The release date associated with the post.
            rating (float): The rating associated with the post.

        Returns:
            str: A unique string identifier for the created post.
        """
        response = self.post(
            self.base_url,
            json={
                "id": id,
                "title": title,
                "overview": overview,
                "release_date": release_date,
                "rating": rating,
            },
        )
        if response.status_code == 201:
            logging.info("Post created successfully.")
            created_id = self._unique_string_from_params(id, title)
        else:
            raise ValueError(
                f"Failed to create post. Status code: {response.status_code}"
            )

        return created_id


if __name__ == "__main__":
    client = PostSimulationClient()
    response = client.create_post(
        id=1,
        title="Sample Movie",
        overview="This is a sample movie overview.",
        release_date="2024-01-01",
        rating=8.5,
    )
    print("Created post ID:", response)
