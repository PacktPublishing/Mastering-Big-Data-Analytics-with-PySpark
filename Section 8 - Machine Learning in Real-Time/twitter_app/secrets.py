"""Replace the values below with your own Twitter API Keys, Secrets, and Tokens"""

# Twitter Consumer API keys
CONSUMER_KEY    = "szt9ytUAMAlEyqHiJH0c8hWas"
CONSUMER_SECRET = "0m4A3izC3brsO0rto7C2A6Q52BgPVKxTRmbMJvJvdcHsedBVzY"

# Twitter Access token & access token secret
ACCESS_TOKEN    = "1152234679065595906-Pat8sOnyeOi5onpSX7hM545GTc6UmE"
ACCESS_SECRET   = "YEEw2viJr6URtYbnLw1Wqu5cjeMzMRvxkjwr4aku8TnUz"


class TwitterSecrets:
    """Class that holds Twitter Secrets"""

    def __init__(self):
        self.CONSUMER_KEY    = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_TOKEN    = ACCESS_TOKEN
        self.ACCESS_SECRET   = ACCESS_SECRET
        
        # Tests if keys are present
        for key, secret in self.__dict__.items():
            assert secret != "", f"Please provide a valid secret for: {key}"

        
twitter_secrets = TwitterSecrets()
