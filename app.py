from flask import Flask, request
from flask import render_template, redirect, url_for
import validators, json
from spotify_api import SpotifyAPI


app = Flask(__name__)
spotify_api = SpotifyAPI()


# When user click "download" it will execute
@app.route("/submit", methods=['POST'])
def submit():
    if request.method != 'POST':
        return redirect(url_for("index"))
    # Get the input[type="url" name="link"] value
    link = request.form.get('link')

    # Check if link is a valid url, if not it will redirect to index.html
    if not validators.url(link) or link == '':
        return redirect(url_for('index'))
    playlist_id = link.split("/")[-1]
    playlist = spotify_api.get_playlists(playlist_id)
    with open("observe.json", "w") as file:
        json.dump(playlist, file)
    return render_template('response.html', playlist=playlist)

# When user request for index.html, this is the response
@app.route("/")
def index():
    return  render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)