#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import com.xhaus.jyson.JysonCodec as json

if not jenkinsServer:
    raise Exception("Jenkins server ID must be provided")
if not username:
    username = jenkinsServer["username"]
if not password:
    password = jenkinsServer["password"]

jenkinsUrl = jenkinsServer['url']

credentials = CredentialsFallback(jenkinsServer, username, password).getCredentials()
content = None
RESPONSE_OK_STATUS = 200
print "Sending content %s" % content

jenkinsServerAPIUrl = jenkinsUrl + '/job/%s/api/json?pretty=true&depth=2&tree=builds[displayName,result,url]' % (jobName)
jenkinsResponse = XLRequest(jenkinsServerAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()
if jenkinsResponse.status == RESPONSE_OK_STATUS:
    json_data = json.loads(jenkinsResponse.read())
    joblist = []
    for item in json_data['builds']:
    	data1 = {"number" : item['displayName'], "result" : item['result'], "url" : item['url']}
        joblist.append(data1)
    data = joblist
else:
    error = json.loads(jenkinsResponse.read())
    if 'Invalid table' in error['error']['message']:
        print "Invalid Table Name"
        data = {"Invalid table name"}
        jenkinsResponse.errorDump()
    else:
        print "Failed to run query in Jenkins"
        jenkinsResponse.errorDump()
        sys.exit(1)
