"""
Taboo
Don't speak and you shall not hear.
"""
from typing import List

from frontend.Args import Args
from frontend.logo import get_intro

if __name__ == "__main__":
    # Gotta have a little neato branding :)
    print(get_intro())

    """
    Parse the CMD line arguments.
    """
    # Parse the command line arguments one time,
    # Then the class will statically cache it for later
    Args().parse_cmd_args()

    from frontend.logger import log
    log.info("Loading Taboo engine and modules...")

    # Load them dynamically since large modules will take quite a while to import
    # I'm looking at you, pandas ...
    from engine.algorithm.TabooEngine import TabooEngine
    from engine.algorithm.SearchEngine import SearchEngine
    from engine.results.TabooResults import TabooResults
    from engine.results.result_format_mapping import FMT_MAPPING

    # Create cache folder for result memoization
    if TabooResults.init_cache():
        log.info("No cache folder found, created one...")

    # Check if we got a file as input or a query
    linkedin_users, strong_query, soft_query = None, None, None
    if Args.args['infile']:
        log.info("Reading input file data...")
        # Strip links
        linkedin_urls: List[str] = Args.args['infile'].readlines()
        linkedin_urls = [url.strip() for url in linkedin_urls if url.strip()]

        # Error check after stripping
        if not linkedin_urls:
            raise ValueError(f"No links inputted: {linkedin_urls}")

        # Parse URLs for usernames
        linkedin_users = SearchEngine.extract_usernames_from_links(linkedin_urls)
    else:
        # Split the query by strength category
        strong_query, soft_query = Args.split_by_strength(Args.args['query'])
        strong_query_repr = ' '.join(w.upper() for w in strong_query)
        soft_query_repr = ' '.join(w.lower() for w in soft_query)
        log.info(f"Found input query: {strong_query_repr} {soft_query_repr}")

    """
    Check for caching to save computing/networking time.
    """
    # Create the unique ID for this query
    this_query_id = TabooResults.create_query_id(linkedin_users, strong_query, soft_query, Args.args['pages'])
    log.info(f"Identifying query with unique ID {this_query_id}...")
    # First check if there is a cache for this item,
    # So we don't execute the same exact query multiple times
    log.info("Checking taboo cache for old results...")
    if TabooResults.get_cache_path(this_query_id).exists():
        """
        If there is a cache, we will use the old version
        """
        log.info(f"Cache found, loading {this_query_id}...")
        results = TabooResults.load(this_query_id)
    else:
        """
        Execute the query if there is no cache.
        """
        log.info("No cache found, running engine...")
        eng = TabooEngine()

        # Use input usernames if we got it as input
        if linkedin_users:
            log.info("Running engine on input list from file...")
            results = eng.process_usernames(linkedin_users)
        else:
            log.info("Running search engine on input query...")
            results = eng.query(strong_query, soft_query)

        log.info("Engine was successful...")
        # Save the results to the cache so next time we
        # will not have to run the engine again
        results.save(this_query_id)

    """
    Now that we have the data, handle the ouput.
    """
    if Args.args['format'] is not None:
        # Convert to the given format
        log.info(f"Converting results to format {Args.args['format'].upper()}...")
        format_class = FMT_MAPPING[Args.args['format']]
        # Instantiate the target format class
        formatted_results = format_class(results.data)

        # User gave us a path to write the results to
        log.info(f'Saving results to file with ID "{this_query_id}"...')
        formatted_results.save(this_query_id)
    else:
        log.info("No output path specified to write results to...")
