#!/bin/bash

start_app() {
    docker-compose build
    docker-compose up -d --remove-orphans --force-recreate
    echo "Starting success"
}

clean_app() {
    docker-compose down
}

while getopts ":p:" opt; do
  case $opt in
    p) param="$OPTARG"
    ;;
    \?) echo "using arg -p with up to run up app, -p down to clean up" >&2
    ;;
  esac
done

if [[ "$param" == "up" ]]; then
    start_app
elif [[ "$param" == "down" ]]; then
    clean_app
fi