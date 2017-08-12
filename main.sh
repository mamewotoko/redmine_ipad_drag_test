#! /bin/bash

./finalize.sh
(
    set -e
    set -x
    ./init.sh
    ./run_test.sh
)
EXIT_CODE=$?
{
    ./finalize.sh
}
exit $EXIT_CODE
