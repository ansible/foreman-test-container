#! /usr/bin/env python
"""JSON fixtures sanitizer."""

import json
import random
import string
import sys

from mock import sentinel
from urllib.parse import urlparse


DEFAULT_FILE='fixtures/aHR0cHM6Ly9zYXQtcjIyMC0wMi5sYWIuZW5nLnJkdTIucmVkaGF0LmNvbS9hcGkvdjIvaG9zdHMmcGFnZT00.json'

contains_rh = lambda _: isinstance(_, str) and 'redhat.com' in _


class FqdnSanitizer:
    """JSON sanitizer, turns RH domains into safe-to-share data."""

    def __init__(self, filename=DEFAULT_FILE[:]):
        """Parse JSON file and prepare map for replacements cache."""
        self._orig_filename = filename
        with open(self._orig_filename) as j:
            self._orig_obj = json.load(j)
        self.sanity_map = {}

    def sanitize_dict(self, dct=sentinel):
        """Return sanitized data structure."""

        if dct is sentinel:
            dct = self._orig_obj.copy()

        if isinstance(dct, str):
            return self.sanitize_fqdn(dct)
        elif isinstance(dct, list):
            return [self.sanitize_dict(_) for _ in dct]
        elif not isinstance(dct, dict):
            return dct

        return {k: self.sanitize_dict(v) for k, v in dct.items()}

    def sanitize_fqdn(self, val):
        """Replace FQDN with a dummy one.

        Reuses same dummies for repeated domains.
        """
        orig_val = val
        if isinstance(val, str):
            val = val.strip()
            if ' ' in val or not contains_rh(val):
                return val
            if '//' not in val:
                val = '//' + val
            pr = urlparse(val)
            cur_fqdn = pr.netloc
            cur_port = pr.port
            if not cur_fqdn:
                return orig_val
            try:
                pr = pr._replace(netloc=self.sanity_map[cur_fqdn])
            except KeyError:
                hostport = [randomize_fqdn(cur_fqdn)]
                if cur_port:
                    hostport.append(cur_port)
                self.sanity_map[cur_fqdn] = ':'.join(hostport)
                pr = pr._replace(netloc=self.sanity_map[cur_fqdn])
            finally:
                val = pr.geturl()
                if not pr.scheme:
                    val = val[2:]
        return val

    def save(self):
        """Rewrite same JSON file with sanitized version."""
        with open(self._orig_filename, 'w') as j:
            json.dump(self.sanitize_dict(), j)


def randomize_fqdn(fqdn):
    """Generate a dummy FQDN in place of input one."""
    dots_count = fqdn.count('.')
    ending_base = f'example-{str(random.randint(0, 999)).rjust(3, "0")}'
    if dots_count == 0:
        return ending_base
    ending_base = f'{ending_base}.com'
    if dots_count == 1:
        return ending_base

    subdomains_needed = dots_count - 2
    for _ in range(subdomains_needed):
        ending_base = f'{random.choice(string.ascii_lowercase)}{random.randint(0, 9)}.{ending_base}'

    return ending_base


def main(args):
    """Entrypoint for sanitizing RH domains JSON files."""
    for arg in args:
        try:
            print(f'Processing {arg}...')
            FqdnSanitizer(arg).save()
        except json.decoder.JSONDecodeError:
            print('Failed to decode it. Skipping...')


__name__ == '__main__' and main(sys.argv[1:])
