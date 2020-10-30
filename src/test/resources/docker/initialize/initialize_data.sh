#!/bin/sh
#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

####################### Jenkins server data

curl --user admin:admin -i -X POST http://localhost:15516/api/v1/config \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  --data "@"$SCRIPTPATH"/data/server-config.json"

SERVER="http://localhost:9080"
COOKIEJAR="$(mktemp)"
CRUMB=$(curl -u "admin:admin" --cookie-jar "$COOKIEJAR" "$SERVER/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,%22:%22,//crumb)")
curl -s -X POST -u "admin:admin" --cookie "$COOKIEJAR"  -H "$CRUMB" -H "Content-Type:text/xml" --data "@"$SCRIPTPATH"/data/config.xml" "$SERVER"/createItem?name=myBuild
curl -X POST -u "admin:admin" --cookie "$COOKIEJAR" -H "$CRUMB" "$SERVER"/job/myBuild/buildWithParameters


########### LOAD XLR TEMPLATE

curl --user admin:admin -i -X POST http://localhost:15516/api/v1/templates/import \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    --data "@"$SCRIPTPATH"/data/release-template.json"