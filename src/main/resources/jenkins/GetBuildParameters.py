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

logging.info("GetBuildParameters: begin")


def get_parameters(context):
    response = request.get(context + 'api/json', contentType='application/json')
    logging.debug("response status: %s" % response.status)
    logging.debug("response decoded: %s" % response.response)

    if not response.isSuccessful():
        raise Exception("Failed to get build parameters. Server return [%s], with content [%s]" % (response.status, response.response))

    decoded = json.loads(response.response)
    values = [item.get('parameters') for item in decoded['actions'] if item.get('parameters')]

    data = {}

    if len(values) > 0:
        for v in values[0]:
            if 'value' in v:
                data[v['name']] = v['value']
            else:
                data[v['name']] = 'XXXXXXXX'
    else:
        print("Job has no parameters")

    return data

job_context = '/job/' + urllib.quote(jobName) + '/' + buildNumber + '/'
logging.info("job_context %s" % job_context)

request = HttpRequest(server, username, password)
jobParameters = get_parameters(job_context)

logging.info("GetBuildParameters: end")
