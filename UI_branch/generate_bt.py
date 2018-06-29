#!/usr/bin/env python


import re
import pexpect
import sys
import os
import subprocess
import argparse
import generate_bt_utils as utils


def usuage():
    print "Content-Type: text/html\r\n"
    print """ 
            <!DOCTYPE html>
            <html>
            <p>This Site compares Stack Traces of Core Files and Looks up the Database to find Duplicate crashes matching the current Stack trace. 
              if a match is found, the Jira Ticket and the Staus of Ticket is returned. If a match is not found in the database a new Jira Ticket
              is created Automatically along with the contents of the Stack Trace.

              The Core Archive Directory containing a list of 'Core Archive Bundle'and Salesforce Case Number is given as input 
              to the Script. Below is an example of a Core Archive Directory.

              root@Avi-Dev:/mnt/cores/case_3231/:
              -rw-r--r-- 1  595 30932 149380832 Jul 14 19:17 core_archive_bundle.20170714_190341_1500059021.tar.gz
              -rw-r--r-- 1  595 30932 149762251 Jul 14 19:17 core_archive_bundle.20170714_190804_1500059284.tar.gz
              -rw-r--r-- 1  595 30932 147819144 Jul 14 19:17 core_archive_bundle.20170714_191229_1500059549.tar.gz
              -rw-r--r-- 1  595 30932  98500608 Jul 14 19:17 core_archive_bundle.20170714_191659_1500059819.tar.gz
             </p>
             </html>"""

              
            
                  
    


def untar_core_directories(path_to_core_archive_directory):
    
    #os.chdir(path_to_core_archive_directory)
    #ls_dir = os.listdir(path_to_core_archive_directory)
    try:
        ls_dir = os.listdir(path_to_core_archive_directory)
    except OSError as e:
        print "Content-Type: text/html\r\n"
        html_data = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>SE Core Analyzer</title>
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
            <style>
            input[type=text] {
                    width: 95%;
                        padding: 12px 12px;
                            margin: 8px 0;
                                box-sizing: border-box;
                                    border: 1px solid #555;
                                        outline: none;
            }

            input[type=text]:focus {
                    background-color: white;
            }

            h2 {
                    border-bottom: 4px solid;
                    border-bottom-width: 6px;
                    border-bottom-style: solid;
                    border-bottom-color: rgb(255, 75, 0);
            }
            </style>
            </head>
                            
                               <body>
                               <header class="w3-container" style="padding:30px;background-color:#2a2a2d;color:white">
                                                       <div class="w3-container" style="padding-top:10px;float:left">
                                                                    <img src="https://avinetworks.com/client/logo.png" alt="Avi Networks">
                                                                                </div>
                                       <div class="w3-container w3-center"><h1>SE Core Analyzer</h1></div>
                                       <h2><div class="w3-bar w3-deep-orange" style="color:white"></div></h2
                               </header>"""
        print html_data
        sys.stdout.flush()
        print "<p><b>Unable to list the given Core Archive Path since %s</b></p>" %(str(e))
        exit(0)

    core_archive_untarred_directory_pattern = re.compile('core_archive_bundle\.(\d+_\d+_\d+)')
    core_archive_untarred_directory_hm_pattern = re.compile('core_archive_bundle_hm\.(\d+_\d+_\d+)')
    core_archive_tarred_directory_pattern = re.compile('^\d+_\d+_\d+')

    core_file_bundle_to_untar = [f for f in ls_dir if core_archive_untarred_directory_pattern.search(f)]
    core_file_bundle_to_untar.extend([f for f in ls_dir if core_archive_untarred_directory_hm_pattern.search(f)])
    core_directories_already_untarred = [f for f in ls_dir if core_archive_tarred_directory_pattern.search(f)]
     

    print "Content-Type: text/html\r\n"
    html_data = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>SE Core Analyzer</title>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <style>
        input[type=text] {
                width: 95%;
                    padding: 12px 12px;
                        margin: 8px 0;
                            box-sizing: border-box;
                                border: 1px solid #555;
                                    outline: none;
        }

        input[type=text]:focus {
                background-color: white;
        }

        h2 {
                border-bottom: 4px solid;
                border-bottom-width: 6px;
                border-bottom-style: solid;
                border-bottom-color: rgb(255, 75, 0);
        }
        </style>
        </head>
                        
                           <body>
                           <header class="w3-container" style="padding:30px;background-color:#2a2a2d;color:white">
                                                   <div class="w3-container" style="padding-top:10px;float:left">
                                                                <img src="https://avinetworks.com/client/logo.png" alt="Avi Networks">
                                                                            </div>
                                   <div class="w3-container w3-center"><h1>SE Core Analyzer</h1></div>
                                   <h2><div class="w3-bar w3-deep-orange" style="color:white"></div></h2
                           </header>"""
    print html_data
    sys.stdout.flush()
    if not core_file_bundle_to_untar:
        print "<p>There are no Core Archive Directories under the path %s</p>" %(path_to_core_archive_directory)
        sys.stdout.flush()
        exit(0)
    print "<p>Untarring the Core Archive Directories</p>"
    sys.stdout.flush()
    for f in core_file_bundle_to_untar:
        if core_archive_untarred_directory_pattern.search(f):
            if core_archive_untarred_directory_pattern.search(f).group(1) not in core_directories_already_untarred:
                print "<p>Trying to untar the file %s</p>" %f
                sys.stdout.flush()
                try:
                    subprocess.check_call(['tar','-xzf',path_to_core_archive_directory+f,'--directory',path_to_core_archive_directory])
                    print "<p>Untarred the file %s successfully</p>" %f
                    sys.stdout.flush()
                    core_directories_already_untarred.append(core_archive_untarred_directory_pattern.search(f).group(1))
                except subprocess.CalledProcessError as e:
                    print "<p>unable to untar the directory since %s</p>" %str(e)
                    sys.stdout.flush()
                    pass
                
        elif core_archive_untarred_directory_hm_pattern.search(f): 
            if core_archive_untarred_directory_hm_pattern.search(f).group(1) not in core_directories_already_untarred:
                print "<p>Trying to untar the file %s</p>" %f
                sys.stdout.flush()
                try:
                    subprocess.check_call(['tar','-xzf',path_to_core_archive_directory+f,'--directory',path_to_core_archive_directory])
                    print "<p>Untarred the file %s successfully</p>" %f
                    sys.stdout.flush()
                    core_directories_already_untarred.append(core_archive_untarred_directory_hm_pattern.search(f).group(1))
                except subprocess.CalledProcessError as e:
                    print "<p>unable to untar the directory since %s</p>" %str(e)
                    sys.stdout.flush()
                    pass
                
       

