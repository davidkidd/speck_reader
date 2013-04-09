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

1. Add edit.py and save.py to your cgi-bin directory
2. Put rss_merge.py somewhere so it can be accessed by the server, but not in the cgi-bin directory
3. Configure rss_merge.py to point at your web server's root directory. This *must* be one level above cgi-bin.
4. Create a stream by going to your_server/cgi-bin/edit.py
5. Save it and bookmark the link. The link will only update when rss_merge.py is executed.
6. The stream file contains the title, PIN (or null if no PIN) and the feeds. The stream file is used by rss_merge.py to generate a corresponding static HTML page for the stream.
7. Create a cron job to run rss_merge.py however often you like
8. rss_merge.py will create HTML files from the information in the stream file.

By default, a server containing one stream will look like this:

	/www/
		/3c9fbc0f-bf14-4f3a-a61e-d13b54bce86f.html
    	/3c9fbc0f-bf14-4f3a-a61e-d13b54bce86f.feeds
    	/cgi-bin/
      		edit.py
      		save.py
