
# -*- coding: utf-8 -*-
import mechanize
import sys
import config

def config_task_tracker_workflow():
    br = mechanize.Browser()
    br.open(config.REDMINE_URL)

    br.follow_link(text="Sign in")
    br.select_form(nr=1)
    br['username'] = 'admin'
    br['password'] = 'admin'
    br.submit()

    br.follow_link(text="Administration")

    # br.select_form(nr=1)
    # # select language
    # br.submit()
    # return True
    br.follow_link(text="Trackers")

    br.follow_link(text="Edit")

    br.select_form(nr=1)
    br.submit()

    br.select_form(nr=2)

    br.form.find_control(type="checkbox", name="transitions[1][1][always]").items[0].selected = True
    br.form.find_control(type="checkbox", name="transitions[1][2][always]").items[0].selected = True
    br.form.find_control(type="checkbox", name="transitions[1][5][always]").items[0].selected = True

    br.form.find_control(type="checkbox", name="transitions[2][1][always]").items[0].selected = True
    br.form.find_control(type="checkbox", name="transitions[2][2][always]").items[0].selected = True
    br.form.find_control(type="checkbox", name="transitions[2][5][always]").items[0].selected = True

    br.form.find_control(type="checkbox", name="transitions[5][1][always]").items[0].selected = True
    br.form.find_control(type="checkbox", name="transitions[5][2][always]").items[0].selected = True
    br.form.find_control(type="checkbox", name="transitions[5][5][always]").items[0].selected = True
    
    br.submit()
    
#    print(br.response().read())    

if __name__ == '__main__':
    if len(sys.argv) == 2:
        config.REDMINE_URL = sys.argv[1]
    
    config_task_tracker_workflow()
