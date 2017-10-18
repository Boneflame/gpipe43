import webapp2
import cloudstorage as gcs


def Speichern(prjname, bucket_name, subdir4bg, subdir4rss, rssname, result):
    bucket = bucket_name
    filename = '/' + bucket+ '/' + rssname + '.xml'
    class FeedSaver(webapp2.RequestHandler):
        def create_file(self, filename):
            gcs_file = gcs.open(filename, 'w', content_type='text/plain')
            gcs_file.write(result)
            gcs_file.close()
        def get(self):
            self.create_file(filename)
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write('<p>RSS ist erfolgreich erzeugt worden!</p><p>Klicken Sie auf <a href="%s">HIER</a></p>' % ('http://' + prjname + '.appspot.com/' + subdir4rss + '/' + rssname))
    return webapp2.WSGIApplication([('/' + subdir4bg + '/' + rssname, FeedSaver)], debug=True)


def Abrufen(bucket_name, subdir4rss, rssname):
    filename = '/' + bucket_name + '/' + rssname + '.xml'
    class RssGet(webapp2.RequestHandler):
        def read_file(self, filename):
            gcs_file = gcs.open(filename, 'r')
            self.response.write(gcs_file.read())
            gcs_file.close()
        def get(self):
            self.response.headers['Content-Type'] = 'text/xml'
            self.read_file(filename)
    return webapp2.WSGIApplication([('/' + subdir4rss + '/' + rssname, RssGet)], debug=True)


def FeedModi(subdir4bg, rssname, result):
    class MainPage(webapp2.RequestHandler):
        def get(self):
            self.response.headers['Content-Type'] = 'text/xml'
            self.response.out.write(result)
    return webapp2.WSGIApplication([('/' + subdir4rss + '/' + rssname, MainPage)], debug=True)


def HelloWorld(subdir4bg, rssname, result):
    class MainPage(webapp2.RequestHandler):
        def get(self):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write(result)
    return webapp2.WSGIApplication([('/' + subdir4bg + '/' + rssname, MainPage)], debug=True)

def Portal(prjname, subdir4bg, subdir4rss, rssname):
    class MainPage(webapp2.RequestHandler):
        def get(self):
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write('<a href="%s">HERE</a>' % ('http://' + prjname + '.appspot.com/' + subdir4rss + '/' + rssname))
    return webapp2.WSGIApplication([('/' + subdir4bg + '/' + rssname, MainPage)], debug=True)
