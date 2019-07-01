#!/usr/bin/env python3

import json, sys
from junit_xml import TestSuite, TestCase

def generate_junit_report(failed_checks):
    test_cases = []
    for (k, v) in failed_checks.items():
        tc = TestCase(k, k, 0, "Policy Check Result: {}".format(v))
        tc.add_failure_info("Policy [{}] check failed.".format(k), "failure")
        test_cases.append(tc)
    return [TestSuite("Policy Checks", test_cases)]

with open('result.json') as json_file:
    data = json.load(json_file)
    failed_checks = {k: v for (k, v) in data[0].items() if v == False}
    if len(failed_checks) > 0:
        print("Policy Check Failures Detected!")
        print("Failed policy checks:")
        for (k, v) in failed_checks.items():
            print("{}".format(k))
        with open('test-policy-result-report.xml', 'w') as f:
            TestSuite.to_file(f, generate_junit_report(failed_checks), prettyprint=False)
        sys.exit(-1)
    else:
        print("All Policy Checks Succeeded!")
