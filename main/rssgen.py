# -*- coding: utf-8 -*-
__author__ = 'Shinobu Jamella Hoshino, https://github.com/Boneflame/gpipe43'

import urlfetch_ps, urllib_ps, Entdecker
from remove_control_characters import remove_control_characters
import chardet
import random
import re
import urlparse
import threading
import time
from lxml import etree
from lxml.etree import CDATA
from xml.sax.saxutils import unescape
ISOTIMEFORMAT = '%a, %e %b %Y %H:%M:%S %z'



'''''''''''''''''''''
Crawl from website(not from a feed) and generate RSS

'''''''''''''''''''''


#multi treading crawl
def run_itemgen_mt(lib_or_fetch, encoding, itemgen, x, artikelurllist, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage):
    for i in random.sample(range(0, x), x):
        artikelurl = artikelurllist[i]
        t = threading.Thread(target=itemgen, args=(lib_or_fetch, encoding, artikelurl, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage))
        t.start()
        t.join()
        time.sleep(float(random.sample(range(1, 6), 1)[0]))


#single treading crawl
def run_itemgen_st(lib_or_fetch, encoding, itemgen, x, artikelurllist, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage):
    for i in random.sample(range(0, x), x):
        artikelurl = artikelurllist[i]
        itemgen(lib_or_fetch, encoding, artikelurl, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage)
        time.sleep(float(random.sample(range(1, 6), 1)[0]))


#main part
def ausfuehren(lib_or_fetch, func, siteurl, reg4site, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage, Anzahl, *custom_para):
    if lib_or_fetch == 'use_urlfetch':
        lib_or_fetch = urlfetch_ps.pagesource
    else:
        lib_or_fetch = urllib_ps.pagesource

    page_source = lib_or_fetch(siteurl[0])
    try:
        encoding = chardet.detect(page_source)['encoding']
#        if len(custom_para) == 1:
#            encoding = custom_para[0]
#        else: pass
        page_source = page_source.decode(encoding)
    except UnicodeDecodeError:
        page_source = page_source.decode(encoding, 'ignore')
    except TypeError: pass

    pathlist = re.findall(reg4site, page_source)

    if len(pathlist) != 0:
        #限制抓取的文章数
        l0 = len(pathlist)
        if Anzahl == 0 or Anzahl >= l0: pass
        elif Anzahl < l0:
            pathlist = pathlist[0:Anzahl]

        lll = len(siteurl)
        if lll == 1: pass

        else:
            #先找出第一个siteurl里的文章地址，再找其余siteurl的
            siteurl.pop(0)
            lll = lll-1
            time.sleep(float(random.sample(range(4,10),1)[0]))
            for i in random.sample(siteurl,lll):
                mmm = re.findall(reg4site, lib_or_fetch(i))

                #限制抓取的文章数（siteurl有多组时）
                l1 = len(mmm)
                if Anzahl == 0 or Anzahl >= l1: pass
                elif Anzahl < l1:
                    mmm = mmm[0:Anzahl]

                for j in mmm:
                    pathlist.append(j)
                time.sleep(float(random.sample(range(4,10),1)[0]))

        #把相对路径转为绝对路径。有的网站不是所有文章的url都全部是相对或绝对路径，故全部都用urlprase处理一遍
        if re.search('[^0-9]', pathlist[0]):
