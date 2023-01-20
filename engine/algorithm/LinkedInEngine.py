"""
Extract the information we need from LinkedIn.
"""
from random import choice, randint
from time import sleep
from typing import Dict, List, Optional

from linkedin_api import Linkedin

from config import LINKEDIN_ACCS
from frontend.logger import log


class LinkedInEngine:
    """
    Wrapper class for the LinkedIn API.
    Should also handle account management and swapping for rate limits.
    """

    def __init__(self) -> None:
        # Load accounts to use
        log.info("Loading config accounts...")
        if not LINKEDIN_ACCS:
            raise ValueError("No account supplied to configuration file.")

        # Get a random account
        rand_email = choice(list(LINKEDIN_ACCS))
        rand_pass = LINKEDIN_ACCS[rand_email]

        # Authenticate session
        log.info("Authenticating account...")
        self.__linkedin = Linkedin(
            username=rand_email,
            password=rand_pass
        )

    def get_info(self, username: str, retry_attempt: int = 0) -> Optional[Dict]:
        """
        Download and extract our structured information about a user.

        Returns None if it can't find the user.
        """
        # TODO catch exceptions for rate limiting
        try:
            # Query the profile
            profile = self.__linkedin.get_profile(username)
            if 'profile_id' in profile:
                log.info(f"Successfully resolved {profile['profile_id']}...")
            else:
                raise ValueError(f"Unexpected result: {profile}")

            # And query the skills, but we will add them to the profile
            # since the API doesn't add the list to the result automatically
            skills = self.__linkedin.get_profile_skills(username)
            profile['skills'] = [skill['name'] for skill in skills]
            # Also courses are not found in the default profile
            profile['courses'] = self.__get_courses(username)

            # Return the mixed profile
            return profile
        except KeyError:
            # Give up after a few attempts
            if retry_attempt > 3:
                return None

            log.error(f"Error while resolving, retrying...")
            sleep(randint(5, 10))
            return self.get_info(username, retry_attempt + 1)

    def __get_courses(self, username: str) -> List[str]:
        """
        New API call for LinkedIn API that is not supported in Python API.
        """
        params = {"count": 100, "start": 0}
        # noinspection PyProtectedMember
        res = self.__linkedin._fetch(
            uri=f"/identity/profiles/{username}/courses",
            params=params
        )
        data = res.json()

        # Extract the names from the data
        return [item['name'] for item in data.get("elements", [])]
