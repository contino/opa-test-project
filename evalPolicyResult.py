#!/usr/bin/env python3

import json, sys
from junit_xml import TestSuite, TestCase

def generate_junit_report(checks):
    test_cases = []
    for (k, v) in checks:
        tc = TestCase(k, "policy", 0)
        if (v == False):
            tc.add_failure_info("Policy [{}] check failed.".format(k))
        test_cases.append(tc)
    return [TestSuite("Policy Checks", test_cases)]

data = json.loads(sys.stdin.read())
checks = data[0].items()
with open('test-policy-result-report.xml', 'w') as f:
    TestSuite.to_file(f, generate_junit_report(checks), prettyprint=True)
failed_checks = {k: v for (k, v) in checks if v == False}
if len(failed_checks) > 0:
    print("Policy Check Failures Detected! The following policy checks failed:")
    for (k, v) in failed_checks.items():
        print("\t{}".format(k))
    sys.exit(-1)
else:
    print("All Policy Checks Succeeded!")
