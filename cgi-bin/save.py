#!/usr/bin/env python

import os
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

def get_new_stream_stub(title):
    
    html = '''
<html>
<head>
  <link rel="stylesheet" type="text/css" href="../style.css"/>
<title>{0}</title>
</head>
<body>
<div class="entry">
<br /><br /><p align="center">Generating new stream. Try again later.</p>
</div>
</body>
</html>
'''.format(title)
    return html
    

def write_to_file(fname, title, supplied_pin):
    
    with open(form.getvalue('stream') + '.feeds', 'w') as r_file:
        
        r_file.write(title.strip()+"\n")
        
        r_file.write(supplied_pin + "\n")
                
        for i in range(0, 10):
            try:
                r_file.write(form.getvalue(str(i)).strip()+"\n")
            except:
                pass
        
        print '<div class="entry">'
        print '<h2 class="title">Saved</h2>'
        print '<p><a href="{0}">Stream link</a></p>'.format("../" + form.getvalue('stream').strip() + ".html")
        print '</div>'
    

print 'Content-type: text/html\r\n\r'
print '''
<html>
<head>
  <link rel="stylesheet" type="text/css" href="../style.css"/>
</head>
<body>
'''

if form.getvalue('stream'):
    
    os.chdir('../')
    
    supplied_pin = form.getvalue('pin')
    if not supplied_pin:
        supplied_pin = "null"
    
    new_stream = True
    
    if (form.getvalue('new') == "0"):
        new_stream = False
    
    r_file = None
    
    if new_stream:
        
        write_to_file(form.getvalue('stream'), form.getvalue('title'), supplied_pin)
    
    else:
        r_file = open(form.getvalue('stream') + '.feeds', 'r')
    
        existing_pin = r_file.readlines()[1].strip()
        
        if (supplied_pin == existing_pin):
        
            if form.getvalue('change_pin'):
                 
                write_to_file(form.getvalue('stream'), form.getvalue('title'), form.getvalue('change_pin'))
            else:
                write_to_file(form.getvalue('stream'), form.getvalue('title'), supplied_pin)
            
        elif existing_pin == "null" and supplied_pin != "null":
            
            write_to_file(form.getvalue('stream'), form.getvalue('title'), supplied_pin)
               
        else:
            print '<div class="entry">'
            
            print '<h2 class="title">Wrong PIN</h2>'
            
            print '<p><a href="javascript:history.go(-1)">Try again</a>'
            
            print '<p><a href="../{0}.html">Back to stream</a>'.format(form.getvalue('stream').strip())
            
            print '</div>'
    
    
    if new_stream:
        
        with open(form.getvalue('stream') + '.html', 'w') as new_html:
        
            new_html.write(get_new_stream_stub(form.getvalue('title')))
        
else:
    print '<p>Could not find stream ID or PIN number.</p>'

print '''
</body>
</html>
'''

