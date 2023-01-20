"""
Handles searching up information.
"""
from random import randint
from time import sleep
from typing import List, Set, Dict
from urllib.parse import urlparse

from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

from frontend.Args import Args
from frontend.hush_stdout import suppress_stdout
from frontend.logger import log


class SearchEngine:
    """
    Wrapper class for the Google search API.
    """

    def __init__(self):
        # Cache results
        self.__gsearch = GoogleSearch()

    def get_links(self, strong_query: List[str], soft_query: List[str]) -> Set[str]:
        """
        Executes the query and returns a set of unique LinkedIn usernames.
        Handles proxies, multiple pages, etc.
        """
        # Build the query
        site_filter = "site:linkedin.com"
        profile_filter = "inurl:/in/"
        query_str = " ".join([f'"{query}"' for query in strong_query] + soft_query)
        # Join the filter and query together
        final_query = " ".join([query_str, site_filter, profile_filter])

        # Execute the search for the amount of pages we asked for
        # TODO add proxies
        results: List[Dict] = []
        for page in range(Args.args['pages']):
            # Cast to dict
            log.info(f"Executing query #{page + 1}...")
            try:
                # Don't let the module print to console
                with suppress_stdout():
                    for result in self.__gsearch.search(final_query, page=page + 1).results:
                        # Add the results to the total list
                        results.append(dict(result))
            except NoResultsOrTrafficError:
                log.warn(f"No more query results found...")
                break

            # Rate limit ourselves
            if Args.args['pages'] > 1:
                sleep(randint(3, 5))

        # Get unique URL paths
        log.info(f"Found {len(results)} total results...")
        log.info("Extracting unique results...")
        usernames = set()
        for result in results:
            # Parse the link
            parse_result = urlparse(result['links'])
            if parse_result.path.startswith('/in/'):
                # Cut off the start of the path and add to the list of usernames
                usernames.add(parse_result.path.removeprefix('/in/').split('/')[0])

        # Give back the available usernames
        log.info(f"Found {len(usernames)} unique results...")
        return usernames
