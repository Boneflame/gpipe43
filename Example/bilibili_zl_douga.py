# -*- coding: utf-8 -*-
from main import feed_fulltext, rssgen
import config
import re
import webapp2
import cloudstorage as gcs


''''''''''''''''''
'''config start'''
''''''''''''''''''

rssname = 'bilibili_zl_douga'
siteurl = ['https://www.bilibili.com/read/douga?from=articleDetail']
reg4site = '<a title=".*?href="(.*?)"'
reg4title = '<title>(.*?)</title>'	
reg4pubdate = ''	#no date info in article's page source
reg4text = '<div class="article-holder">[\S\s]+?<p class="authority">'
reg4comment = ''
reg4nextpage = ''
Anzahl = 10


def filter():
    result = rssgen.ausfuehren('use_urllib', 'mt', siteurl, reg4site, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage, Anzahl)
    result = re.sub('<div.*?>', '', result).replace('</div>', '')
    return result

''''''''''''''''''
''' config end '''
''''''''''''''''''

bucket = config.bucket_name
filename = '/' + bucket + '/' + rssname + '.xml'
class FeedSaver(webapp2.RequestHandler):
    bucket = config.bucket_name
    filename = '/' + bucket + '/' + rssname + '.xml'
    def create_file(self, filename):
        gcs_file = gcs.open(filename, 'w', content_type='text/plain')
        gcs_file.write(filter())
        gcs_file.close()
    def get(self):
        self.create_file(filename)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<p>RSS is sucessfully generated!</p><p>Click <a href="%s">HERE</a></p>' % ('http://' + config.prjname + '.appspot.com/' + config.subdir4rss + '/' + rssname))
app = webapp2.WSGIApplication([('/' + config.subdir4bg + '/' + rssname, FeedSaver)], debug=True)
