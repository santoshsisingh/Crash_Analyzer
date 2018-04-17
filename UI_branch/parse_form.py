#! /usr/bin/env python

import cgi
import os
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
if form['case_num'].value == " ":
    form['case_num'].value= None
#print "The core Archive Directory path is %s" %(form['core_dir_path'].value)
#print "The salesforce force case number  is %s" %(form['case_num'].value)
cmd = "sudo python generate_bt.py -p %s -c %s" %( form['core_dir_path'].value, form['case_num'].value)
os.system(cmd)

