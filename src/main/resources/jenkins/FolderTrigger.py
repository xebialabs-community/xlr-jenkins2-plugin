#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import ast
import json
from xlrelease.HttpRequest import HttpRequest

def get_jobs(folder_name):
    jenkins_cis = []
    response = request.get('job/' + folder_name + '/api/json?depth=2', contentType='application/json')
    if not response.isSuccessful():
        raise Exception("Failed to check for folder. Server return [%s], with content [%s]" % (response.status, response.response))
    response_json = json.loads(response.response)
    if "jobs" in response_json:
        for job in response_json["jobs"]:
            if "buildable" not in job or not job["buildable"]:
                jenkins_cis.extend(get_jobs(folder_name + "/job/" + job["name"]))
            elif job["buildable"]:
                jenkins_cis.append(job)
    return jenkins_cis

def convert_dict_to_sorted_string(dict_jobs):
    string_dict = "{"
    sorted_keys = sorted(dict_jobs.iterkeys())
    for idx, key in enumerate(sorted_keys, start=1):
        string_dict += "'%s':'%s'" % (key, dict_jobs[key])
        if idx < len(sorted_keys):
            string_dict += ","
    string_dict += "}"
    return string_dict

request = HttpRequest(server, username, password)
jobs = ast.literal_eval(triggerState) if triggerState else {}
jenkins_jobs = dict()
# Do this recursive
for job in get_jobs(folderName):
    job_name = job["fullName"]
    build_number = job[buildStatus]["number"] if job[buildStatus] else None
    if build_number and (job_name not in jobs or jobs[job_name] != str(build_number)):
        jobs[job_name] = build_number
        branchName = job["name"]
        jenkins_jobs[job["fullName"]]=str(build_number)

jenkinsJobs = str(jenkins_jobs)
triggerState = convert_dict_to_sorted_string(jobs)
