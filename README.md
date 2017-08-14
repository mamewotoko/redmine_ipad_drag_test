redmine_ipad_drag_test [![Build Status](https://travis-ci.org/mamewotoko/redmine_ipad_drag_test.svg?branch=master)](https://travis-ci.org/mamewotoko/redmine_ipad_drag_test) [![Code Health](https://landscape.io/github/mamewotoko/redmine_ipad_drag_test/master/landscape.svg?style=flat)](https://landscape.io/github/mamewotoko/redmine_ipad_drag_test/master)
======================

Prepare
-------
* install dependencies
  * Mac

```
brew install selenium-server-standalone chromedriver
```

Run
---
* simple test

```
sh run.sh test.py
```

* parametrized test

```
sh run.sh param_test.py
```

List iOS Simulator
------------------

```
xcodebuild -showsdks
```

References
----------
* [HTMLTestRunner](http://tungwaiyip.info/software/HTMLTestRunner.html)
* [Python unit testing: parametrized test cases](http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases)

Keywords
--------
selenium, python, unittest. HTMLTestRunner, screenshot, mechanize

----
Takashi Masuyama < mamewotoko@gmail.com >  
http://mamewo.ddo.jp/
