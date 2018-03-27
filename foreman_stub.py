#!/usr/bin/env python

"""Foreman API v2 stub server.

Create anything.foreman.yaml with this contents::

    plugin: foreman
    url: http://localhost:8080
    user: ansible-reader
    password: changeme
    validate_certs: False

Start this script::

    $ ./flaskapp.py

Run ansible-inventory to test::

    $ ansible-inventory -vvvv -i anything.foreman.yaml --list

"""

import glob
import json
import os

from collections import defaultdict
from urllib.parse import urlparse

from flask import Flask, jsonify, request


DEBUG = os.getenv('DEBUG', 'false').lower() not in ('false', '0', '', 'off')

if DEBUG:
    import pip
    pip.main(['install', 'q', 'epdb'])

app = Flask(__name__)

PAGECACHE = defaultdict(dict)


@app.before_first_request
def build_pagecache():
    """Read JSON fixtures into in-memory cache."""
    jfiles = glob.glob('fixtures/*.json')
    for jfile in jfiles:
        with open(jfile, 'r') as f:
            jdata = json.load(f)
        key = urlparse(jdata['url']).path[7:]
        subkey = jdata['page']
        PAGECACHE[key][subkey] = jdata['data']


def get_page_num():
    """Return page number if present."""
    pagenum = request.args.get('page')
    if pagenum:
        pagenum = int(pagenum)
    return pagenum


@app.route('/api/v2/hosts')
@app.route('/api/v2/hosts/<hostid>')
def get_hosts(hostid=None):
    """Render fixture contents from cache."""
    pagenum = get_page_num()

    cache_key = '/hosts'
    if hostid is not None:
        cache_key = f'{cache_key}/{hostid}'

    try:
        resp = PAGECACHE[cache_key][pagenum]
    except KeyError:
        if DEBUG:
            import q; q/cache_key; q/pagenum; q/hostid
            import epdb; epdb.st()
    else:
        return jsonify(resp)


__name__ == '__main__' and app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)), debug=DEBUG)
