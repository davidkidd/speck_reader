#!/usr/bin/env python

import os
import cgi
import cgitb
import uuid
cgitb.enable()

form = cgi.FieldStorage()

def unique_UUID (id):
    try:
        open(id, 'r')
        return False
    
    except:
        return True

print 'Content-type: text/html\r\n\r'
print '''
<html>
<head>
  <link rel="stylesheet" type="text/css" href="../style.css"/>
</head>
<body>
<div class="entry">
<h2 class="title">Edit</h2>
<a href="edit.py">Create new</a>
<form action="save.py" method="post">
'''

feeds = []

stream_id = None

stream_pin = None

stream_title = None

pin_match = False

new_stream = True

if form.getvalue('stream'):
    
    new_stream = False
     
    os.chdir('../')
    
    stream_id = form.getvalue('stream')
    
    r_file = open(form.getvalue('stream') + '.feeds', 'r')
    
    r_file_lines = r_file.readlines()
 
    try:
        stream_pin = r_file_lines[1].strip()
        
        stream_title = r_file_lines[0].strip()
         
        feeds = r_file_lines[2:]
     
    except:
         
        print 'Stream does not exist. Create a new one.'
    
    if stream_id:
        
        print '<p>ID: ' + stream_id + '</p>'
        
    r_file.close()
    
else:
    stream_id = str(uuid.uuid4())

    while not unique_UUID(stream_id):
        stream_id = str(uuid.uuid4())
  
    print '<p>ID: ' + stream_id + '</p>'

feed_count = len(feeds)

print '<div class="title_pass_field_block">'

if new_stream:
    print '<label>Stream title</label><input type="text" name="title" value="Untitled">'
    print '<label>Optional PIN</label><input type="text" size="60" name="pin" value="">'
    print '<input type="hidden" name="new" value="1">'
    
else:
    print '<label>Stream title</label><input type="text" name="title" value="{0}">'.format(stream_title)
    
    locked = True
    
    pin_label = "PIN required"
    
    if (stream_pin.strip() == "null"):
        locked = False
        pin_label = "Create PIN"
        
    print '<label>{0}</label><input type="text" name="pin" value="">'.format(pin_label)
    print '<input type="hidden" name="new" value="0">'
    
    if locked:
        print '<label>Change PIN</label><input type="text" name="change_pin" value="">'.format(pin_label)
    
print '</div>'

print '<div style="margin-bottom: 20px; clear:both"/><br />'

for row in range(10):
    existing = ""
    if (feed_count >= row + 1):
        existing = feeds[row].strip()
    print '<input type="text" size="60" name="{0}" value="{1}">'.format(row, existing)
    print '<br />'

print '<br /><br /><input type="submit" value="Save" />'
print '<input type="hidden" name="stream" value="{0}">'.format(stream_id)
print '</form>'
print '</div>'
print '<br />'
print '<div class="caveat">'
print '<p>The PIN is a simple block to stop someone editing the stream if you choose to share the stream link. If you forget your PIN, there is no way to retrieve it unless you can access stream files on the server.</p>'
print '<p>To remove a PIN, enter "null" without the quotation marks.</p>'
print '</div'
print '</html>'
