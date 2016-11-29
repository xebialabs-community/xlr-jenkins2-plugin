#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json
import urllib
from xlrelease.HttpRequest import HttpRequest


def get_parameters(context):
    response = request.get(context + 'api/json', contentType='application/json')
    print 'response %s' % response
    if not response.isSuccessful():
        raise Exception("Failed to check for last build. Server return [%s], with content [%s]" % (response.status, response.response))

    decoded = json.loads(response.response)
    values = decoded['actions'][0]['parameters']
    data = {}
    for v in values:
        if 'value' in v:
            data[v['name']] = v['value']
        else:
            data[v['name']] = 'XXXXXXXX'
    return data


job_context = '/job/' + urllib.quote(jobName) + '/' + buildNumber + '/'
print "job_context %s" % job_context
request = HttpRequest(server, username, password)
jobParameters = get_parameters(job_context)
