#! /usr/bin/env python

from jira.client import JIRA
import sys
import traceback

ACCESS_TOKEN = 'IXWGWN1wmcKcpdNwa2GI8n4E6BdKnwl1'
ACCESS_TOKEN_SECRET = 'tHRK2crHo9rAiEJ9HjDnjCKNjqw6Qw1L'
CONSUMER_KEY = 'JiraAvi'

jira_server = 'https://avinetworks.atlassian.net'

with open('jira.pem', 'r') as key_cert_file:
    key_cert = key_cert_file.read()

oauth = {'access_token': ACCESS_TOKEN, 'access_token_secret': ACCESS_TOKEN_SECRET, 'consumer_key': CONSUMER_KEY, 'key_cert': key_cert}

def jira_connect():
    jira = JIRA({'server': jira_server}, oauth = oauth)
    return jira

def create_issue(summary, description, components, versions, issuetype,core_file_location, case_number): 
    project_name = 'AV'
    jira = jira_connect()
    core_file_location = "The Location of Core File is "+core_file_location
    issue = ''

    if jira:
       try: 
           issue = jira.create_issue(project= project_name,
                                     summary = summary,
                                     description = description,
                                     issuetype = {'name': issuetype},
                                     components = [{'name': components}],
                                     versions = [{'name': versions}],
                                     customfield_12424={'value':'Customer Bug'})

       except:
            print traceback.print_exc()
            print "<p>Unable to create Jira Ticket since </p>" 
            exit(0)


    if issue:
        issue.update(fields={'customfield_10400': case_number, 'labels': ['Crash'], 'customfield_10030':{'value':'Severity 1'}, 'priority':{'name':'High'}})
        jira.add_comment(issue, core_file_location)
        return issue


def search_issue(jira_id):
    
    jira = jira_connect()
    issue = ''
    status = ''

    if jira:
        try:
            issue = jira.search_issues('key=%s'% (jira_id))[0]
        except:
            print "<p>Unable to Search issues with the Jira ID</p>"
            sys.stdout.flush()
            pass

    if issue:
        status = issue.raw['fields']['status']['name']

    return status


def add_jira_comments(jira_ticket, contents,core_file_location):

    jira = jira_connect()
    
    if jira:
        try:
            jira.add_comment(jira_ticket, contents)
            jira.add_comment(jira_ticket, core_file_location)
        except:
            print "<p>unable to add Jira Comments</p>"
            pass

