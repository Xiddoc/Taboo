"""
The high-level API for Taboo.
"""
from hashlib import md5
from typing import List

from engine.algorithm.LinkedInEngine import LinkedInEngine
from engine.algorithm.SearchEngine import SearchEngine
from engine.results.TabooResults import TabooResults
from frontend.logger import log


class TabooEngine:
    """
    Class to expose the high level Taboo API.
    """

    def __init__(self):
        # Result cache re-use
        self.__search = SearchEngine()
        self.__linkedin = LinkedInEngine()

    def query(self, strong_query: List[str], soft_query: List[str]) -> TabooResults:
        """
        Runs a taboo query.
        """
        # Get the LinkedIn usernames that match our query
        log.info("Retrieving links for query...")
        usernames = self.__search.get_links(strong_query, soft_query)

        # For each user, extract the information from their profile
        log.info("Extracting data from results...")
        users_data = []
        for i, user in enumerate(usernames):
            log.info(f"Downloading profile {md5(user.encode()).hexdigest()} ({i + 1}/{len(usernames)})...")
            user_info = self.__linkedin.get_info(user)
            if user_info is not None:
                users_data.append(user_info)
            else:
                log.warn(f"Could not download profile...")

        # Return the data
        return TabooResults(users_data)
