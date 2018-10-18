#coding: utf-8
import argparse
import subprocess
import re

import requests
from git import Repo


def parse_issues(repo_path, repo_url, before_day, split_key):
    log_cmd = '''git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %C(blue)%s%Creset %C(dim cyan)<%an>%Creset %C(dim white)(%ci)%Creset' --abbrev-commit --since=\"{day} days ago\"'''.format(day=before_day)
    cd_cmd = "cd {path} && ".format(path=repo_path)
    git_log = subprocess.check_output(cd_cmd + log_cmd, shell=True)
    out_text = git_log.decode('utf-8')
    if split_key:
        scope_pattern = re.compile('(.*?) {key}'.format(key=split_key), re.S)
        scope_text = re.search(scope_pattern, out_text)[0]
    else:
        scope_text = out_text
    issue_pattern = re.compile('\* \w{8} - .*?#(\d+) <.*?> \(.*?\)', re.S)
    all_issues = set(re.findall(issue_pattern, scope_text))

    if not repo_url.endswith('/'):
        repo_url += '/'
    repo_url += 'issues/'
    return map(lambda x: (x, repo_url + x), all_issues)


def parse_commit_msg(repo_path):
    repo = Repo(repo_path)
    commits = list(repo.iter_commits(max_count=10))
    return ''.join(map(lambda m: '✓ ' + m, [commit.message for commit in commits]))


def send_to_bc(text, webhook):
    data = {
        "text": text,
        "markdown": True,
    }
    requests.post(webhook, json=data)


def main(arges):
    issues = parse_issues(arges.repo_path, arges.repo_url, arges.day, arges.key)
    issues = map(lambda x: '[#{issue}]({url})'.format(issue=x[0], url=x[1]), issues)
    issues_str = ' '.join(issues)
    commit_message_str = parse_commit_msg(arges.repo_path)
    text = '\n'.join([arges.fir, issues_str, commit_message_str])
    send_to_bc(text, arges.webhock)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--git', required=True, dest='repo_path', help='repo path')
    parser.add_argument('-u', '--url', required=True, dest='repo_url', help='the repo url in github')
    parser.add_argument('-w', '--webhock', required=True, dest='webhock')
    parser.add_argument('-d', '--day', dest='day', default=30)
    parser.add_argument('-k', '--key', dest='key', help='the keyword about bump version')
    parser.add_argument('-f', '--fir', dest='fir', help='fir url', default='')
    result = parser.parse_args()
    print(result)
    main(result)
