"""
Format the output into an Excel file.
"""
from typing import Dict, List

import pandas as pd
from xlsxwriter import Workbook
from xlsxwriter.chart_column import ChartColumn
from xlsxwriter.worksheet import Worksheet

from engine.results.TabooResults import TabooResults


class ExcelTabooResults(TabooResults):
    """
    Class manager for formatting, analyzing, and saving data into an Excel file.
    """

    def __init__(self, user_data: List[Dict]) -> None:
        super().__init__(user_data)
        # Convert to DataFrame, analyze below
        self.df = pd.DataFrame(self.data)
        self.df.drop([
            'elt', 'geoLocationBackfilled', 'geoCountryUrn', 'geoCountryName', 'student', 'locationName', 'entityUrn',
            'industryUrn', 'geoLocation', 'location', 'displayPictureUrl', 'img_200_200', 'img_400_400', 'img_800_800',
            'img_100_100', 'languages', 'publications', 'certifications', 'volunteer', 'honors', 'profile_urn',
            'member_urn', 'skills'
        ], axis=1, inplace=True)
        # Get all the skills (flatten the nested lists)
        all_skills = []
        for profile in user_data:
            all_skills.extend(profile['skills'])
        self.skill_df = pd.Series(all_skills)

    def save(self, query_id: str) -> None:
        """
        Saves to an excel file.
        """
        super().save(query_id)

        # Create an .xlsx file
        ex = pd.ExcelWriter(query_id + ".xlsx", engine='xlsxwriter')
        # Save the DF, this also creates the sheet
        self.df.to_excel(ex, sheet_name="Taboo Results", index=False)

        # Now we can get references to the workbook and the worksheet
        workbook: Workbook = getattr(ex, 'book')
        worksheet: Worksheet = ex.sheets['Taboo Results']

        # Add Industry chart
        self.df['industryName'].value_counts(normalize=True).to_excel(ex, sheet_name="Industry Counts", header=False)
        unique_industries = len(self.df['industryName'].unique())
        # Styling
        chart: ChartColumn = workbook.add_chart({'type': 'column'})
        chart.set_legend({'position': 'none'})
        chart.set_x_axis({'name': 'Industry Type'})
        chart.set_y_axis({'name': 'Relative Count'})
        chart.set_size({'height': 21.333 * 15, 'width': 64 * (unique_industries + 1)})
        # Create and add the series
        chart.add_series({
            'categories': ["Industry Counts", 0, 0, unique_industries - 1, 0],
            'values': ["Industry Counts", 0, 1, unique_industries - 1, 1],
            'gap': 15,
        })
        worksheet.insert_chart(f"B{len(self.data) + 3}", chart)

        # Add Skills chart
        self.skill_df.value_counts(normalize=True).to_excel(ex, sheet_name="Skills Counts", header=False)
        unique_skills = len(self.skill_df.unique())
        # Styling
        chart: ChartColumn = workbook.add_chart({'type': 'column'})
        chart.set_legend({'position': 'none'})
        chart.set_x_axis({'name': 'Tech'})
        chart.set_y_axis({'name': 'Relative Count'})
        chart.set_size({'height': 350, 'width': 64 * (unique_skills + 1)})
        # Create and add the series
        chart.add_series({
            'categories': ["Skills Counts", 0, 0, unique_skills - 1, 0],
            'values': ["Skills Counts", 0, 1, unique_skills - 1, 1],
            'gap': 15,
        })
        worksheet.insert_chart(f"B{len(self.data) + 20}", chart)

        # Save all the data to the file and close the writer
        ex.save()
