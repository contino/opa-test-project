#!/usr/bin/env python3

from github import Github

import argparse

parser = argparse.ArgumentParser(description='Post a comment to a github pr')
parser.add_argument('--access_token', help='the user access token with which to authenticate with github', required=True)
parser.add_argument('--hostname', help='the github hostname', required=True)
parser.add_argument('--pr', help='the pull request id', required=True, type=int)
parser.add_argument('--comment', help='the comment', required=True)
parser.add_argument('--repo', help='the repository', required=True)

args = parser.parse_args()

## Github Enterprise with custom hostname
g = Github(base_url=f'https://{args.hostname}/api/v3', login_or_token=args.access_token)

repo = g.get_repo(args.repo)
pr = repo.get_pull(args.pr)

pr.create_review(body=args.comment)
