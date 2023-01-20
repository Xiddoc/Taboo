"""
Configurable settings.
"""
from typing import Dict

# Path to store the cache of queries at
CACHE_PATH = "cache"

# Load directly from .env file, not env vars
with open(".env") as f:
    accs = f.readlines()

# Accounts to use for LinkedIn scraping
LINKEDIN_ACCS: Dict[str, str] = {
    # Get first part of =, then get the second part
    line.split('=', 1)[0]: line.split('=', 1)[1]
    for line in accs
}
