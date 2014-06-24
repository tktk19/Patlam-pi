from flask import Flask, render_template
from flask_bootstrap import Bootstrap
#import RPI.GPIO as GPIO

app = Flask(__name__)
Bootstrap(app)

@app.route('/')

def hello_world():
    link = ['http://google.com','http://yahoo.co.jp','http://facebook.com','http://mixi.jp']
    return render_template("index.html", urls = link)

if __name__ == '__main__':
    app.run()

