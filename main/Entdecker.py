# -*- coding: utf-8 -*-
__author__ = 'Shinobu Jamella Hoshino, knochenflamme@gmail.com'

import chardet
import urlfetch_ps
import urllib_ps
import re
import random
import time
import urlparse

'''''''''''''''
抓正文及评论
'''''''''''''''

def ausfuehren(lib_or_fetch, artikelurl, SeiteQuelle, reg4nextpage, reg4text, reg4comment, vtext, comments):
    #无评论
    if len(reg4comment) == 0: pass
    #有评论
    else:
        cmt_tmp = re.findall(reg4comment, SeiteQuelle.replace(r'&#34;', r'"').replace('\\', ''))
        if len(cmt_tmp) != 0:
            #将评论变成一个字符串，不论评论的正则里有无分组
#            for i in cmt_tmp:
#                comments_tmp = ["".join(i) for i in cmt_tmp]
            comments_tmp = ["".join(i) for i in cmt_tmp]
            comments = "".join(comments_tmp)
        else:
            comments = '<br/><p style="color:#1890cd;font-size:25px;">No comments/gallery</p>'
#        print comments

    #无分页
    if len(reg4nextpage) == 0: pass
    #有分页
    else:
        #判断正文正则结果是否只有一组
        if isinstance(re.findall(reg4text, SeiteQuelle)[0], tuple) is False:
            while re.search(reg4nextpage, SeiteQuelle):
                artikelurl_temp = re.findall(reg4nextpage, SeiteQuelle)[0]

                if re.search(r'://', artikelurl_temp):
                    artikelurl = artikelurl_temp
                else:
                    artikelurl = urlparse.urljoin(artikelurl, artikelurl_temp)

                SeiteQuelle = lib_or_fetch(artikelurl)
                Content = re.findall(reg4text, SeiteQuelle)
                if len(Content) != 0:
                    vtext.append(Content[0])	#移除decode('utf-8')
                elif re.search(r'ERROR! QwQ', SeiteQuelle):
                    vtext.append('<span style="color:#ff0000;font-size:30px;">' + SeiteQuelle + '</span>')
                else:
                    vtext.append('<span style="color:#ff0000;font-size:30px;">Please check your regex</span>')
                time.sleep(float(random.sample(range(1, 6), 1)[0]))

        else:
            while re.search(reg4nextpage, SeiteQuelle):
                artikelurl_temp = re.findall(reg4nextpage, SeiteQuelle)[0]

                if re.search(r'://', artikelurl_temp):
                    artikelurl = artikelurl_temp
                else:
                    artikelurl = urlparse.urljoin(artikelurl, artikelurl_temp)

                SeiteQuelle = lib_or_fetch(artikelurl)
                Content = re.findall(reg4text, SeiteQuelle)
                if len(Content) != 0:
                    text_temp = Content
                    for e in txt_temp:
                        vtext.append("".join(e))	#移除decode('utf-8')
                elif re.search(r'ERROR! QwQ', SeiteQuelle):
                    vtext.append('<span style="color:#ff0000;font-size:30px;">' + SeiteQuelle + '</span>')
                else:
                    vtext.append('<span style="color:#ff0000;font-size:30px;">Please check your regex</span>')
                time.sleep(float(random.sample(range(1, 6), 1)[0]))


    return vtext, comments

