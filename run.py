from flask import Flask, render_template, request
import mp3parser
import urlparser
import urllib

app = Flask(__name__)

@app.route("/")
def index():
    url = 'http://music.bugs.co.kr'
    sel = '#CHARTrealtime > table > tbody > tr'
    songs = urlparser.bugs(url, sel)

    return render_template('index.html', songs=songs)

@app.route("/fresh")
def fresh():
    url = 'http://music.bugs.co.kr/newest'
    sel = '#GENREtotalpicked > table > tbody > tr'
    songs = urlparser.bugs(url, sel)

    return render_template('index.html', songs=songs)

@app.route("/search")
def search():
    query = request.args.get('q')
    print(query)
    query = urllib.parse.quote(query)

    url = 'http://search.bugs.co.kr/track?q=' + query
    sel = '#DEFAULT0 > table > tbody > tr'
    songs = urlparser.bugs(url, sel)

    return render_template('index.html', songs=songs)

@app.route("/stream")
def stream():
    title = request.args.get('title')
    artist = request.args.get('artist')

    stream = mp3parser.getaudio(title, artist)

    return stream

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
