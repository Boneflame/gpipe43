# -*- coding: utf-8 -*-
__author__ = 'Shinobu Jamella Hoshino, knochenflamme@gmail.com'

import user_agents
import random
from StringIO import StringIO
import urllib2
import httplib
import gzip
import zlib
import chardet
import google

UA = random.choice(user_agents.user_agents)

def pagesource(URL):
    request = urllib2.Request(URL, headers = {'User-Agent': UA, 'Referer': URL, 'Accept-Encoding': 'gzip, deflate'})
    try:
        response = urllib2.urlopen(request, timeout=90)
#        response = requests.get(URL, headers = {'User-Agent': UA, 'Referer': URL}).content
        ContentEncoding = response.info().get('Content-Encoding')
        if ContentEncoding == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            result = f.read()
            f.close()
            return result
        elif ContentEncoding == 'deflate':
            return zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
        else:
            return response.read()

    except urllib2.HTTPError, e:
        return r'ERROR! QwQ<br/>' + str(e.code) + ' ' + str(e.reason)
    except urllib2.URLError, e:
        return r'ERROR! QwQ<br/>' + str(e.reason)
    except httplib.HTTPException, e:
        return r'ERROR! QwQ<br/>HTTPException: ' + str(e)
    except google.appengine.api.urlfetch_errors.DNSLookupFailedError, e:
        return r'ERROR! QwQ<br/>' + str(e)
    except google.appengine.api.urlfetch_errors.DeadlineExceededError, e:
        return r'ERROR! QwQ<br/>' + str(e)
    except google.appengine.runtime.apiproxy_errors.DeadlineExceededError, e:
        return r'ERROR! QwQ<br/>apiproxy_errors.' + str(e)
