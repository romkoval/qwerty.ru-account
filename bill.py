# -*- coding: utf-8 -*-

__author__ = 'roman'

import grab
import sys

g = grab.Grab()
g.setup(debug=True)

def get_user_info():
    g.setup(post={'USERNAME': '', 'PASSWORD': '', 'IDENTIFICATION': 'CONTRACT', 'FORMNAME': 'QFRAME', 'button': 'Вход'})
    res = g.go('http://billing.qwerty.ru/pls/rac.q/!w3_p_main.showform?CONFIG=CONTRACT')

    addr_pattern = '<FRAME name="data" SRC="'
    replace = res.body.find(addr_pattern)
    if replace >= 0:
        replace_end = res.body.find('"', replace + len(addr_pattern))
        redirect = res.body[replace + len(addr_pattern):replace_end]
        print >> sys.stderr, replace, replace_end, redirect
        res = g.go('http://billing.qwerty.ru/pls/rac.q/!w3_p_main.showform' + redirect)

        print >> sys.stderr, g.xpath('//form/table[3]/tr[6]/td[2]').text
    else:
        print >> sys.stderr, 'unable to parse qwerty answer!'
        return False

    print res.body



if __name__ == '__main__':
    get_user_info()

