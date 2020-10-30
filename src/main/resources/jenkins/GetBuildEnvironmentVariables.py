#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import urllib
import logging

from xlrelease.HttpRequest import HttpRequest

logging.basicConfig(filename='log/plugin.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("GetBuildEnvironmentVariables: begin")


def get_environmentvariables(context):
    response = request.get(context + 'api/json', contentType='application/json')
    logging.debug("response status: %s" % response.status)
    logging.debug("response: %s" % response.response)

    if not response.isSuccessful():
        errorStr = ("Failed to get build environment variables. Is the Jenkins Plugin 'Environment Injector'"
        +" installed? "
        +"Server return [%s], with content [%s]" % (response.status, response.response))
        raise Exception(errorStr)

    decoded = json.loads(response.response)
    #decoded = response.response
    values = decoded['envVars']['envVar']
    logging.debug("The values are %s" % str(values))

    data = {}

    if len(values) > 0:
        for item in values:
            if 'value' in item:
                data[item['name']] = item['value']
            else:
                data[item['name']] = 'XXXXXXXX'
    else:
        print("Job has no environment variables")

    return data

job_context = '/job/' + urllib.quote(jobName) + '/' + buildNumber + '/' + 'injectedEnvVars/export/'
logging.info("job_context %s" % job_context)

request = HttpRequest(server, username, password)
jobEnvVars = get_environmentvariables(job_context)

logging.info("GetBuildEnvironmentVariables: end")