#    print "<p>=================================================================================="
    print "<p>Core Archive Directories Untarred Successfully</p>\n"
    print "</html>"
    sys.stdout.flush()

    return core_directories_already_untarred


def get_version_and_build(core_dir, path_to_core_archive_directory):
    
    
    version_pattern= re.compile('[0-9]{2}\.[0-9]{1,2}\.[0-9]{1,2}')
    build_pattern = re.compile('\d{4}')

    with open(path_to_core_archive_directory+core_dir+'/VERSION','r') as fp:
        version_list = fp.readlines()

    for line in version_list:
        if line.find('Version') != -1:
            version = version_pattern.search(line).group(0)
        if line.find('build') != -1:
            build = build_pattern.search(line).group(0)

    return (version,build)  


def get_image_directory_with_version_build(version,build, path_to_core_archive_directory):
    
    MNT_REL_BUILDS = '/mnt/rel-builds/'
    MAKE_SE_DIR = path_to_core_archive_directory+'avi_se_'+version

    if not os.path.exists(path_to_core_archive_directory+'avi_se_'+version):
        try:
            os.mkdir(MAKE_SE_DIR)
        except OSError:
            print "<p>unable to create the directory with name 'avi_se', please check if you have enough permissions</p>"
            sys.stdout.flush()
            exit(0)


    ls_dir = os.listdir(MNT_REL_BUILDS+version+'/nightly-build-'+version+'-'+build+'/')
    

    for f in ls_dir:
        if f.find('avi_se.tar.gz') != -1:
            if not os.path.exists(path_to_core_archive_directory+'avi_se_'+version+'/'+'opt/avi/'):
                try:
                    subprocess.check_call(['tar','-xzvf',MNT_REL_BUILDS+version+'/nightly-build-'+version+'-'+build+'/'+f,'-C',path_to_core_archive_directory+'avi_se_'+version])
                except subprocess.CalledProcessError as e:
                    print "<p>unable to untar the directory since %s</p>" % str(e)
                    sys.stdout.flush()
                    exit(0)


