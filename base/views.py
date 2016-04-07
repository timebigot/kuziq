from django.shortcuts import render

from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import soundcloud

def index(request):
    test = 'https://api.soundcloud.com/tracks/257808741/stream?client_id=af6ef05f45065af007e4763a222c2619'
    url = 'http://music.bugs.co.kr'
    con = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(con, 'html.parser')
    sel = '#CHARTrealtime > table > tbody > tr'
    songs = soup.select(sel)[0:1]

    client = soundcloud.Client(client_id='af6ef05f45065af007e4763a222c2619')
    url_id = '?client_id=af6ef05f45065af007e4763a222c2619'

    titles = []
    thumbs = []
    thumbs_orig = []
    artists = []
    albums = []
    streams = []
    dl_links = []
    
    for song in songs:
        
        title = song.find('p', class_='title').find('a').string

        thumb_raw = song.find('a', class_='thumbnail').find('img')['src']
        thumb = re.sub(r'\/50\/', '/100/', thumb_raw)
        thumb_orig = re.sub(r'\/50\/', '/original/', thumb_raw)

        artist = song.find('p', class_='artist').find('a').string
        
        album = song.find('a', class_='album').string
        
        tracks = client.get('/tracks', q=title + ' ' + artist)
        
        if tracks:
            sc_stream = tracks[0].stream_url
            sc_title = tracks[0].title
            stream = sc_stream + url_id
        else:
            stream = 'ERROR'
            
        res = urllib.request.urlopen(stream)
        dl_link = res.geturl()
        
        titles.append(title)
        thumbs.append(thumb)
        thumbs_orig.append(thumb_orig)
        artists.append(artist)
        albums.append(album)
        streams.append(stream)
        dl_links.append(dl_link)
        
    context = {'songs': zip(titles, thumbs, thumbs_orig, artists, albums, streams, dl_links)}
    
    return render(request, 'base/index.html', context)
    