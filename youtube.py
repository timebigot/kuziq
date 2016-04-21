from apiclient.discovery import build
import pafy

def getaudio(query):
    apikey = 'AIzaSyBWR_T6AAm9p6UCcTX56IsrZ5oxuuNMtpc'
    youtube = build('youtube', 'v3', developerKey=apikey)

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
