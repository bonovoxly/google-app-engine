# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# As you can see above, this was created based around the Google Python example
#   for Google Analytics - https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/analytics


import logging
import os

from flask import Flask, request, render_template
import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)

# Environment variables are defined in app.yaml.
GA_TRACKING_ID = os.environ['GA_TRACKING_ID']
SITE_HOSTNAME = os.environ['SITE_HOSTNAME']


# [START track_event]
# haven't found a use for this yet;  this was in the example.  I'll dig into this later...
def track_event(category, action, label=None, value=0):
    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': '555',
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
    }
    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)
    # If the request fails, this will raise a RequestException. Depending
    # on your application's needs, this may be a non-error and can be caught
    # by the caller.
    response.raise_for_status()
# [END track_event]

# [START track_page]
# https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide#page
def track_page(page, title=''):
    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': '555',
        't': 'pageview',  # Pageview hit type.
        'dh': SITE_HOSTNAME,  # Document hostname
        'dp': page,  # Page.
        'dt': title,  # Title.
    }
    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)
    # If the request fails, this will raise a RequestException. Depending
    # on your application's needs, this may be a non-error and can be caught
    # by the caller.
    response.raise_for_status()
# [END track_page]

# routing for index
@app.route('/')
def static_index():
    track_page(page='/index.html')
    return app.send_static_file('index.html')
# routing for all other paths
@app.route('/<path:path>')
def static_proxy(path):
    track_page(page=path)
    return app.send_static_file(path + '/index.html')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
