"""
Command line argument handling.
"""
from argparse import ArgumentParser, FileType
from typing import Dict, List, Tuple


class Args:
    """
    Argument handler and command line parser.
    """

    # Static declaration
    args: Dict = {}

    def __init__(self) -> None:
        # Build the argument parser
        parser = ArgumentParser()
        # Might need to account later for proxies
        parser.add_argument('-p', '--pages', type=int, required=False, default=1,
                            help="The amount of times to execute the query. "
                                 "More pages means more data collected. Defaults to one page.")
        # Dynamically take the available formats from the format mapping
        parser.add_argument('-f', '--format', type=str, required=False,
                            choices=['excel', 'text'],
                            help="The output format to write to. By default, it does not output anywhere.")
        # parser.add_argument('-f', '--format', type=str, required=False,
        #                            choices=['excel', 'text'], default='text',
        #                            help="The output format to write to. Defaults to a text output.")
        # # The file path to save to, might need to fix later to account for CWD
        # parser.add_argument('-o', '--out', type=str, required=False,
        #                            help="The output file path to save the results to.")

        # QUERYING INPUT ARGUMENT
        # Either a file or Google query
        query_group = parser.add_mutually_exclusive_group(required=True)
        query_group.add_argument('--query', nargs="+",
                                 help="The taboo query to execute. Add a plus (+) character at the start of the "
                                      "query word to make it a strong query word.")
        query_group.add_argument('--infile', type=FileType(),
                                 help="A file with a link to a LinkedIn on each line, will take these as input instead"
                                      " of using a query for a Google search.")

        # Assign to self
        self.__parser = parser

    def parse_cmd_args(self) -> None:
        """
        Parses the command line arguments.
        """
        # Parse right now and cache statically for later
        Args.args = vars(self.__parser.parse_args())

    @staticmethod
    def split_by_strength(query_list: List[str]) -> Tuple[List[str], List[str]]:
        """
        Splits the query list by strong queries and soft queries.
        A strong query is represented by a + at the start.
        If the input was:
            +CIA backdoor cyber

        Then the output would be:
            ([CIA], [backdoor, cyber])

        :param query_list: The total list of queries to use.
        :return: A tuple of strong queries and soft queries, both as lists.
        """
        # Parse the user arguments by strength
        strong_query: List[str] = []
        soft_query: List[str] = []
        for query_str in query_list:
            # If the argument is passed with a '+' at the start,
            # it is a strong query (must be found later)
            if query_str.startswith("+"):
                strong_query.append(query_str[1:].strip())
            else:
                soft_query.append(query_str.strip())

        return strong_query, soft_query
