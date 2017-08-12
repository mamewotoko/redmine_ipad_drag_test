#! /bin/sh
REDMINE_URL=$1

for i in $(seq 1 100); do
    OUT=$(curl -I $REDMINE_URL | grep "HTTP/1.1 200 OK"  || true)
    if [ -n "$OUT" ]; then
        break
    fi
    sleep 10
done
