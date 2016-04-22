import soundcloud
import re

query = 'D (Half Moon) (feat. 개코) DEAN(딘)'

client_id = 'af6ef05f45065af007e4763a222c2619'
client = soundcloud.Client(client_id=client_id)

tracks = client.get('/tracks', q=query)

nonowords = ['cover', 'live', 'mv', 'teaser', 'trailer', 'ver', 'collab', 'remix', 'vocal', 'rap ver']
nono_count = len(nonowords)

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
                stream = track.stream_url + '?client_id=' + client_id
                print(stream)
