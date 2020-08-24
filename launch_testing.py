import subprocess
import os
import json
from jira import JIRA
from datetime import datetime

tt = "{0} \nTests:\n".format(datetime.now())

test_to_execute = []
folder = "tests_to_run"
try:
    with open("tests_to_run/test_organization.jsonc") as f:
        data = json.load(f)
        data[os.environ["test_case"]]
        case = data[os.environ["test_case"]]
        test_to_execute = case
except:
    test_to_execute.append(os.environ["test_case"])


print("Test from '{0}' to_execute:".format(os.environ["test_case"]))
for i in test_to_execute:
    print(i)
print("-----------------------------")


logger_file = open("logger_file.log", "w+")
for i in test_to_execute:
    tt = tt + i + "\n"
    path_to_file = os.path.join(folder, i)
    print("Test file: {0}  exists: {1}".format(path_to_file, os.path.isfile(path_to_file)))
    p1 = subprocess.Popen(["pytest", path_to_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p1.communicate()
    print(out.decode())
    print(err.decode())
    logger_file.write(out.decode())
    logger_file.write(err.decode())
    p1.stdout.close()
logger_file.close()


JIRA_SERVER = os.environ["jira_server"]
USER = os.environ['user']
TOKEN = os.environ['token']

jira = JIRA(server=JIRA_SERVER, basic_auth=(USER, TOKEN))
issue = jira.issue(os.environ["jira_text_execution"])
print("this is the issue: {0}  issue_id:".format(issue, issue.id))

logger_file = open("logger_file.log", "r")

tt = tt + "Results:\n"
file_lines = logger_file.readlines()
for i in file_lines:
    if i != "\n":
        # print(i)
        tt = tt + i
# print(file_lines)
comment = jira.add_comment(issue, tt)
logger_file.close()
