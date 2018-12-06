import twitter
from configuration import ConfigurationManager
from spotify import SpotifyClient
from messenger import Messenger

configurationManager = ConfigurationManager()
messenger = Messenger()
spotifyClient = SpotifyClient(**configurationManager.getSpotifyConfiguration())
twitterClient = twitter.Api(**configurationManager.getTwitterConfiguration())

spotifyClient.login()
currently_playing_track = spotifyClient.get_currently_playing()

if currently_playing_track and currently_playing_track['is_playing']:
    album = currently_playing_track['item']['album']
    artists = currently_playing_track['item']['artists']

    message = messenger.create_message(album, artists)

    twitterClient.PostUpdate(message)
