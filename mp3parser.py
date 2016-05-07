from apiclient.discovery import build
import pafy
import soundcloud
import re
from bs4 import BeautifulSoup
import urllib.request

nonowords = ['cover', 'live', 'mv', 'teaser', 'trailer', 'ver', 'collab', 'remix', 'vocal', 'remake', 'm - v', 'inst', 'full album', 'mr', 'video', 'mix', 'piano', 'acca']
nono_count = len(nonowords)


def scsearch(artist, title):

    client_id = 'af6ef05f45065af007e4763a222c2619'
    client = soundcloud.Client(client_id=client_id)

    query = artist + ' ' + title
    tracks = client.get('/tracks', limit=3, q=query)
    title = title.lower()
    title = re.sub(r'\(.+\)', '', title)

    for track in tracks:
        sctitle = track.title.lower()
        print(sctitle)

        i = 0
        for nonoword in nonowords:
            nono = re.search(nonoword, sctitle)
            notitle = re.search(title, sctitle)

            if not notitle:
                print('Wrong song dude...')
                break
            elif nono:
                print('Found a nonoword: ' + nonoword)
                break
            else:
                i += 1
                if i == nono_count:
                    url = track.stream_url + '?client_id=' + client_id
                    return(url)

def ytsearch(artist, title):
    apikey = 'AIzaSyBWR_T6AAm9p6UCcTX56IsrZ5oxuuNMtpc'
    youtube = build('youtube', 'v3', developerKey=apikey)
    query = artist + ' ' + title

    query = query + ' audio'

    res = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            order='relevance'
            ).execute()

    video_id = res['items'][0]['id']['videoId']

    audio = pafy.new(video_id)
    best =  audio.getbestaudio()
    title = best.title
    url = best.url

    print(title)
    return(url)

def fssearch(artist, title):
    query = artist + ' ' + title
    query = urllib.parse.quote(query)
    url = 'http://search.4shared.com/q/CCAD/1/' + query
    sel = '#search_results > table > tbody > tr > td > table > tbody > tr'
    con = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(con, 'html.parser')
    try:
        raw_src = soup.find('div', class_='playThumb').find('img')['onclick']
        regex = re.search('http:.+preview\.mp3', raw_src)
        url = regex.group(0)
        return(url)
    except AttributeError:
        return False

def getaudio(artist, title):
    if fssearch(artist,title):
        print('source: 4shared')
        return fssearch(artist, title)
    elif scsearch(artist,title):
        print('source: Soundcloud')
        return scsearch(artist, title)
    elif ytsearch(artist,title):
        print('source: Youtube')
        return ytsearch(artist, title)
