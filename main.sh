#! /bin/bash

. config.env
./finalize.sh

(
    set -e
    set -x
    ./init.sh
    ## TODO: define sprint
    docker-compose run --rm tester ./run_test.sh $REDMINE_URL
)
EXIT_CODE=$?
{
    ./finalize.sh
}
exit $EXIT_CODE
