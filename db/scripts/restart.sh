#!/bin/bash
docker compose -f ./db/dbcluster.yml down
docker build -f ./db/mongox -t nachocode/mongox:n1 /home/nacho/Programming/Python/oca_api/db 
docker build -f ./db/mongox2 -t nachocode/mongox:n2 /home/nacho/Programming/Python/oca_api/db 
docker build -f ./db/mongox3 -t nachocode/mongox:n3 /home/nacho/Programming/Python/oca_api/db 
docker compose -f ./db/dbcluster.yml up -d