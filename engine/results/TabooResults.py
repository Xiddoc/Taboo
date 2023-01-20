"""
Base class for results.
Holds all the data found, without extra processing.
"""
from bz2 import compress, decompress
from hashlib import md5
from json import loads, dumps
from os import getcwd, mkdir
from os.path import dirname
from pathlib import Path
from sys import argv
from typing import List, Dict, Optional, Iterable

from config import CACHE_PATH


class TabooResults:
    """
    Akin to a dataclass for the output data.
    """

    def __init__(self, user_data: List[Dict]) -> None:
        # Store the data for later
        self.data = user_data

    @staticmethod
    def create_query_id(user_list: Iterable[str],
                        strong_query: Optional[List[str]], soft_query: Optional[List[str]], pages: int) -> str:
        """
        Takes a query and returns a unique identifier for it (as a string).
        This will hash the query if it was inputted, or the filename if it was given.

        :return: A string which deterministically hashes the input arguments.
        """
        # If we got a file as input, then we will hash by the list of usernames we got
        if user_list:
            # Turn the iterable to a deterministic string
            hash_str = "".join(sorted(user_list))
            # Hash the usernames
            return md5(hash_str.encode()).hexdigest()
        else:
            # If we got a query as input

            # Sort the queries so even if you rearrange them, it's the same
            # However, if you change a query from strong to soft, it should change the ID
            return \
                str(pages) + '_' + \
                md5(str(sorted(strong_query)).lower().encode()).hexdigest() + \
                md5(str(sorted(soft_query)).lower().encode()).hexdigest()

    @classmethod
    def init_cache(cls) -> bool:
        """
        Creates the result cache folder, if it does not exist already.
        """
        try:
            mkdir(cls.get_base_cache_path())
        except OSError:
            return False

        # Folder created successfully
        return True

    @staticmethod
    def get_base_cache_path() -> Path:
        """
        :return: The full path to the result cache folder.
        """
        # Get the base path
        path = dirname(argv[0])
        if not path:
            path = getcwd()
        # Build the full path to the cache
        return Path(path, CACHE_PATH)

    @classmethod
    def get_cache_path(cls, query_id: str) -> Path:
        """
        Creates the full path to the cached query file.
        """
        return cls.get_base_cache_path() / Path(query_id + ".bin")

    @classmethod
    def load(cls, query_id: str) -> "TabooResults":
        """
        Loads a query's UID into a TabooResults class.
        """
        # Read the file contents,
        with open(cls.get_cache_path(query_id), 'rb') as f:
            # Load it from JSON,
            # And return the class instance
            return TabooResults(loads(decompress(f.read())))

    def save(self, query_id: str) -> None:
        """
        Saves these results to the cache.
        """
        with open(self.get_cache_path(query_id), 'wb') as f:
            # Dump to a JSON,
            # then write to the file as binary
            f.write(compress(dumps(self.data).encode()))
