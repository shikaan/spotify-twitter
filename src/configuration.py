from os import environ


class ConfigurationManager:
    def __get_env(self, variable):
        try:
            return environ[variable]
        except:
            return None

    def __init__(self):
        self.__spotify = {
            'client_id': self.__get_env('SPOTIFY_CLIENT_ID'),
            'client_secret': self.__get_env('SPOTIFY_CLIENT_SECRET'),
            'redirect_uri': self.__get_env('SPOTIFY_REDIRECT_URI')
        }

        self.__twitter = {
            'consumer_key': self.__get_env('TWITTER_CONSUMER_KEY'),
            'consumer_secret': self.__get_env('TWITTER_CONSUMER_SECRET'),
            'access_token_key': self.__get_env('TWITTER_ACCESS_TOKEN_KEY'),
            'access_token_secret': self.__get_env('TWITTER_ACCESS_TOKEN_SECRET')
        }

    def getSpotifyConfiguration(self):
        return self.__spotify

    def getTwitterConfiguration(self):
        return self.__twitter
