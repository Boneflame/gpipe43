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
        return r'ERROR! QwQ<br/>HTTPException'
    except google.appengine.runtime.DeadlineExceededError:
        return r'ERROR! QwQ<br/>DeadlineExceededError'
    except google.appengine.runtime.apiproxy_errors.DeadlineExceededError:
        return r'ERROR! QwQ<br/>apiproxy_errors.DeadlineExceededError'
    except google.appengine.api.urlfetch_errors.DeadlineExceededError:
        return r'ERROR! QwQ<br/>urlfetch_errors.DeadlineExceededError'
