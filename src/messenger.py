from string import Template

class Messenger:
    def __init__(self):
        self.message_template = Template('${album_name} by ${artists_names} ${album_url} #NowPlaying')

    def create_message(self, album, artists):
        album_url = album['external_urls']['spotify']
        album_name = album['name']

        artists_names = ", ".join(list(map(lambda artist: artist['name'], artists)))

        return self.message_template.substitute(album_url=album_url, album_name=album_name, artists_names=artists_names)