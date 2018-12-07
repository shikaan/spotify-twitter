import twitter
from configuration import ConfigurationManager
from spotify import SpotifyClient
from messenger import Messenger

configurationManager = ConfigurationManager()
messenger = Messenger()
spotifyClient = SpotifyClient(**configurationManager.getSpotifyConfiguration())
twitterClient = twitter.Api(**configurationManager.getTwitterConfiguration())

print('[Spotify] - Login')
spotifyClient.login()
print('[Spotify] - Login SUCCESS')

print('[Spotify] - Get Currently Playing')
currently_playing_track = spotifyClient.get_currently_playing()
print('[Spotify] - Get Currently Playing SUCCESS')

if currently_playing_track and currently_playing_track['is_playing']:
    album = currently_playing_track['item']['album']
    artists = currently_playing_track['item']['artists']

    message = messenger.create_message(album, artists)

    print('[Twitter] - Post message')
    twitterClient.PostUpdate(message)
    print('[Twitter] - Post message SUCCESS')
