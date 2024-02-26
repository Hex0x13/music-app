from flask import Flask, render_template, request, redirect, url_for
import validators


app = Flask(__name__)

# When user click download it will execute
@app.route("/submit", methods=['POST'])
def submit():
    # Get the input[type="url" name="link"] value
    link = request.form.get('link')

    # Check if link is a valid url, if not it will redirect to index.html
    if not validators.url(link) or link == '':
        return redirect(url_for('index'))
    return f'Submititted link: {link}'

# When user request for index.html, this is the response
@app.route("/")
def index():
    return  render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)