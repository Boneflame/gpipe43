gpipe43 is a full text RSS generator which can hosted on Google App Engine. Use Regex to search and format full text from a article, or any other content that you want.<br>
Inspired by Yahoo Pipes and Feed43.<br>
Yahoo Pipe RIP.

Feature
===
* Support multi page.
* Display all images of article's gallery.
* Appending article's comment is possible.

Prepare
====
* [Create a new Cloud Platform project and App Engine application](https://cloud.google.com/appengine/docs/standard/python/quickstart)
* [Create a bucket in google cloud storage](https://cloud.google.com/storage/docs/quickstart-console)
* [Install Google Cloud SDK Python](https://cloud.google.com/sdk/docs/)

Simple quickstart
====
### Edit /main/user_agents.py
* add UA
### Edit config.py
* `prjname`: Name of your project on app engine
* `bucket_name`: Name of bucket
* `subdir4bg`: The crawler working under: http://[prjname].appspot.com/[subdir4bg]/[rssname]
* `subdir4rss`: This is your RSS site: http://[prjname].appspot.com/[subdir4rss]/[rssname]
### Edit example.py，replace 'example' to your own RSS's name
* `rssname`: RSS's name.
* `siteurl`: The website or a RSS feed that you want to generat fulltext RSS.
* `reg4site`: Regex that can find articles' URL. Leave a blank if siteurl is a feed.
* `reg4title`: Regex for title of a article. Leave a blank if siteurl is a feed.
* `reg4pubdate`: Regex for publish date of a article. Leave a blank if siteurl is a feed. The format of pubdate must contain '%Y-%m-%d', otherwise leave a blank.
* `reg4text`: Regex for main body of a article.
* `reg4comment`: Regex for comment. Not necessary, can leave it blank. You can also use this Regex to find all the image of a gallery in the article.
* `reg4nextpage`: Regex for article's next page if there's more than one page.
* `Anzahl`: How much article will be generated. If there's not only one siteurl, this limit for EVERY SINGLE siteurl instead of for all articleurl from all siteurl. 0 = no limit.<br><br>
* `rssgen.ausfuehren('use_urllib/use_urlfetch', 'st/mt', siteurl, reg4site, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage, Anzahl)`: Generat a RSS from a website.
* `feed_fulltext.ausfuehren('use_urllib/use_urlfetch', siteurl, reg4nextpage, reg4text, reg4comment, Anzahl, rssname)`: Use this to generat fulltext from a RSS feed.
	* `use_urllib`: Use urllib2，with UA
	* `use_urlfetch`: Use urlfetch，no UA
	* `mt`: Multi threading
	* `st`: Single threading


### Edit feed_list.py
* Replace 'example' to your own RSS's name

### app.yaml, cron.yaml
* Replace subdir4bg, subdir4rss, example to your own.<br>
See official guide: [app.yaml Reference](https://cloud.google.com/appengine/docs/standard/python/config/appref), [Scheduling Tasks With Cron for Python](https://cloud.google.com/appengine/docs/standard/python/config/cron)

### Optional
* Edit ./main/Vorlage.xml and Vorlage_Error.xml, you can fill the properties of elements 'generator', 'webMaster' and 'copyright'.

Test
====
    dev_appserver.py [PATH_TO_YOUR_APP]/app.yaml
Start the crawler: http://localhost:8080/[subdir4bg]/[rssname]<br>
When done, here to check your RSS: http://localhost:8080/[subdir4rssg]/[rssname]

See official guide: [Using the Local Development Server](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)

Upload to app engine
====
* cd to the directory of your project
>gcloud config set project PROJECT_NAME<br>
>gcloud app deploy app.yaml cron.yaml --version=VERSION_NUMBER<br>

See official guide: [Deploying a Python App](https://cloud.google.com/appengine/docs/standard/python/tools/uploadinganapp)


Some Examples
====
* [Autoblog](http://misaka19003.appspot.com/feed/autoblog)
* [Auto Motor und Sport](http://misaka19003.appspot.com/feed/ams)
* [Engadget中文版](http://misaka19002.appspot.com/feed/engadgetcn)
* [游民星空|单机游戏](http://misaka19002.appspot.com/feed/gamersky_pcgame)
* [Acfun文章区|动漫文化](http://misaka19002.appspot.com/feed/acfun)
