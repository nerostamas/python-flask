#! /bin/bash

mongoimport --host mongodb --db ${MONGO_DB} --collection user --type json --file /mongo-seed/init-data.json --jsonArray
