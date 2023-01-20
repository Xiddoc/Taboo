"""
Taboo
Don't speak and you shall not hear.
"""

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

    from engine.algorithm.TabooEngine import TabooEngine
    from engine.results.TabooResults import TabooResults
    from engine.results.result_format_mapping import FMT_MAPPING

    # Make sure we got a query
    if not Args.args['query']:
        strong_query = []
        soft_query = []
        log.info("No input found, write below:")
        # Keep looping till we get a query
        user_input = None
        while not user_input:
            user_input = input("> ").strip()
        raise NotImplementedError("In-program input not completed yet.")
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
    this_query_id = TabooResults.create_query_id(strong_query, soft_query, Args.args['pages'])
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
        log.info(f"No cache found, running engine...")
        eng = TabooEngine()
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
        log.info(f'Saving results to file...')
        formatted_results.save(this_query_id)
    else:
        log.info("No output path specified to write results to...")
