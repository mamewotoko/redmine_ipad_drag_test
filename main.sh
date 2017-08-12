#! /bin/sh

./finalize.sh
(
    set -e
    set -x
    ./init.sh
    ./run.sh
)

{
    ./finalize.sh
}

