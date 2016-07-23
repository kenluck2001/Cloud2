import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
from flask import Flask, request, Response, render_template
from extra import  ProcessQueue #provide function required in the event stream
import requests


gevent.monkey.patch_all()
CDELAY = 1  #1 seconds


app = Flask(__name__)


def event_messages():
    try:
        qObject = ProcessQueue() #queue object
        while True:
            gevent.sleep(CDELAY)
            yield qObject.getFullMessage()  + "\n"
    except GeneratorExit: # Or maybe use flask signals
        pass


@app.route('/messages')
def messages():
    return Response( event_messages(), mimetype='text/event-stream' )



def event_index():
    try:
        qObject = ProcessQueue() #queue object
        while True:
            gevent.sleep(CDELAY)
            yield qObject.getMeta() + "\n"   
    except GeneratorExit: # Or maybe use flask signals
        pass



@app.route('/')
def index():
    return Response( event_index(), mimetype='text/event-stream' )

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8001), app)
    http_server.serve_forever()

