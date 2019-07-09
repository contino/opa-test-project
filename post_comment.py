#!/usr/bin/env python3

from github import Github

import argparse
import sys

parser = argparse.ArgumentParser(description='Post a comment (from stdin) to a github pr')
parser.add_argument('--access_token', help='the user access token with which to authenticate with github', required=True)
parser.add_argument('--hostname', help='the github hostname', required=True)
parser.add_argument('--pr', help='the pull request id', required=True, type=int)
parser.add_argument('--repo', help='the repository', required=True)

import json
result = json.loads(sys.stdin.read())
checks = result[0].items()
failed_checks = {k: v for (k, v) in checks if v == False}
content = []
for (k, v) in failed_checks.items():
    content.append("- {}".format(k))

args = parser.parse_args()

base_url = "https://{hostname}/api/v3".format(hostname=args.hostname)

## Github Enterprise with custom hostname
g = Github(base_url=base_url, login_or_token=args.access_token)

repo = g.get_repo(args.repo)
pr = repo.get_pull(args.pr)

title = "PR {pr_id} failed policy check".format(pr_id=pr.id)

body = "### Failed security policy check in pull request {pull_request_url}\n\n**Constraints violated:**\n{content}\n".format(pull_request_url=pr.html_url, content="\n".join(content))

issue = repo.create_issue(title=title, body=body, assignees=[pr.user])

pr.create_review(body="Policy constraint violation - issue raised: {issue_url}".format(issue_url=issue.html_url))
