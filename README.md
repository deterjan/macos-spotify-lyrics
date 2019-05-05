# macos-spotify-lyrics

Short script to get the currently playing song from Spotify, scrape its lyrics from Genius and print the lyrics on your macOS terminal.

Note that the script only works on macOS because Applescript is used to communicate with Spotify.

Put your Genius API token in the field `genius_token` in the object `config` at the top of the script. [See here](https://docs.genius.com/) for details on getting an API token.

Genius API request and scraping code adapted from [lyrics-crawler](https://github.com/willamesoares/lyrics-crawler/blob/master/get-lyric.py) by willamesoares.
