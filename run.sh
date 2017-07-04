#! /bin/sh
PYTHONPATH=./libs/ParametrizedTestCase/:./libs/HTMLTestRunner:$PYTHONPATH xvfb-run --server-args="-screen 0 1024x768x8" python $@
