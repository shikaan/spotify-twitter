from string import Template



from configuration import ConfigurationManager
from spotify import SpotifyClient
import twitter

configurationManager = ConfigurationManager()

spotifyClient = SpotifyClient(**configurationManager.getSpotifyConfiguration())
twitterClient = twitter.Api(**configurationManager.getTwitterConfiguration())

print('Login')
spotifyClient.login()

print('Currently playing')
currently_playing_track = spotifyClient.get_currently_playing()
message_template = Template('${album_name} by ${artists_names} ${album_url} #NowPlaying')

if currently_playing_track['is_playing']:
    album = currently_playing_track['item']['album']
    artists = currently_playing_track['item']['artists']

    album_url = album['external_urls']['spotify']
    album_name = album['name']

    artists_names = ", ".join(list(map(lambda artist: artist['name'], artists)))

    twitterClient.PostUpdate(message_template.substitute(album_url=album_url, album_name=album_name, artists_names=artists_names))
