#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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