from apiclient.discovery import build
import pafy
import soundcloud
import re

nonowords = ['cover', 'live', 'mv', 'teaser', 'trailer', 'ver', 'collab', 'remix', 'vocal', 'remake', 'm - v', 'inst', 'full album', 'mr', 'video', 'mix', 'piano', 'acca']
nono_count = len(nonowords)

def getaudio(query):

    def scsearch(query):

        client_id = 'af6ef05f45065af007e4763a222c2619'
        client = soundcloud.Client(client_id=client_id)

        tracks = client.get('/tracks', limit=3, q=query)

        for track in tracks:
            title = track.title.lower()
            print(title)

            i = 0
            for nonoword in nonowords:
                res = re.search(nonoword, title)

                if res:
                    print('Found a nonoword ' + nonoword)
                    break
                else:
                    i += 1
                    if i == nono_count:
                        url = track.stream_url + '?client_id=' + client_id
                        return(url)

    def ytsearch(query):
        apikey = 'AIzaSyBWR_T6AAm9p6UCcTX56IsrZ5oxuuNMtpc'
        youtube = build('youtube', 'v3', developerKey=apikey)

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
        url = best.url

        return(url)

    sc = scsearch(query)

    if sc:
        return(sc)
    else:
        return(ytsearch(query))
