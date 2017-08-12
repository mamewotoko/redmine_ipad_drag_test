#! /bin/bash
set -e

. config.env

cd redmine_docker/backlogs/
docker-compose down
sudo rm -rf volume
cd ../..

