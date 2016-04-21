from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import urllib.request
import re
import sys
import soundcloud
import youtube

def index(request):

    url = 'http://music.bugs.co.kr'
    con = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(con, 'html.parser')
    sel = '#CHARTrealtime > table > tbody > tr'
    songs = soup.select(sel)[0:100]

    titles = []
    thumbs = []
    thumbs_orig = []
    artists = []
    albums = []

    for song in songs:

        title = song.find('p', class_='title').find('a').string

        thumb_raw = song.find('a', class_='thumbnail').find('img')['src']
        thumb = re.sub(r'\/50\/', '/100/', thumb_raw)
        thumb_orig = re.sub(r'\/50\/', '/original/', thumb_raw)

        artist = song.find('p', class_='artist').find('a').string

        album = song.find('a', class_='album').string


        titles.append(title)
        thumbs.append(thumb)
        thumbs_orig.append(thumb_orig)
        artists.append(artist)
        albums.append(album)

    context = {'songs': zip(titles, thumbs, thumbs_orig, artists, albums)}

    return render(request, 'base/index.html', context)

def stream(request):

    if request.method == 'GET':
        artist = request.GET['artist']
        title = request.GET['title']

        client_id = 'af6ef05f45065af007e4763a222c2619'
        client = soundcloud.Client(client_id=client_id)

    tracks = client.get('/tracks', q=title + ' ' + artist)

    if tracks:
        sc_stream = tracks[0].stream_url
        sc_title = tracks[0].title
        stream = sc_stream + '?client_id=' + client_id
        stream = ''

    query = title + ' ' + artist + ' ' + 'audio'
    stream = youtube.getaudio(query)

    return HttpResponse(stream)

def search(request):

    if request.method == 'GET':
        query = request.GET['q']

    query = query.replace(' ', '%20')
    # need to url encode to work (for some reason)
    query = urllib.parse.quote(query)

    url = 'http://search.bugs.co.kr/track?q=' + query
    con = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(con, 'html.parser')
    sel = '#DEFAULT0 > table > tbody > tr'
    songs = soup.select(sel)[0:100]

    titles = []
    thumbs = []
    thumbs_orig = []
    artists = []
    albums = []

    for song in songs:

        title = song.find('p', class_='title').find('a').string

        thumb_raw = song.find('a', class_='thumbnail').find('img')['src']
        thumb = re.sub(r'\/50\/', '/100/', thumb_raw)
        thumb_orig = re.sub(r'\/50\/', '/original/', thumb_raw)

        artist = song.find('p', class_='artist').find('a')
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

    context = {'songs': zip(titles, thumbs, thumbs_orig, artists, albums)}

    return render(request, 'base/index.html', context)

def fresh(request):

    url = 'http://music.bugs.co.kr/newest'
    con = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(con, 'html.parser')
    sel = '#GENREtotalpicked > table > tbody > tr'
    songs = soup.select(sel)[0:100]

    titles = []
    thumbs = []
    thumbs_orig = []
    artists = []
    albums = []

    for song in songs:

        title = song.find('p', class_='title').find('a').string

        thumb_raw = song.find('a', class_='thumbnail').find('img')['src']
        thumb = re.sub(r'\/50\/', '/100/', thumb_raw)
        thumb_orig = re.sub(r'\/50\/', '/original/', thumb_raw)

        artist = song.find('p', class_='artist').find('a').string
        album = song.find('a', class_='album').string

        titles.append(title)
        thumbs.append(thumb)
        thumbs_orig.append(thumb_orig)
        artists.append(artist)
        albums.append(album)

    context = {'songs': zip(titles, thumbs, thumbs_orig, artists, albums)}

    return render(request, 'base/index.html', context)
