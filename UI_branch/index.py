#! /usr/bin/env python

import cgitb
cgitb.enable()

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
                   <header class="w3-container" style="padding:110px;background-color:#2a2a2d;color:white">
                                           <div class="w3-container" style="padding-top:10px;float:left">
                                                        <img src="https://avinetworks.com/client/logo.png" alt="Avi Networks">
                                                                    </div>
                           <div class="w3-container w3-center"><h1>SE Core Analyzer</h1></div>
                           <h2><div class="w3-bar w3-deep-orange" style="color:white"></div></h2
                   </header>
                     
                                                                                    
                   <form name="parse_form" action="/crash-analysis/parse_form.py"  method="POST">
                     <label for="core_dir_path">Core Directory Path:</label>
                       <input type="text" id="core_dir_path" name="core_dir_path" value=" " maxlength="200" >
                         <label for="case_num">Salesforce Case Number:</label>
                           <input type="text" id="case_num" name="case_num" value=" " maxlength="10" >
                           <input type="submit" value="Submit">
                           </form>
                  <footer class="w3-container" style="padding:130px;background-color:#2a2a2d;color:white"></footer>         
                          </body>
                    </html> """

print html_data                                                                
                

