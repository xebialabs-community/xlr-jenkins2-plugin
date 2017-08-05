#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from xlrelease.HttpRequest import HttpRequest

if not jenkinsServer:
    raise Exception("Jenkins server ID must be provided")

jenkins_server_api_url = '/job/%s/api/json?pretty=true&depth=2&tree=builds[displayName,result,url]' % (jobName)
request = HttpRequest(jenkinsServer, username, password)
response = request.get(jenkins_server_api_url, contentType='application/json')

if not response.isSuccessful():
    print "Failed to run query in Jenkins"
    raise Exception("Failed to get job summary. Server return [%s], with content [%s]" % (response.status, response.response))

json_data = json.loads(response.response)
job_list = []
for item in json_data['builds']:
    data1 = {"number" : item['displayName'], "result" : item['result'], "url" : item['url']}
    job_list.append(data1)
data = job_list
