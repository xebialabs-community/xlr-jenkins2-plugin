#
# Copyright 2019 XEBIALABS
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

# Compile jobs information for the standard API endpoint
jenkinsServerAPIUrl = jenkinsUrl + '/job/%s/api/json?pretty=true&depth=2&tree=builds[number,result,url]' % (jobName)
jenkinsResponse = XLRequest(jenkinsServerAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()
if jenkinsResponse.status == RESPONSE_OK_STATUS:
    json_data = json.loads(jenkinsResponse.read())
    joblist = []
    buildsToProcess = maxNumberOfBuilds
    for build in json_data['builds']:
        if buildsToProcess <= 0:
            break
        joblist.append(
            {"number" : build['number'], "result" : build['result'], "url" : build['url']}
        )
        buildsToProcess -= 1
else:
    print "Failed to run query in Jenkins"
    jenkinsResponse.errorDump()
    sys.exit(1)

# Add additional information about stages (requires the Jenkins plugin Pipeline Stage View)
for i in range(len(joblist)):
    buildNum = joblist[i]["number"]
    jenkinsServerAPIUrl = jenkinsUrl + '/job/%s/%s/wfapi/describe' % (jobName, buildNum)
    print "/job/%s/%s/wfapi/describe" % (jobName, buildNum)
    jenkinsResponse = XLRequest(jenkinsServerAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()
    if jenkinsResponse.status == RESPONSE_OK_STATUS:
        json_data = json.loads(jenkinsResponse.read())
        joblist[i]["stages"] = []
        for stage in json_data["stages"]:
            joblist[i]["stages"].append(
                {
                    "name": stage["name"],
                    "id": int(stage["id"]),
                    "status": stage["status"],
                    "duration": float(stage["durationMillis"])/1000
                }
            )

# Get data in the plot-ready format
stages_dict = {}
for i in range(len(joblist)):
    for stage in joblist[i]["stages"]:
        if stage["name"] not in stages_dict.keys():
            stages_dict[stage["name"]] = {}
            stages_dict[stage["name"]]["durations"] = [0]*len(joblist)
            stages_dict[stage["name"]]["id"] = stage["id"]
        stages_dict[stage["name"]]["durations"][i] = stage["duration"]
# Create ordered list from dict, using ascending stage ID
stages_list = []
for stage in stages_dict.keys():
    stages_list.append(stages_dict[stage])
    stages_list[-1]["name"] = stage
stages_list = sorted(stages_list, key = lambda i: i['id'])

# Create series object for echarts
series = []
for stage in stages_list:
    series.append(
        {
            "name": stage["name"],
            "type": 'bar',
            "stack": 'stages',
            "data": stage["durations"]
        },
    )

data = {
    "series": series,
    "builds": [job["number"] for job in joblist],
    "stages": [stage["name"] for stage in stages_list]
}