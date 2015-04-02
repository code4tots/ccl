"""http.py for making http requests in ccl.
"""

import contextlib
import urllib

try:
  from urllib import request as urllib2
except ImportError:
  import urllib2


def Get(url):
  with contextlib.closing(urllib2.urlopen(url)) as f:
    return f.read()


def Post(url, values):
  data = urllib.urlencode(values)
  request = urllib2.Request(url, data)
  with contextlib.closing(urllib2.urlopen(request)) as f:
    return f.read()


def Load():
  return {
      'get': Get,
      'post': Post,
  }
