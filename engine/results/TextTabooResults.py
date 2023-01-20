"""
Format the output into a txt (text) file.
"""

from engine.results.TabooResults import TabooResults


class TextTabooResults(TabooResults):
    """
    Class manager for analyzing and saving the data to a txt file.
    """

    def save(self, query_id: str) -> None:
        """
        Saves to an excel file.
        """
        super().save(query_id)
