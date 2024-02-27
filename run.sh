#!/bin/bash
docker run \
-e  MONGO_IP_ADDR="mongol" \
-e MONGO_PORT="27017" \
-e MONGO_DATABASE_NAME="oca" \
-e IP_ADDR="0.0.0.0" \
-e PORT="5000" \
-e RELOAD="0" \
-v /data:/data \
--name oca-api \
--network="oca" \
-p 500:5000 \
-d \
nachocode/oca:api