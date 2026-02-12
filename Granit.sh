#!/bin/bash

cd /home/guard/Pay_Project/granit_pol/
rm -rf Granit_pol

# Classic token (починається з ghp_)
export GITHUB_TOKEN="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"

# Клонування без username
git clone -b master "https://${GITHUB_TOKEN}@github.com/GuardianOfHell/Granit_pol.git"

docker stop granit_pol 2>/dev/null
docker rm granit_pol 2>/dev/null
docker rmi granit_pol 2>/dev/null

cd /home/guard/Pay_Project/granit_pol/Granit_pol/
docker build -t granit_pol .

docker run -d \
  --name granit_pol \
  -v /home/guard/Pay_Project/granit_pol/socker:/app/sockets \
  -v /home/guard/Pay_Project/granit_pol/staticfiles:/app/staticfiles \
  -v /home/guard/Pay_Project/granit_pol/media:/app/media \
  -v /home/guard/Pay_Project/granit_pol/error/errors.log:/app/errors.log \
  --net las_in_ua \
  --ip 172.18.0.19 \
  --restart always \
  granit_pol