#! /usr/bin/env python
# -*- coding: utf-8 -*-
import mechanize
import sys
import config


def config_task_tracker_workflow():
    br = mechanize.Browser()
    try:
        br.open(config.REDMINE_URL)
        #print(cont.read())
        #print("----------")
        br.follow_link(text="Sign in")
        #print(cont.read())
        br.select_form(nr=2)
        br['username'] = 'admin'
        br['password'] = 'admin'
        br.submit()

        # change password
        br.select_form(nr=2)
        br['password'] = 'admin'
        br['new_password'] = 'adminadmin'
        br['new_password_confirmation'] = 'adminadmin'
        br.submit()
        
        # load english default settings        
        cont = br.follow_link(text="Administration")
        br.select_form(nr=2)
        # default is english
        br.submit()

    except:
        print(br.response().read())
        

if __name__ == '__main__':
    if len(sys.argv) == 2:
        config.REDMINE_URL = sys.argv[1]

    config_task_tracker_workflow()
