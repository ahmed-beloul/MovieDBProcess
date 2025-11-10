class Config:
    @staticmethod
    def get_moviedb_token() -> str:
        return "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZjhjNTRiNTVhNGU1NDA1OGY1NDU2OWJlYTNjNWJkOSIsIm5iZiI6MTc2MTkzOTU4NS4xMDYsInN1YiI6IjY5MDUxMDgxZmI4NzE5MjMwMmUxMjJkNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.a_dS5KH3d404iE8Bj9iVVD728zoRpe0HeMDgqg_t_kw"

    @staticmethod
    def get_moviedb_base_url() -> str:
        return "https://api.themoviedb.org/3"

    @staticmethod
    def get_post_simulation_url() -> str:
        return "https://jsonplaceholder.typicode.com/posts"
