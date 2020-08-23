import argparse
import subprocess
import os
import json

os.environ['test_case'] = 'stage'

# parser = argparse.ArgumentParser()
# parser.add_argument("test")
# args = parser.parse_args()

test_to_execute = []
folder = "tests_to_run"
try:
    with open("tests_to_run/test_organization.jsonc") as f:
        data = json.load(f)
        data[os.environ["test_case"]]
        print(data)
        case = data[os.environ["test_case"]]
        test_to_execute = case
except Exception as e:
    test_to_execute.append(os.environ["test_case"])

print(test_to_execute)


logger_file = open("logger_file.log", "w")
for i in test_to_execute:
    pathh = os.path.join(folder, i)
    p1 = subprocess.Popen(["pytest", os.path.join(folder, i)], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p1.communicate()
    logger_file.write(out.decode())
    logger_file.write(err.decode())
    p1.stdout.close()

