#! /usr/bin/python -u

""" Command line option
1: command ('create', or 'comment')
2: owner of target repository
3: name of target repository
4-: option per command

Option for 'create'
4: title
5: assignee
6: body (filename)

Option for 'comment'
4: issue ID
5: body (filename)
"""

import pycurl
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

api_issue_create = '/repos/{owner}/{repo}/issues'
api_issue_comment = '/repos/{owner}/{repo}/issues/{number}/comments'

def ReadConf(fname):
    try:
        fjson = open(fname, 'r')
        return json.load(fjson)
    except:
        return None

def ReadComment(fname):
    try:
        with open(fname, 'r') as fdat:
            data = fdat.read()
            fdat.close()
    except:
        return None
    return data

def IssueComment(conf, opt):
    opts = {'owner': opt[0], 'repo': opt[1], 'number': opt[2] }
    url = InsertParameter(api_issue_comment, opts)
    print url
    body = ReadComment(opt[3])
    if not body:
        print "Null comment body file: " + opt[3]
        return
    data = json.dumps({'body': body})
    QueryAPI(api_head + url, data, conf)

def IssueCreate(conf, opt):
    opts = { 'owner': opt[0], 'repo': opt[1] }
    url = InsertParameter(api_issue_create, opts)
    print url
    body = ReadComment(opt[4])
    if not body:
        print "Null comment body file: " + opt[4]
        return
    data = json.dumps({
            'title': opt[2],
            'body': body,
            'assignee': opt[3]
            })
    QueryAPI(api_head + url, data, conf)

def QueryAPI(url, json, conf):
    c = pycurl.Curl()
    buf = StringIO()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buf)
    c.setopt(c.USERPWD, conf['user'] + ':' + conf['okey'])
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, json) 
    c.perform()
    print 'code: ' + str(c.getinfo(c.HTTP_CODE))
    c.close()
    print buf.getvalue()

def InsertParameter(target, param):
    for key in param:
        rep = re.compile('{' + key + '}')
        rem = rep.search(target)
        if rem:
            find = rem.span()
            target = target[0:find[0]] + param[key] + target[find[1]:]
    return target

def main(cmdline):
    conf = ReadConf(api_conf)
    if conf:
        if not (('user' in conf) and ('okey' in conf)):
            print "Required configuration not found: " + api_conf
            return
        cmdline.pop(0)
        api_cmd = cmdline.pop(0)
        if api_cmd == 'create':
            IssueCreate(conf, cmdline)
        elif api_cmd == 'comment':
            IssueComment(conf, cmdline)
        else:
            return
    else:
        print "No configuration file found: " + api_conf

if __name__ == '__main__':
    main(sys.argv)

