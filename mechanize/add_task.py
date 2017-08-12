
# -*- coding: utf-8 -*-
import mechanize
import sys
import config

def add_project():
    br = mechanize.Browser()
    br.open(config.REDMINE_URL)

    br.follow_link(text="Sign in")
    br.select_form(nr=1)
    br['username'] = 'admin'
    br['password'] = 'admin'
    br.submit()

    br.follow_link(text="Projects")
    br.follow_link(text="New project")

    br.select_form(nr=1)
    br.set_value("test project", id="project_name")
    br.set_value("test_project", id="project_identifier")

    br.form.find_control(type="checkbox", name='project[enabled_module_names][]').get('backlogs').selected = True
    br.submit()

def add_task():
    br = mechanize.Browser()
    br.open(config.REDMINE_URL)

    br.follow_link(text="Sign in")
    br.select_form(nr=1)
    br['username'] = 'admin'
    br['password'] = 'admin'
    br.submit()

    br.follow_link(text="test project")
    br.follow_link(text="New issue")
    br.select_form(nr=1)
    br.set_value("test", id="issue_subject")
    br.submit()
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        config.REDMINE_URL = sys.argv[1]
    add_project()
    add_task()
