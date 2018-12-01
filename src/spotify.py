from string import Template
from urllib.parse import parse_qs
import requests
import webbrowser
import json

SPOTIFY_BASE_URL = {
    'API': 'https://api.spotify.com',
    'ACCOUNTS': 'https://accounts.spotify.com'
}

AUTHENTICATION_FILENAME = 'spotify_authentication.json'


class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authentication = None

    def __build_login_url(self, scopes='user-read-currently-playing'):
        readable_template_string = [
            SPOTIFY_BASE_URL['ACCOUNTS'],
            '/authorize?',
            'client_id=${client_id}&',
            'redirect_uri=${redirect_uri}&',
            'scope=${scope}&'
            'response_type=code'
        ]

        base_url = Template(''.join(readable_template_string))

        return base_url.substitute(client_id=self.client_id, redirect_uri=self.redirect_uri, scope=scopes)

    def __get_authentication(self, code):
        try:
            request = requests.post(
                SPOTIFY_BASE_URL['ACCOUNTS'] + '/api/token',
                {
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
            )
        except requests.exceptions.HTTPError as exception:
            print(exception.errno)
            return
        except Exception:
            print(exception)
            return

        authentication = request.json()

        self.authentication = authentication
        self.__save_authentication(authentication)

    def __refresh_authentication(self):
        try:
            request = requests.post(
                'https://accounts.spotify.com/api/token',
                {
                    'grant_type': 'refresh_token',
                    'refresh_token': self.authentication['refresh_token'],
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
            )
            request.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            print(exception.errno)
            return
        except Exception:
            print(exception)
            return

        self.authentication = request.json()

    def __save_authentication(self, authentication):
        f = open(AUTHENTICATION_FILENAME, "w+")
        json.dump(authentication, f)

    def __load_authentication(self):
        f = open(AUTHENTICATION_FILENAME, "r")
        self.authentication = json.load(f)

    def login(self):
        try:
            self.__load_authentication()
            self.__refresh_authentication()
        except Exception as exception:
            print('Autologin failed due to: ' + str(exception))

            login_url = self.__build_login_url()
            code = input('Open ' + login_url + ' and paste here the code here:')
            self.__get_authentication(code)

    def get_currently_playing(self):
        if self.authentication == None:
            raise Exception('UNAUTHORIZED')  # FIXME: create real exceptions

        url = SPOTIFY_BASE_URL['API'] + '/v1/me/player/currently-playing'
        headers = {'Authorization': 'Bearer ' +
                   self.authentication['access_token']}

        return requests.get(url, headers=headers).json()
