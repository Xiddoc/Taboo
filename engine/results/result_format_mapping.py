"""
A mapping between the user-inputted format option to the class that implements this format.
"""
from typing import Dict, Type

from engine.results.ExcelTabooResults import ExcelTabooResults
from engine.results.TabooResults import TabooResults
from engine.results.TextTabooResults import TextTabooResults

FMT_MAPPING: Dict[str, Type[TabooResults]] = {
    'excel': ExcelTabooResults,
    'text': TextTabooResults
}
