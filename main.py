# coding: utf-8
# [START app]
import logging
from flask import Flask
from Tweet import Tweet

app = Flask(__name__)

@app.route('/')
def test():
    return "App is working"

@app.route('/init')
def init():
    tweet = Tweet()
    tweet.listen()

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]

