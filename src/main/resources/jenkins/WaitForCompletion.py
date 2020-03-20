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

from xlrelease.HttpRequest import HttpRequest

job_context = "/job/" + urllib.quote(jobName) + "/" + buildNumber + "/"

request = HttpRequest(server, username, password)
response = request.get(job_context + "api/json", contentType="application/json")

if not response.isSuccessful():
    raise Exception(
        "Failed to get build information. Server return [%s], with content [%s]"
        % (response.status, response.response)
    )

result = json.loads(response.response)["result"]

if result is None:
    task.setStatusLine("Waiting for build completion...")
    task.schedule("jenkins/WaitForCompletion.py", 3)
else:
    if result != "SUCCESS":
        raise Exception("[Build %s](%s) was not successful - status is %s" % (
            buildNumber,
            json.loads(response.response)["url"],
            result,
        ))
    else:
        task.setStatusLine("Success")
