# -*- coding: utf-8 -*-
__author__ = 'Shinobu Jamella Hoshino, knochenflamme@gmail.com'

from google.appengine.api import urlfetch
import google
import httplib
import chardet

#urlfetch.set_default_fetch_deadline(180)

def pagesource(URL):
    try:
        result = urlfetch.fetch(URL, headers = {'Referer': URL}, deadline = 60).content
        return result
    except httplib.HTTPException, e:
        return r'ERROR! QwQ<br/>HTTPException: ' + str(e.reason)
    except google.appengine.api.urlfetch_errors.DNSLookupFailedError, e:
        return r'ERROR! QwQ<br/>' + str(e)
    except google.appengine.api.urlfetch_errors.DeadlineExceededError, e:
        return r'ERROR! QwQ<br/>' + str(e)
    except google.appengine.runtime.apiproxy_errors.DeadlineExceededError, e:
        return r'ERROR! QwQ<br/>apiproxy_errors.' + str(e)
