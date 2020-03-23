from subprocess import Popen, PIPE
import json

import requests
import bs4

config = {
	'genius_token': "",
	'genius_base_url': 'https://api.genius.com'
}

def exec_applescript(script):
	p = Popen(['osascript', '-e', script], stdout=PIPE).communicate()
	return json.loads(p[0])

def get_spotify_now_playing():
	spotify_now_playing_applescript = '''
tell application "System Events"
	set processList to (name of every process)
end tell
if (processList contains "Spotify") is true then
	tell application "Spotify"
		set artistName to artist of current track
		set trackName to name of current track
		set albumName to album of current track
		return "{" & "\\\"artist\\\": \\\"" & artistName & "\\\", " & "\\\"track\\\": \\\"" & trackName & "\\\", \\\"album\\\": \\\"" & albumName & "\\\"}"
	end tell
end if'''

	return exec_applescript(spotify_now_playing_applescript)

def request_genius_song_info(song_title, artist_name):
	genius_base_url = config['genius_base_url']
	headers = {'Authorization': 'Bearer ' + config['genius_token']}
	search_url = genius_base_url + '/search'
	data = {'q': song_title + ' ' + artist_name}
	response = requests.get(search_url, data=data, headers=headers)
	return response

def extract_genius_lyrics_angular(html):
	lyrics = html.find('div', class_='lyrics').get_text()
	return lyrics

def extract_genius_lyrics_react(html):
	lyric_elements = html.select('div[class*="Lyrics__Container"]')[0]
	lyrics = ""

	for elem in lyric_elements:
		if isinstance(elem, bs4.NavigableString):
			lyrics += elem
		elif elem.name == "br":
			lyrics += "\n"
		else:
			lyrics += elem.decode_contents().replace("<br/>", "\n")

	return lyrics

def scrape_genius_song_url(url):
	page = requests.get(url)
	html = bs4.BeautifulSoup(page.text, 'html.parser')

	if html.find('div', class_='lyrics') is not None:
		return extract_genius_lyrics_angular(html)
	else:
		return extract_genius_lyrics_react(html)

def get_lyrics_from_genius(song_title, artist_name):
	song_info = request_genius_song_info(song_title, artist_name).json()
	remote_song_info = None

	for hit in song_info['response']['hits']:
		if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
			remote_song_info = hit
			break

	# Extract lyrics from URL if song was found
	if remote_song_info:
		song_url = remote_song_info['result']['url']
		lyrics = scrape_genius_song_url(song_url).strip("\n")
		return lyrics

def print_spotify_now_playing_lyrics():
	info = get_spotify_now_playing()
	lyrics = get_lyrics_from_genius(info['track'], info['artist'])
	print()
	print(info['track'] + " by " + info['artist'] + " from album " + info["album"])
	print()
	print(lyrics)
	print()

print_spotify_now_playing_lyrics()

