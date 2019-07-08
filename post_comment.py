#!/usr/bin/env python3

from github import Github

import argparse
import sys

parser = argparse.ArgumentParser(description='Post a comment (from stdin) to a github pr')
parser.add_argument('--access_token', help='the user access token with which to authenticate with github', required=True)
parser.add_argument('--hostname', help='the github hostname', required=True)
parser.add_argument('--pr', help='the pull request id', required=True, type=int)
parser.add_argument('--repo', help='the repository', required=True)


import fileinput

comment = sys.stdin.read()

args = parser.parse_args()

base_url = "https://{hostname}/api/v3".format(hostname=args.hostname)

## Github Enterprise with custom hostname
g = Github(base_url=base_url, login_or_token=args.access_token)

repo = g.get_repo(args.repo)
pr = repo.get_pull(args.pr)

pr.create_review(body=comment)