def generate_bt_with_core_and_symbol_files(core_directories_after_untar, path_to_core_archive_directory, case_number):
    
    se_agent_pattern = re.compile('se_agent\.\d+\.\d+\.core$')
    se_dp_pattern    = re.compile('se_dp\.\d+\.\d+\.core$')
    se_log_agent_pattern    = re.compile('SeLogExport\.\d+\.\d+\.core$')
    generic_core_pattern = re.compile('core\.\d+$')
    get_symbol_from_generic_core_pattern = re.compile('(se_dp|se_agent|se_log_agent|se_hm)')
    oldest_core_pattern = re.compile('(se_dp|se_agent|se_log_agent|core|se_hm|SeLogExport)\.\d+\.(\d+)\.stack_trace')
    previous_version = current_version = ''
    
#    print core_directories_after_untar
 

    for d in core_directories_after_untar:
        version, build = get_version_and_build(d,path_to_core_archive_directory)
        list_dir = os.listdir(path_to_core_archive_directory+d)
        core_file_location = path_to_core_archive_directory+d
        stack_traces = [f for f in os.listdir(path_to_core_archive_directory+d) if f.endswith('stack_trace')]
        stack_traces = sorted(stack_traces, key = lambda x: oldest_core_pattern.search(x).group(2))
        
        if len(stack_traces):
            function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_traces[0])
            core_file = os.path.basename(path_to_core_archive_directory+d+'/'+stack_traces[0])
