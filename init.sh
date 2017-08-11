#! /bin/bash

set -x

cd redmine_docker/backlogs
sh init.sh
docker-compose up -d --build
echo waiting remine starts

while true; do
    MATCH=$(docker-compose logs redmine | grep -m1 "WEBrick::HTTPServer#start")
    if [ -n "$MATCH" ]; then
       break
    fi
    sleep 10
done
  
echo wait until http request is accepted
for i in $(seq 1 100); do
    OUT=$(curl -I http://localhost:3001/redmine_backlogs/  | grep "HTTP/1.1 200 OK")
    if [ -n "$OUT" ]; then
        break
    fi
    sleep 10
done

cd ../..
python mechanize/load_default_setting.py
sh redmine_docker/backlogs/install.sh
python mechanize/config_task_tracker_workflow.py

cd redmine_docker/backlogs
docker-compose restart

while true; do
    MATCH=$(docker-compose logs redmine | tail | grep "Bundled gems are installed")
    if [ -n "$MATCH" ]; then
        break
    fi
    sleep 10
done

cd ../..

echo wait until http request is accepted after restart
for i in $(seq 1 100); do
    OUT=$(curl -I http://localhost:3001/redmine_backlogs/  | grep "HTTP/1.1 200 OK")
    if [ -n "$OUT" ]; then
        break
    fi
    sleep 10
done

python mechanize/add_task.py

