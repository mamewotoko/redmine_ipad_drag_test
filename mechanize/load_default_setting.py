
# -*- coding: utf-8 -*-
import mechanize
import sys

def load_default_setting():
    br = mechanize.Browser()
    br.open("http://localhost:3001/redmine_backlogs/")

    br.follow_link(text="Sign in")
    br.select_form(nr=1)
    br['username'] = 'admin'
    br['password'] = 'admin'
    br.submit()

    br.follow_link(text="Administration")

    br.select_form(nr=1)
    # select language
    br.submit()
    return True


if __name__ == '__main__':
    load_default_setting()
    
    
