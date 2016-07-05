#! /usr/bin/python -u

""" github-watchall.py for watch all repository in organization
Command line options
1: github account name (if 'oauth', read oauth file specified by api_conf)

"""

import requests
import getpass
import re
import sys
import json
from StringIO import StringIO

""" Configuration file api_conf
File in JSON format
user: GitHub API query user name
okey: GitHub API OAuth2 key for user
"""
api_conf = 'conf.json'
api_head = 'https://api.github.com'
api_target_org = 'Subaru-PFS'

api_list_repos = '/orgs/{org}/repos'
api_subscription = '/repos/{owner}/{repo}/subscription'

def ReadConf(fname):
    try:
        fjson = open(fname, 'r')
        return json.load(fjson)
    except:
        return None

def ListRepos(conf):
    opts = {'org': api_target_org}
    url = InsertParameter(api_list_repos, opts)
    data = {'type': 'all'}
    repos = QueryGet(api_head + url, data, conf)
    if repos['code'] != 200:
        return None
    return repos['json']

def GetSubscription(conf, repo):
    opts = {'owner': api_target_org, 'repo': repo}
    url = InsertParameter(api_subscription, opts)
    res = QueryGet(api_head + url, {}, conf)
    if res['code'] != 200:
        return None
    return res['json']

def SubscribeRepo(conf, repo):
    opts = {'owner': api_target_org, 'repo': repo}
    url = InsertParameter(api_subscription, opts)
    data = {'subscribed': True, 'ignored': False}
    res = QueryPut(api_head + url, data, conf)

def QueryGet(url, data, conf):
    r = requests.get(url, auth = (conf['user'], conf['okey']))
    ret = {'code': r.status_code, 'json': r.json(), 'text': r.text}
    return ret

def QueryPut(url, data, conf):
    r = requests.put(url, auth = (conf['user'], conf['okey']), data = json.dumps(data))
    ret = {'code': r.status_code, 'json': r.json(), 'text': r.text}
    return ret

def InsertParameter(target, param):
    for key in param:
        rep = re.compile('{' + key + '}')
        rem = rep.search(target)
        if rem:
            find = rem.span()
            target = target[0:find[0]] + param[key] + target[find[1]:]
    return target

def main(cmdline):
    cmdline.pop(0)
    uname = cmdline.pop(0)
    conf = {}
    if uname == 'oauth':
        conf = ReadConf(api_conf)
        if conf:
            if not (('user' in conf) and ('okey' in conf)):
                print "Required configuration not found: " + api_conf
                return
    else:
        conf['user'] = uname
        conf['okey'] = getpass.getpass()
    repos = ListRepos(conf)
    if repos == None:
        print "Error reading repositories in organization " + api_target_org
        return
    print str(len(repos)) + ' repositories found in organization ' + api_target_org
    for repo in repos:
        reposub = GetSubscription(conf, repo['name'])
        if reposub == None:
            print 'Not subscribed to repository "' + repo['name'] + '", subscribing'
            SubscribeRepo(conf, repo['name'])
        else:
            print 'Already subscribed to repository "' + repo['name'] + '": ' + ' Subscribed=' + str(reposub['subscribed']) + ' Ignored=' + str(reposub['ignored'])

if __name__ == '__main__':
    main(sys.argv)

