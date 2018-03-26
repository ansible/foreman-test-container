#!/usr/bin/env python


# Create anything.foreman.yaml with this content ...
#plugin: foreman
#url: http://localhost:8080
#user: ansible-reader
#password: changeme
#validate_certs: False

# Start this script
# ./flaskapp.py

# Run ansible-inventory to test
# ansible-inventory -vvvv -i anything.foreman.yaml --list


import glob
import json

from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

PAGECACHE = {}

@app.before_first_request
def build_pagecache():
    jfiles = glob.glob('fixtures/*.json')
    for jfile in jfiles:
        with open(jfile, 'r') as f:
            jdata = json.loads(f.read())
        key = (jdata['url'], jdata['page'])
        PAGECACHE[key] = jdata


@app.route('/api/v2/hosts')
@app.route('/api/v2/hosts/<hostid>')
def get_hosts(hostid=None):
    # page number?
    pagenum = request.args.get('page')
    if pagenum:
        pagenum = int(pagenum)

    keys = PAGECACHE.keys()
    thiskey = None
    for key in keys:
        if key[-1] != pagenum:
            continue
        if hostid is None and key[0].endswith('/hosts'):
            thiskey = key
            break
        elif hostid and key[0].endswith('/hosts/%s' % hostid):
            thiskey = key
            break

    if not thiskey:
        import epdb; epdb.st()

    resp = PAGECACHE[thiskey]
    #import epdb; epdb.st()
    return jsonify(resp['data'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
