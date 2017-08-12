#! /bin/bash

set -x
set -e

. config.env

# build tester
docker-compose build

cd redmine_docker/backlogs
sh init.sh
docker-compose up -d --build
echo waiting remine starts

#REDMINE_URL="http://localhost:3001/redmine_backlogs/"
#CONTAINER_ADDRESS=$(docker inspect ${COMPOSE_PROJECT_NAME}_redmine_1 | python ../../get_container_ip.py)
#REDMINE_URL="http://${CONTAINER_ADDRESS}:3000/redmine_backlogs/"

REDMINE_URL="http://${COMPOSE_PROJECT_NAME}_redmine_1:3000/redmine_backlogs/"

while true; do
    MATCH=$(docker-compose logs redmine | grep -m1 "WEBrick::HTTPServer#start" || true)
    if [ -n "$MATCH" ]; then
       break
    fi
    sleep 10
done

cd ../..

echo wait until http request is accepted
docker-compose run tester bash wait_redmine.sh $REDMINE_URL

docker-compose run tester python mechanize/load_default_setting.py $REDMINE_URL
( cd redmine_docker/backlogs ; sh install.sh )
docker-compose run tester python mechanize/config_task_tracker_workflow.py $REDMINE_URL

cd redmine_docker/backlogs
docker-compose restart

while true; do
    MATCH=$(docker-compose logs redmine | tail | grep "Bundled gems are installed" || true)
    if [ -n "$MATCH" ]; then
        break
    fi
    sleep 10
done

cd ../..

echo wait until http request is accepted after restart
docker-compose run tester bash wait_redmine.sh $REDMINE_URL

docker-compose run tester python mechanize/add_task.py $REDMINE_URL
