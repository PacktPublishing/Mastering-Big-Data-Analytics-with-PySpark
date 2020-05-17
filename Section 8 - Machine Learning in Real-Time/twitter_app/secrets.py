"""Replace the values below with your own Twitter API Keys, Secrets, and Tokens"""

# Twitter Consumer API keys
CONSUMER_KEY    = "<your_creds_go_here>"
CONSUMER_SECRET = "<your_creds_go_here>"

# Twitter Access token & access token secret
ACCESS_TOKEN    = "<your_creds_go_here>"
ACCESS_SECRET   = "<your_creds_go_here>"


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
