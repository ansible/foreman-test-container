#!/usr/bin/env python3

"""Foreman API v2 stub server."""

import glob
import json
import os

from collections import defaultdict
from urllib.parse import urlparse

from flask import Flask, abort, jsonify, request


DEBUG = os.getenv('DEBUG', 'false').lower() not in ('false', '0', '', 'off')

app = Flask(__name__)  # pylint: disable=invalid-name

PAGECACHE = defaultdict(dict)


@app.before_first_request
def build_pagecache():
    """Read JSON fixtures into in-memory cache."""
    jfiles = glob.glob('fixtures/*.json')
    for jfile in jfiles:
        with open(jfile, 'r') as fixture:
            jdata = json.load(fixture)
        key = urlparse(jdata['url']).path[7:]
        subkey = jdata['page']
        PAGECACHE[key][subkey] = jdata['data']

        if 'id' in jdata['data'] and key == f"/hosts/{jdata['data']['id']}":
            PAGECACHE[f"/hosts/{jdata['data']['name']}"][subkey] = jdata['data']


def get_page_num():
    """Return page number."""
    return int(request.args.get('page') or 1)


def get_per_page():
    """Return the number of results per page."""
    return int(request.args.get('per_page') or 20)


def find_host(hostid):
    """Find a single host by its hostid, which is a numeric ID or a hostname"""
    try:
        return PAGECACHE[f'/hosts/{hostid}'][1]
    except KeyError:
        abort(404)


@app.route('/api/v2/hosts')
def get_hosts():
    """Render fixture contents from cache."""
    pagenum = get_page_num()
    resp = PAGECACHE['/hosts'][pagenum]
    return jsonify(resp)


@app.route('/api/v2/hosts/facts', methods=['POST'])
def handle_facts():
    """Create facts for hosts"""
    data = request.get_json()

    # Foreman can allow creating hosts that don't exist - we don't support this
    host = find_host(data['name'])

    if data['facts']['_type'] == 'ansible':
        host['facts'] = data['facts']['ansible_facts']
    else:
        abort(400)

    return jsonify(host), 201


@app.route('/api/v2/hosts/<hostid>')
def get_host(hostid):
    """Render fixture contents from cache."""
    return jsonify(find_host(hostid))


@app.route('/api/v2/hosts/<hostid>/facts')
def get_facts(hostid):
    """Return the facts for a single host"""
    host = find_host(hostid)

    page = get_page_num()
    per_page = get_per_page()

    start = (page - 1) * per_page
    end = page * per_page

    resp = {
        'total': len(host['facts']),
        'subtotal': 1,  # this appears to always be 1 in the API
        'page': page,
        'per_page': per_page,
        'sort': {
            'by': None,
            'order': None,
        },
        'results': {
            host['name']: dict(sorted(host['facts'].items())[start:end]),
        },
    }

    return jsonify(resp)


@app.route('/ping')
@app.route('/heartbeat')
def ping_heartbeat():
    return jsonify({"status": "ok", "response": "pong"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')), threaded=True, debug=DEBUG)