#            if re.search(r'://', pathlist[0]):
#                artikelurllist = pathlist
#            else:
#                artikelurllist = [urlparse.urljoin(siteurl[0], path) for path in pathlist]
            artikelurllist = [urlparse.urljoin(siteurl[0], path) for path in pathlist]
	#如果有自定义的url(从js里获得url的id，通常是一串数字)转换函数，则调用它
        else:
            artikelurllist = custom_para[0](pathlist)


        #获得文章url后休息，以防被ban
        time.sleep(float(random.sample(range(4, 9), 1)[0]))

        #填入channel元素的属性
        f = open('main/Vorlage.xml')
        root = etree.XML(f.read(), etree.XMLParser(remove_blank_text=True))		#移除空白符，这样才可以pretty print
        f.close()
        rsschannel = root.xpath('//lastBuildDate')[0]

        if len(re.findall(re.compile('<meta[\S\s]+?<title>(.*?)\s*</title>', re.I), page_source)) != 0:
            root.xpath('/rss/channel/title')[0].text = CDATA(re.findall(re.compile('<meta[\S\s]+?<title>(.*?)\s*</title>', re.I), page_source)[0])
        elif len(re.findall(re.compile('<title>\s*(.*?)\s*</title>', re.I), page_source)) != 0:
            root.xpath('/rss/channel/title')[0].text = CDATA(re.findall('<title>\s*(.*?)\s*</title>', page_source)[0])
        elif isinstance(custom_para, tuple) is True:
            root.xpath('/rss/channel/title')[0].text = CDATA(custom_para[1])
        else:
            root.xpath('/rss/channel/title')[0].text = CDATA(siteurl[0])

        if len(re.findall(re.compile('<meta name="(?:description|keywords)" content="(.*?)"', re.I), page_source)) != 0:
            root.xpath('/rss/channel/description')[0].text = CDATA(re.findall(re.compile('<meta name="(?:description|keywords)" content="(.*?)"', re.I), page_source)[0])
        elif len(re.findall(re.compile('<meta content="(.{18,})" name="(?:description|keywords)"', re.I), page_source)) != 0:
            root.xpath('/rss/channel/description')[0].text = CDATA(re.findall(re.compile('<meta content="(.{18,})" name="(?:description|keywords)"', re.I), page_source)[0])
        elif len(re.findall(re.compile('<div class="profile_desc_value" title="(.*?)"', re.I), page_source)) != 0:		#wechat公众号
            root.xpath('/rss/channel/description')[0].text = CDATA(re.findall(re.compile('<div class="profile_desc_value" title="(.*?)"'), page_source)[0])
        elif len(re.findall(re.compile('<title>(.*?)</title>', re.I), page_source)) != 0:
            root.xpath('/rss/channel/description')[0].text = CDATA(re.findall(re.compile('<title>(.*?)</title>'), page_source)[0])
        elif isinstance(custom_para, tuple) is True:
            if len(custom_para) == 3:
                root.xpath('/rss/channel/description')[0].text = CDATA(custom_para[2])
            else: pass
        else:
            root.xpath('/rss/channel/description')[0].text = CDATA(siteurl[0])

        root.xpath('/rss/channel/link')[0].text = CDATA(siteurl[0])
        root.xpath('/rss/channel/lastBuildDate')[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

        def itemgen(lib_or_fetch, encoding, artikelurl, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage):
            global root
            #创建一个新的item
            rssitem = etree.Element('item')
            item_title = etree.SubElement(rssitem, 'title')
            item_link = etree.SubElement(rssitem, 'link')
            item_description = etree.SubElement(rssitem, 'description')
            item_pubDate = etree.SubElement(rssitem, 'pubDate')
            item_guid = etree.SubElement(rssitem, 'guid')
            item_link.text = artikelurl
            item_guid.text = artikelurl
            #填入各元素属性
            SeiteQuelle = lib_or_fetch(artikelurl)

            #若正则结果有分组，join成一个str
            if len(re.findall(reg4title, SeiteQuelle)) != 0:
                tmp_title = re.findall(reg4title, SeiteQuelle)[0]
                try:
                    item_title.text = CDATA("".join(tmp_title))
                except ValueError:
                    item_title.text = CDATA("".join(tmp_title).decode(encoding))
            elif re.search(r'ERROR! QwQ', SeiteQuelle):
                item_title.text = artikelurl
                item_description.text = SeiteQuelle
            else:
                item_title.text = 'No title, please check regex'

            if len(reg4pubdate) != 0:
                if len(re.findall(reg4pubdate, SeiteQuelle)) != 0:
                    tmp_pbdate = re.findall(reg4pubdate, SeiteQuelle)[0]
                    pubdate_temp = "".join(tmp_pbdate).replace('/', '-').replace('T', ' ').replace(r'&nbsp;', ' ').replace('年', '-').replace('月', '-').replace('日', '-')	#移除decode('utf-8')
                    pubdate_temp = re.sub('\.\d+', '', pubdate_temp)		#移除秒数后的小数
                    if re.match('\d{4}', pubdate_temp) == None:
                        item_pubDate.text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
                        vtext = []
                    elif re.match('[^0-9 :-\\\+]', pubdate_temp) != 0:
                        item_pubDate.text = re.sub(r'(\+\d{2}):(\d{2})', '', pubdate_temp)
                        vtext = []
                    else:
                        item_pubDate.text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
                        vtext = []
                        vtext.append('<span style="color:#ff0000;font-size:30px;">Please check pubDate regex</span><br/><br/>')
                else:
                    item_pubDate.text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
                    vtext = []
                    vtext.append('<span style="color:#ff0000;font-size:30px;">Please check pubDate regex</span><br/><br/>')
            else:
                item_pubDate.text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

            if len(re.findall(reg4text, SeiteQuelle)) != 0:
                #判断正文正则是否只有一组
                txt_tmp = re.findall(reg4text, SeiteQuelle)
                if isinstance(txt_tmp[0], tuple) is True:
#                    vtext = []				#放在填写时间的地方，若时间正则有错好加入提示
                    for g in txt_tmp:
                        vtext.append("".join(g))
                else:
                    vtext = [txt_tmp[0]]	#移除decode('utf-8')

                comments = ''
                Ergebnis = Entdecker.ausfuehren(lib_or_fetch, artikelurl, SeiteQuelle, reg4nextpage, reg4text, reg4comment, vtext, comments)

                if len(reg4comment) == 0:
                    try:
                        item_description.text = CDATA("".join(Ergebnis[0]))
                    except ValueError:
                        if len(custom_para) == 1:
                            item_description.text = CDATA(remove_control_characters("".join(Ergebnis[0]).decode(custom_para[0])))
                        else:
                            item_description.text = CDATA(remove_control_characters("".join(Ergebnis[0]).decode(encoding, 'replace')))
                else:
                    try:
                        item_description.text = CDATA("".join(Ergebnis[0]) + Ergebnis[1])
                    except ValueError:
                        if len(custom_para) == 1:
                            item_description.text = CDATA(remove_control_characters("".join(Ergebnis[0]).decode(custom_para[0]) + Ergebnis[1].decode(custom_para[0])))
                        else:
                            item_description.text = CDATA(remove_control_characters("".join(Ergebnis[0]).decode(encoding, 'replace') + Ergebnis[1].decode(encoding, 'replace')))

            elif re.search(r'ERROR! QwQ', SeiteQuelle): pass		#在title处已填description
            else:
                item_description.text = '<span style="color:#ff0000;font-size:30px;">Please check regex</span>'

            rsschannel.addnext(rssitem)

        if func == 'st':
            func = run_itemgen_st
        else:
            func = run_itemgen_mt

        l = len(artikelurllist)
        func(lib_or_fetch, encoding, itemgen, l, artikelurllist, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage)

        #判断时间格式并格式化
        l = len(root.xpath('//pubDate'))+1
        for Nummer in range(1, l):
            zeit = root.xpath('//item[$i]/pubDate', i = Nummer)[0].text
            if re.match('\D{3}', zeit): pass
            elif re.search('\d{2}:\d{2}:\d{2}', zeit):
                root.xpath('//item[$i]/pubDate', i = Nummer)[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.mktime(time.strptime(zeit, '%Y-%m-%d %H:%M:%S'))))
            elif re.search('\d{2}:\d{2}', zeit):
                root.xpath('//item[$i]/pubDate', i = Nummer)[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.mktime(time.strptime(zeit, '%Y-%m-%d %H:%M'))))
            else:
                try:
                    root.xpath('//item[$i]/pubDate', i = Nummer)[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.mktime(time.strptime(zeit, '%Y-%m-%d'))))
                except ValueError:
                    root.xpath('//item[$i]/pubDate', i = Nummer)[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.mktime(time.strptime(zeit, '%m-%d-%Y'))))
                except ValueError:
                    root.xpath('//item[$i]/pubDate', i = Nummer)[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.mktime(time.strptime(zeit, '%d-%m-%Y'))))

        return re.sub(r'(<|&#60;|&lt;)(/|)(body|html)(>|&#62;|&gt;)', '', unescape(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')))

    #打不开网页、reg4site失效时返回错误
    else:
        f = open('main/Vorlage_Error.xml')
        root = etree.XML(f.read(), etree.XMLParser(remove_blank_text=True))
        f.close()
        root.xpath('/rss/channel/title')[0].text = siteurl[0]
        root.xpath('/rss/channel/link')[0].text = siteurl[0]
        root.xpath('/rss/channel/description')[0].text = siteurl[0]
        root.xpath('/rss/channel/lastBuildDate')[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

        root.xpath('//item[1]/description')[0].text = page_source
        root.xpath('//item[1]/link')[0].text = siteurl[0]
        root.xpath('//item[1]/guid')[0].text = siteurl[0]
        root.xpath('//item[1]/pubDate')[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
        return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