#            print function_list
            
            if (function_list and signal):
                crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)
                if not jira_id:
                    print """<p>No Matching Crash Signature found in the Database.
                             Creating a New Jira Ticket with the Contents of Core File</p>"""
                    sys.stdout.flush()         
                    jira_id, status =  utils.create_jira_ticket(crash_function,contents,version,build,func_list,signal,core_file_location,case_number)
                    print "<p>Jira Ticket %s for Crash %s with Crash Function %s is Successfully Created</p>" % (jira_id, core_file, crash_function)
                    sys.stdout.flush()
                    utils.display_results_of_new_jira_in_tabular_format(core_file, crash_function, jira_id, status)

                else:
                    utils.display_results_in_tabular_format(core_file, crash_function, jira_id, status)

            else:
                print "<p>The Core File: %s is Corrupted, Please perform manual analysis on the Core</p>" % (core_file)
                sys.stdout.flush()

            if len(stack_traces[1:]):
                for stack_trace in stack_traces[1:]:
                    function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_trace)
                    if (function_list and signal):
                        crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)

                        if (jira_id and status != 'Resolved' or status != 'Closed'):
                            if not os.path.exists(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added'):
                                print "<p>Found Additional Core Files in the Same Core Archive Directory, Adding the Stack Traces as Comments in the Parent Jira Ticket</p>"
                                utils.add_jira_comment(jira_id, contents,core_file_location)
                                ft = open(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added', 'w')
                                ft.close()
                    else:
                        print "<p>The Core File: %s is Corrupted, Please perform manual analysis on the Core</p>" % (stack_trace)
                        sys.stdout.flush()
                    

        else:
            if os.path.exists(path_to_core_archive_directory+d+'/VERSION'):
                version, build = get_version_and_build(d,path_to_core_archive_directory)
                current_version = version
                if previous_version != current_version:
                    print "<p>Trying to Fetch the Build Directory for Version: %s</p>" % (version)
                    sys.stdout.flush()
                    get_image_directory_with_version_build(version,build,path_to_core_archive_directory)
                    previous_version = current_version
                 
                for core_file in list_dir:
                    if se_agent_pattern.search(core_file):
                        core_stack = core_file.replace('core','stack_trace')
                        fp = open(path_to_core_archive_directory+d+'/'+core_stack , 'wt+')
                        print "<p>==============================Generating BT for Core %s==========================</p>" % core_file
                        sys.stdout.flush()
                        try:
                                child = pexpect.spawn('gdb '+path_to_core_archive_directory+'avi_se_'+version+'/'+'opt/avi/bin/se_agent '+path_to_core_archive_directory+d+'/'+core_file,timeout = 600)
                                child.logfile_read = fp
                                child.expect_exact('(gdb)')
                                child.sendline('set pagination off')
                                child.expect_exact('(gdb)')
                                child.sendline('bt')
                                child.expect_exact('(gdb)')
                                child.sendcontrol('d')
                        except pexpect.TIMEOUT:
                                print "<p>BT Generation Timed Out</p>"
                                sys.stdout.flush()
                                child.sendcontrol('d')
                                

                        stack_traces = [f for f in os.listdir(path_to_core_archive_directory+d) if f.endswith('stack_trace')]
                        stack_traces = sorted(stack_traces, key = lambda x: oldest_core_pattern.search(x).group(2))
                        
                        if len(stack_traces):
                            function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_traces[0])
                            core_file = os.path.basename(path_to_core_archive_directory+d+'/'+stack_traces[0])
                            
                            
                            if (function_list and signal):
                                crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)
                                if not jira_id:
                                    print """<p>No Matching Crash Signature found in the Database.
                                             Creating a New Jira Ticket with the Contents of Core File</p>"""
                                    sys.stdout.flush()         
                                    jira_id, status =  utils.create_jira_ticket(crash_function,contents,version,build,func_list,signal,core_file_location,case_number)
                                    print "<p>Jira Ticket %s for Crash %s with Crash Function %s is Successfully Created</p>" % (jira_id, core_file, crash_function)
                                    sys.stdout.flush()
                                    utils.display_results_of_new_jira_in_tabular_format(core_file, crash_function, jira_id, status)

                                else:
                                    utils.display_results_in_tabular_format(core_file, crash_function, jira_id, status)

                            else:
                                print "<p>The Core File: %s is Corrupted, Please perform manual analysis on the Core</p>" % (core_file)
                                sys.stdout.flush()

                            if len(stack_traces[1:]):
                                for stack_trace in stack_traces[1:]:
                                    function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_trace)
                                    if (function_list and signal):
                                        crash_function, _, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)

                                        if (jira_id and status != 'Resolved' or status != 'Closed'):
                                            print "<p>Found Additional Core Files in the Same Core Archive Directory, Adding the Stack Traces as Comments in the Parent Jira Ticket</p>"
                                            sys.stdout.flush()
                                            if not os.path.exists(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added'):
                                                utils.add_jira_comment(jira_id, contents,core_file_location)
                                                ft = open(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added', 'w')
                                                ft.close()
                                    else:
                                        print "<p>The Core File: %s is Corrupted, Please perform manual analysis on the Core</p>" % (stack_trace)
                                        sys.stdout.flush()
                        

                        fp.close()


                    elif se_dp_pattern.search(core_file):
                        core_stack = core_file.replace('core','stack_trace')
                        fp = open(path_to_core_archive_directory+d+'/'+core_stack , 'wt+')
                        
                        print "<p>==============================Generating BT for Core %s==========================</p>" % core_file
                        sys.stdout.flush()
                        try:
                                child = pexpect.spawn('gdb '+path_to_core_archive_directory+'avi_se_'+version+'/'+'opt/avi/bin/se_dp '+path_to_core_archive_directory+d+'/'+core_file,timeout = 600)
                                child.logfile_read = fp
                                child.expect_exact('(gdb)')
                                child.sendline('set pagination off')
                                child.expect_exact('(gdb)')
                                child.sendline('bt')
                                child.expect_exact('(gdb)')
                                child.sendcontrol('d')
                        except pexpect.TIMEOUT:
                                print "<p>BT Generation Timed Out</p>"
                                sys.stdout.flush()
                                child.sendcontrol('d')
                                

                        stack_traces = [f for f in os.listdir(path_to_core_archive_directory+d) if f.endswith('stack_trace')]
                        stack_traces = sorted(stack_traces, key = lambda x: oldest_core_pattern.search(x).group(2))
                        
                        if len(stack_traces):
                            function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_traces[0])
                            core_file = os.path.basename(path_to_core_archive_directory+d+'/'+stack_traces[0])
                            
                            
                            if (function_list and signal):
                                crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)
                                if not jira_id:
                                    print """<p>No Matching Crash Signature found in the Database.
                                             Creating a New Jira Ticket with the Contents of Core File</p>"""
                                    sys.stdout.flush()         
                                    jira_id, status =  utils.create_jira_ticket(crash_function,contents,version,build,func_list,signal,core_file_location,case_number)
                                    print "<p>Jira Ticket %s for Crash %s with Crash Function %s is Successfully Created</p>" % (jira_id, core_file, crash_function)
                                    sys.stdout.flush()
                                    utils.display_results_of_new_jira_in_tabular_format(core_file, crash_function, jira_id, status)

                                else:
                                    utils.display_results_in_tabular_format(core_file, crash_function, jira_id, status)

                            else:
                                print "<p>The Core File: %s is Corrupted, Please perform manual analysis on the Core</p>" % (core_file)
                                sys.stdout.flush()

                            if len(stack_traces[1:]):
                                for stack_trace in stack_traces[1:]:
                                    function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_trace)
                                    if (function_list and signal):
                                        crash_function, _, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)

                                        if (jira_id and status != 'Resolved' or status != 'Closed'):
                                            print "<p>Found Additional Core Files in the Same Core Archive Directory, Adding the Stack Traces as Comments in the Parent Jira Ticket</p>"
                                            sys.stdout.flush()
                                            if not os.path.exists(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added'):
                                                utils.add_jira_comment(jira_id, contents,core_file_location)
                                                ft = open(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added', 'w')
                                                ft.close()
                                    else:
                                        print "<p>The Core File: %s is Corrupted, Please perform manual analysis on the Core</p>" % (stack_trace)
                                        sys.stdout.flush()
                        

                        fp.close()


                    elif se_log_agent_pattern.search(core_file):
                        core_stack = core_file.replace('core','stack_trace')
                        fp = open(path_to_core_archive_directory+d+'/'+core_stack , 'wt+')
                        print "==================================================================================\n"
                        print "==============================Generating BT for Core %s==========================\n" % core_file
                        print "==================================================================================\n"
                        try:
                                child = pexpect.spawn('gdb '+path_to_core_archive_directory+'avi_se_'+version+'/'+'opt/avi/bin/se_log_agent '+path_to_core_archive_directory+d+'/'+core_file,timeout = 600)
                                child.logfile_read = fp
                                child.expect_exact('(gdb)')
                                child.sendline('set pagination off')
                                child.expect_exact('(gdb)')
                                child.sendline('bt')
                                child.expect_exact('(gdb)')
                                child.sendcontrol('d')
                                print "==================================================================================\n"
                        except pexpect.TIMEOUT:
                                print "BT Generation Timed Out\n"
                                child.sendcontrol('d')
                                print "==================================================================================\n"


                        stack_traces = [f for f in os.listdir(path_to_core_archive_directory+d) if f.endswith('stack_trace')]
                        stack_traces = sorted(stack_traces, key = lambda x: oldest_core_pattern.search(x).group(2))
                        
                        if len(stack_traces):
                            function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_traces[0])
                            core_file = os.path.basename(path_to_core_archive_directory+d+'/'+stack_traces[0])
                            
                            
                            if (function_list and signal):
                                crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)
                                if not jira_id:
                                    print """No Matching Crash Signature found in the Database.
                                             Creating a New Jira Ticket with the Contents of Core File\n"""
                                    jira_id, status =  utils.create_jira_ticket(crash_function,contents,version,build,func_list,signal,core_file_location,case_number)
                                    print "\nJira Ticket %s for Crash %s with Crash Function %s is Successfully Created\n" % (jira_id, core_file, crash_function)
                                    utils.display_results_of_new_jira_in_tabular_format(core_file, crash_function, jira_id, status)

                                else:
                                    utils.display_results_in_tabular_format(core_file, crash_function, jira_id, status)

                            else:
                                print "The Core File: %s is Corrupted, Please perform manual analysis on the Core\n" % (core_file)

                            if len(stack_traces[1:]):
                                for stack_trace in stack_traces[1:]:
                                    function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_trace)
                                    if (function_list and signal):
                                        crash_function, _, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)

                                        if (jira_id and status != 'Resolved' or status != 'Closed'):
                                            print "Found Additional Core Files in the Same Core Archive Directory, Adding the Stack Traces as Comments in the Parent Jira Ticket\n"
                                            if not os.path.exists(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added'):
                                                utils.add_jira_comment(jira_id, contents,core_file_location)
                                                ft = open(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added', 'w')
                                                ft.close()
                                    else:
                                        print "The Core File: %s is Corrupted, Please perform manual analysis on the Core\n" % (stack_trace)
                
                            
                        fp.close()


                    elif generic_core_pattern.search(core_file):
                            ctime = str(int(os.stat(path_to_core_archive_directory+d+'/'+core_file).st_ctime))
                            fp = open(path_to_core_archive_directory+d+'/'+core_file+'.'+ctime+'.stack_trace' , 'wt+')
                            try:
                                output = subprocess.check_output('gdb -ex quit --core='+path_to_core_archive_directory+d+'/'+core_file+' | grep -i generated',shell = True)
                            except subprocess.CalledProcessError as e:
                                print "unable to execute the command since %s" % str(e)
                                exit(0)

                            symbol_file = get_symbol_from_generic_core_pattern.search(output).group(1)
                            if symbol_file != -1:
                                print "==================================================================================\n"
                                print "==============================Generating BT for Core %s==========================\n" % core_file
                                print "==================================================================================\n"
                                try:
                                        child = pexpect.spawn('gdb '+path_to_core_archive_directory+'avi_se_'+version+'/'+'opt/avi/bin/'+symbol_file+' '+path_to_core_archive_directory+d+'/'+core_file, \
                                                              timeout = 600)
                                        child.logfile_read = fp
                                        child.expect_exact('(gdb)')
                                        child.sendline('set pagination off')
                                        child.expect_exact('(gdb)')
                                        child.sendline('bt')
                                        child.expect_exact('(gdb)')
                                        child.sendcontrol('d')
                                        print "==================================================================================\n"
                                except pexpect.TIMEOUT:
                                        print "BT Generation Timed Out\n"
                                        child.sendcontrol('d')
                                        print "==================================================================================\n"
                                                                                                                                                                                                                                                
                            stack_traces = [f for f in os.listdir(path_to_core_archive_directory+d) if f.endswith('stack_trace')]
                            stack_traces = sorted(stack_traces, key = lambda x: oldest_core_pattern.search(x).group(2))
            
                            if len(stack_traces):
                                function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_traces[0])

                                if (function_list and signal):
                                    crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)
                                    if not jira_id:
                                        print """No Matching Crash Signature found in the Database.
                                                 Creating a New Jira Ticket with the Contents of Core File\n"""
                                        jira_id, status =  utils.create_jira_ticket(crash_function,contents,version,build,func_list,signal,core_file_location,case_number)
                                        print "\nJira Ticket %s for Crash %s with Crash Function %s is Successfully Created\n" % (jira_id, core_file, crash_function)
                                        utils.display_results_of_new_jira_in_tabular_format(core_file, crash_function, jira_id, status)
                                    else:
                                        utils.display_results_in_tabular_format(core_file, crash_function, jira_id, status)

                                else:
                                    print "The Core File: %s is Corrupted, Please perform manual analysis on the Core\n" % (core_file)

                                if len(stack_traces[1:]):
                                    for stack_trace in stack_traces[1:]:
                                        function_list, signal, contents = utils.get_function_list_signal_from_stack_trace(path_to_core_archive_directory+d+'/'+stack_trace)
                                        if (function_list and signal):
                                            crash_function, jira_id, status, func_list = utils.check_for_duplicates_in_db(function_list, signal)

                                            if (jira_id and status != 'Resolved' or status != 'Closed'):
                                                print "Found Additional Core Files in the Same Core Archive Directory, Adding the Stack Traces as Comments in the Parent Jira Ticket\n"
                                                if not os.path.exists(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added'):
                                                    utils.add_jira_comment(jira_id, contents,core_file_location)
                                                    ft = open(path_to_core_archive_directory+d+'/'+stack_trace+'_jira_comment_added', 'w')
                                                    ft.close()
                                        else:
                                            print "The Core File: %s is Corrupted, Please perform manual analysis on the Core\n" % (core_file)
                            fp.close()


def main():

    if not len(sys.argv[1:]):
        usuage()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path_to_core_dir",required = True, help = "The Location of the Core Archive Directories")
    parser.add_argument("-c", "--case_num", help = "The Salesforce Case Number", default= None)

    args = parser.parse_args()

    if  args.case_num:
        case_number = args.case_num

    if args.path_to_core_dir:
        path_to_core_archive_directory = args.path_to_core_dir
        path_to_core_archive_list = path_to_core_archive_directory.split('/')
        if path_to_core_archive_list[-1] != '':
            path_to_core_archive_directory = path_to_core_archive_directory+'/'
        core_directories_after_untar = untar_core_directories(path_to_core_archive_directory)
        generate_bt_with_core_and_symbol_files(core_directories_after_untar,path_to_core_archive_directory,case_number)


if __name__ == '__main__':
        main()


