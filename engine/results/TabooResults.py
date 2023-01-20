"""
Base class for results.
Holds all the data found, without extra processing.
"""
from bz2 import compress, decompress
from hashlib import md5
from json import loads, dumps
from os import getcwd
from os.path import dirname
from pathlib import Path
from sys import argv
from typing import List, Dict

from config import CACHE_PATH


class TabooResults:
    """
    Akin to a dataclass for the output data.
    """

    def __init__(self, user_data: List[Dict]) -> None:
        # Store the data for later
        self.data = user_data

    @staticmethod
    def create_query_id(strong_query: List[str], soft_query: List[str], pages: int) -> str:
        """
        Takes a query and returns a unique identifier for it (as a string).
        """
        # Sort the queries so even if you rearrange them, it's the same
        # However, if you change a query from strong to soft, it should change the ID
        return \
            str(pages) + '_' + \
            md5(str(sorted(strong_query)).lower().encode()).hexdigest() + \
            md5(str(sorted(soft_query)).lower().encode()).hexdigest()

    @classmethod
    def get_cache_path(cls, query_id: str) -> Path:
        """
        Creates the full path to the cached query file.
        """
        # Get the base path
        path = dirname(argv[0])
        if not path:
            path = getcwd()
        # Build the full path to the cache
        return Path(path, CACHE_PATH, query_id + ".bin")

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
