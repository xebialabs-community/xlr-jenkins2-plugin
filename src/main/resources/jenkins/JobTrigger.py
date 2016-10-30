#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import json, urllib
from xlrelease.HttpRequest import HttpRequest

def get_latest_build_number(context):
    response = request.get(context + 'api/json', contentType ='application/json')
    build_number = json.loads(response.response)['lastBuild.number']
    return build_number


job_context = '/job/' + urllib.quote(jobName) + '/'
request = HttpRequest(server, username, password)
buildNumber = get_latest_build_number(job_context)
triggerState = buildNumber