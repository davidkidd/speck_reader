speck_reader
============

A simple, server-side RSS merger and reader

* Fast and simple
* Create and view 'streams' that contain only a small number of related RSS feeds, sorted by date
* Static HTML pages, accessible by any device
* No JavaScript or CSS trickery

Caveats
-------

I wrote this a while ago and without too much understanding of Python and CGI.

It's designed for personal use. You can make feeds public and protect them with a PIN, but this is very basic protection.

The timezone is set to Australia/Sydney

Requirements
------------

* Know how to set up a web server to run Python scripts
* Python 2.6 (requires lxml)

Installation
------------

* Add edit.py and save.py to your cgi-bin directory
* Put rss_merge.py somewhere so it can be accessed by the server, but not in the cgi-bin directory
* Create a stream by going to your_server/cgi-bin/edit.py
* Save it and bookmark the link. The link will only update when rss_merge.py is executed.
* Create a cron job to run rss_merge.py however often you like
