# -*- coding: utf-8 -*-

"""
MOM.MMS WEBHOOK

"""

from flask import request, Flask, redirect, render_template, Response, jsonify, url_for
import requests
from firebase import firebase
import random
from os import environ
from keys import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# API & DB credentials
#from Keys import *

# SETUP BASIC LOGGING
import logging
import socket
import logging.handlers

class ContextFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = ContextFilter.hostname
    return True

log = logging.getLogger()
log.setLevel(logging.DEBUG)
lf = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(lf)
log.addHandler(ch)

"""
landing page / HTML / authorization routes

"""
### WEBHOOK
@app.route("/in", methods = ['POST'])
def signup():
    if request.method == 'POST':

        data = request.data
        log.debug( 'request: %s' % (data))

        # Check FB. If >= 99 entries, trigger email (should be a random msg) & clear FB
        if countRows() > 98:
            sendEmail()
            clearData()
            return 'EMAIL SENT & FB CLEARED'

        # Else, add a new row to FB
        else:
            addRow(data)
            return 'DATA PUSHED TO FB'
    else:
        return 'NOT A POST REQUEST'

### MAILGUN METHODS
def sendEmail():
  log.debug('sending email')
  r = requests.post(
    environ['MGDOM'],
    auth=("api", environ['MGKEY']),
    data={
      "from": "momMMS" + " <info@mom.mms>",
      "to": "Neal Shyam <nealrs@gmail.com>",
      "subject": 'We just texted your mom!',
      "text": "Hey mom, how are you?",
      # Copy should be chosen @ random from an array.
      "html": "<p>Hey mom, how are you?</p>" })

  if r.status_code == 200:
    log.info( 'MG API success, msg id: %s' % (r.json()['id']))

  else:
    log.debug('MG API error')

### FIREBASE METHODS
def countRows():
  fb = firebase.FirebaseApplication(environ['FB'], None)
  data = fb.get('/log', None)

  if data is None:
      log.debug('rows: 0')
      return 0
  else:
      log.debug('rows: %s' % (len(data)))
      return len(data)

def clearData():
  fb = firebase.FirebaseApplication(environ['FB'], None)
  fb.delete('/log', None)
  log.info('deleted all rows')

def addRow(data):
  fb = firebase.FirebaseApplication(environ['FB'], None)
  p = fb.post('/log', data)
  log.info('new row in FB: %s' % (p))

if __name__ == "__main__":
    app.run(debug=True)
