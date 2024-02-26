from flask import Flask, render_template, request, redirect, url_for
import validators
from dotenv import load_dotenv
import os

app = Flask(__name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

@app.route("/submit", methods=['POST'])
def submit():
    link = request.form.get('link')
    if not validators.url(link) or link == '':
        return redirect(url_for('index'))
    return f'Submititted link: {link}'


@app.route("/")
def index():
    return  render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)