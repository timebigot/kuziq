from bs4 import BeautifulSoup
import urllib.request
import re
import soundcloud
import mp3parser

def bugs(url, sel):

    con = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(con, 'html.parser')
    songs = soup.select(sel)[0:100]

    titles = []
    thumbs = []
    thumbs_orig = []
    artists = []
    albums = []

    for song in songs:

        title = song.find('p', class_='title').find('a')
        # temp patch: some values come up as empty aka notype
        if not title:
            title = 'Unknown'
        else:
            title = title.string

        thumb_raw = song.find('a', class_='thumbnail').find('img')['src']
        thumb = re.sub(r'\/50\/', '/100/', thumb_raw)
        thumb_orig = re.sub(r'\/50\/', '/original/', thumb_raw)

        artist = song.find('p', class_='artist').find('a').string
        # temp patch: some values come up as empty aka notype
        if not artist:
            artist = 'Unknown'
        else:
            artist = artist.string

        album = song.find('a', class_='album').string

        titles.append(title)
        thumbs.append(thumb)
        thumbs_orig.append(thumb_orig)
        artists.append(artist)
        albums.append(album)

    title = titles
    thumb = thumbs
    thumb_orig = thumbs_orig
    artist = artists
    album = albums

    songs = zip(title, thumb, thumb_orig, artist, album)
    return songs
