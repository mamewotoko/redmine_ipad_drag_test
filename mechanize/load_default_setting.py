
# -*- coding: utf-8 -*-
import mechanize
import sys
import config

def load_default_setting():
    br = mechanize.Browser()
    br.open(config.REDMINE_URL)

    br.follow_link(text="Sign in")
    br.select_form(nr=1)
    br['username'] = u'admin'
    br['password'] = u'admin'
    br.submit()

    br.follow_link(text="Administration")

    br.select_form(nr=1)
    # select language
    br.submit()
    return True

if __name__ == '__main__':
    if len(sys.argv) == 2:
        config.REDMINE_URL = sys.argv[1]
    load_default_setting()
