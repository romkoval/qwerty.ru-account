#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Roman Kovalev'

import grab
import sys

g = grab.Grab()
g.setup(debug=True)

BASE_URL="http://billing.qwerty.ru/pls/rac.q/!w3_p_main.showform"

def getServiceUnError(body):
    from lxml.html import fromstring
    # Дятлы, не выставили кодировку, придется парсить вручную. 
    # Но мы то знаем что там отстойный cp1251
    errtext = fromstring(body.decode('cp1251').lower()).xpath('//body/font/h1')
    if len(errtext) > 0:
        return errtext[0].text.encode('utf8')
    else:
        return None
    

def get_user_info(user, passwd):
    g.setup(post={'USERNAME': user, 'PASSWORD': passwd, 'IDENTIFICATION': 'CONTRACT', 'FORMNAME': 'QFRAME', 'button': 'Вход'})
    res = g.go(BASE_URL + '?CONFIG=CONTRACT')

    frame_url = g.xpath_list("//frame[@name='data']/@src")
    if len(frame_url) > 0:
        res = g.go(BASE_URL + frame_url[0])
        print g.xpath('//form/table[3]/tr[6]/td[2]').text.encode('utf8')
    else:
        alert_pos = res.body.find('alert ("')
        if alert_pos > 0:
            print >> sys.stderr, res.body[alert_pos + 8: res.body.find('"', alert_pos + 8) ].decode('cp1251').encode('utf8')
        else:
            errtext = getServiceUnError(res.body)
            print >> sys.stderr, errtext and errtext or 'unable to parse qwerty answer!'
        return False



def usage(appname):
    print >> sys.stderr, "Usage: %s 'username' 'password'" % appname
    return -1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit ( usage(sys.argv[0]) )
    get_user_info(sys.argv[1], sys.argv[2])

