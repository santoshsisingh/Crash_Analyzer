#! /usr/bin/env python

import MySQLdb
import re 
from prettytable import PrettyTable as pp
import jira_utils
from datetime import datetime


def get_contents(stack_trace):
    contents = ""
    multi_thread = False
    thread_pattern = re.compile('Thread\s[0-9]{1,2}')

    with open(stack_trace, 'r') as f:
        for line in f:
            contents+=line

    if thread_pattern.search(contents):
        multi_thread = True

    return (contents, multi_thread)  

def get_function_list_signal_from_multi_thread_stack_trace(contents):
    func_pattern = re.compile('\s(\S*)\s\(')
    signal = ''
    func_name = []
    crash_func = ''
    match = False
    thread_group = []

    contents_group = [line for line in re.split('Thread\s[0-9]+\s', contents)]
    

    for non_thread in contents_group[0].split("\n"):
        if "signal" in non_thread:
            signal = non_thread
        elif (non_thread.startswith('#') and '??' not in non_thread) :
            if func_pattern.search(non_thread):
                crash_func = func_pattern.search(non_thread).group(1)

    for temp in contents_group[1:]:
        if crash_func in temp:
            thread_group.append(temp.split("\n"))

    for thread_list in thread_group[:1]:
        for line in thread_list:
            if (line.startswith('#') and '??' not in line) :
                if func_pattern.search(line):
                    if crash_func == func_pattern.search(line).group(1):
                        match = True
                    if match:
                        func_name.append(func_pattern.search(line).group(1))

    return (func_name, signal)                                                                                                                                                                                                                             

def get_function_list_signal_from_stack_trace(stack_trace):
    func_pattern = re.compile('\s(\S*)\s\(')
    signal = ''
    func_list = []
    
    contents, multi_thread = get_contents(stack_trace)
    
    if multi_thread:
            func_list, signal = get_function_list_signal_from_multi_thread_stack_trace(contents)
            return (func_list, signal, contents)

    else:
        with open(stack_trace, 'r') as f:
            for line in f:
                if 'signal' in line:
                    signal = line
                if (line.startswith('#') and '??' not in line) :
                    if func_pattern.search(line):
                        func_list.append(func_pattern.search(line).group(1))
        
        return (func_list, signal, contents)


def mysql_connect():
    
    try:
        conn = MySQLdb.connect(host='10.10.25.137', \
                        port = 3306,\
                        db='jenkins_report_portal',\
                        user='root',\
                        passwd='avi123mysql')
    except MySQLdb.Error as e:
        print "MySql Operation Failed because %s" %(str(e))
        exit(0)

    return conn



def check_for_duplicates_in_db(func_list, signal):

    signal = signal.strip()
    crash_function = ''
    
    if '_' not in func_list[0]:
        crash_function = func_list[1]

    if crash_function and  '_' not in crash_function:
        crash_function = func_list[2]
    else:    
        crash_function = func_list[0]

    if func_list[0] == func_list[1]:
        function_list = ', '.join(func_list[1:])
    else:
        function_list = ', '.join(func_list)
    jira_ticket = ''
    status = ''

    sql = "SELECT * FROM crash_issue WHERE function_list LIKE '%s' AND issue_signal LIKE '%s'" % (function_list, signal)

    conn = mysql_connect()

    if conn:
        cursor = conn.cursor()
        try:
            
            cursor.execute(sql)
            for row in cursor:
                jira_ticket = row[1]
                status = row[2]
        except MySQLdb.Error as e:
            print "MySql Operation Failed because %s" %(str(e))

    if jira_ticket:
        new_status = jira_utils.search_issue(jira_ticket)
        if new_status != status:
            status = new_status
            update_database(jira_ticket, status)


    conn.commit()
    conn.close()



    return (crash_function, jira_ticket, status, function_list) 


def insert_into_database(issue_key, issue_status, task_id, total, title, last_line, created_date,issue_signal,function_list, **kwargs):

    conn = mysql_connect()
    stack_trace = kwargs.get("stack_trace", "")

    if conn:
        cursor = conn.cursor()
        try:
            sql = 'INSERT INTO crash_issue(issue_key, issue_status, task_id, total, title, last_line, created_date,stack_trace,issue_signal,function_list) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            cursor.execute(sql, (issue_key, issue_status, task_id, total, title, last_line, created_date,stack_trace,issue_signal,function_list))
        except MySQLdb.Error as e:
            print "MySql Database Update Failed because %s hence please send details of this error to santosh@avinetworks.com" %(str(e))

    conn.commit()
    conn.close()

   
def update_database(jira_ticket, status):

    conn = mysql_connect()

    if conn:
        cursor = conn.cursor()
        try:
            sql = "UPDATE crash_issue SET issue_status='%s' WHERE issue_key='%s'" %(status, jira_ticket)
            cursor.execute(sql)
        except MySQLdb.Error as e:
            print "MySql Operation Failed because %s" %(str(e))
            pass

    conn.commit()
    conn.close()
    


def create_jira_ticket(crash_function, contents, version, build,function_list,signal,core_file_location,case_number):
    
    summary = "Service Engine Crashed @ %s" % crash_function
    components = 'SE-Others'
    versions = version
    description = contents
    issue_type = 'Bug'
    jira_ticket = ''
    status = ''

    issue = jira_utils.create_issue(summary, description, components, versions, issue_type,core_file_location,case_number)

    if issue:
        jira_ticket = issue.key
        status = issue.raw['fields']['status']['name']

    #print "Jira ID: %s\nStatus: \%s\n" % (jira_ticket, status)
    insert_into_database(jira_ticket, status, 0, 1, summary, 'NULL', datetime.now(),signal,function_list, stack_trace=contents)

    return (jira_ticket, status)


def add_jira_comment(jira_ticket, contents):
    jira_utils.add_jira_comments(jira_ticket, contents)
    

def display_results_in_tabular_format(core_file, crash_function, jira_ticket, status):

    col = pp([' Core File', 'Crash Function', 'Matching JIRA ID', 'Status'])
    col.add_row([core_file, crash_function, jira_ticket, status])
    print col
    print '\n'


def display_results_of_new_jira_in_tabular_format(core_file, crash_function, jira_ticket, status):

    col = pp([' Core File', 'Crash Function', 'JIRA ID', 'Status'])
    col.add_row([core_file, crash_function, jira_ticket, status])
    print col
    print '\n'
