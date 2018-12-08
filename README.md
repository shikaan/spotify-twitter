Spotify-Twitter Bot
===

A bot which reads your currently playing song on Spotify, gets the its album 
and creates a tweet like

![Example](https://i.ibb.co/BjZWsGs/Screenshot-from-2018-12-08-15-05-59.png)

## Launch

```
pip3 install -r requirements.txt

python ./src/main.py
```

Make sure to have the environment correctly setup before you launch. Continue
reading for more details.

## Why?

Haven't you ever felt the need of sharing how wonderful is your life with 
others? Me neither, but apparently having a presence on social networks is 
part of our job.

## How?

Everytime you launch this application

```
python3 ./src/main.py
```

[SpotifyClient](./src/spotify.py) tries to login using the following 
environment variables `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, 
`SPOTIFY_REDIRECT_URI`. If you're wondering what those means maybe you should 
take a look [here](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow)

We are following the Authorization Code flow: so first thing we require an
authorization code and then we use that to get an `access_token` and a 
`refresh_token`. This info gets eventually stored in a file called 
`spotify_authentication.json` to save you some logins every now and then.

Yes, the procedure is a bit messed up because it was meant to happen on the
frontend. There is no way (so far!) to make this thing smoother, if you
think I am wrong you can prove it with a PR :D

The Twitter part is extremely more straightforward. We are using an 
[existing twitter client](https://github.com/bear/python-twitter) which 
performs the authentication just using the environment variables: 
`TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, 
`TWITTER_ACCESS_TOKEN_KEY`, `TWITTER_ACCESS_TOKEN_SECRET`.

The magic happens obviously in [`main.py`]('./src/main.py').

Other relevant actors:
- [`ConfigurationManager`](./src/main.py) reads the configuration 
  (only from env at the moment) and creates the configuration objects
  required by the clients
- [`Messenger`](./src/messenger.py) responsible of creating and
  formatting the message to be sent

## CI

If you're the uttermost lazy ass on the world, I have bad news for you: you
aren't, because I am. In [.circleci/config.yml](.circleci/config.yml) you can
find an example of how you can make this run on a schedule and post on Twitter
during business hours. 

## Future improvements

- Find a way to make SpotifyClient login in a smoother way (if Spotify will 
  ever allow me to do so)
- Connect to other social networks