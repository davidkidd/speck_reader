#!/usr/bin/env python

'''
Merges one or more RSS feeds together, sorted by date.
'''

import feedparser
import time
from datetime import datetime, timedelta
from lxml import etree
import lxml.html
import os
import pytz

STREAM_LOCATION = "/var/www"

DATE_FIELDS = ['updated_parsed', 'published_parsed']

MAX_FEEDS = 12

MAX_STORIES_PER_FEED = 12

MAX_HOURS = 24

class Entry:
    def __init__ (self, feed, title, summary, link, timestamp):
        self.feed = feed
        self.title = title
        self.summary = summary
        self.link = link
        self.timestamp = timestamp

def get_streams(directory):
    
    streams = []
    
    os.chdir(directory)
    
    for f in os.listdir("."):
        
        if f.endswith(".feeds"):
            streams.append(f)
            
    return streams

def entry_is_unique(entry, entries):
    for e in entries:
        try:
            if e.link == entry.link:
                return False
            elif e.title == entry.title:
                return False
            elif e['summary_detail']['value'] == entry['summary_detail']['value']:
                return False
        except:
            pass
    
    return True

def get_date(entry, date_fields):
    date = None
        
    for field in date_fields:
        if field in entry.keys():
            date = entry[field]
            break;
    
    local_tz = pytz.timezone ("Australia/Sydney")
    
    if not date:
        date = time.localtime(time.time())
        date = datetime.fromtimestamp(time.mktime(date))
        date = local_tz.localize(date)
    
    else:
        dummy_tz = pytz.timezone ("UTC")
        date = datetime.fromtimestamp(time.mktime(date))
        date = dummy_tz.localize(date)
        date = date.astimezone(local_tz)
        
    return date

def get_local_time():
    
    local = pytz.timezone ("Australia/Sydney")
    
    local_dt = local.localize(datetime.now(), is_dst=True)
    
    return local_dt

def parse_all_feeds(stream):
    
    with open(stream, "r") as stream_file:
        
        feeds = stream_file.readlines()
    
        parsed_feeds = []
        
        print ">> Parsing feeds"
        
        for feed in feeds[2:MAX_FEEDS+2]: #First line in feed file is the IN
            
            print "\nParsing " + feed,
            
            parsed_feed = feedparser.parse(feed)
                        
            print "...as " + parsed_feed['feed']['title']
            
            parsed_feeds.append(parsed_feed)
            
        return parsed_feeds
        
def merge_entries(parsed_feeds, sort=True):
    
    entries = []
    
    print "\n>> Merging entries"
    
    for feed in parsed_feeds:
    
        entries_in_feed = 0
        
        feed['entries'].sort(key = lambda item: get_date(item, DATE_FIELDS), reverse=True)
        
        for entry in feed['entries']:
                
            if (entries_in_feed < MAX_STORIES_PER_FEED):
                
                if entry_is_unique(entry, entries):
                    
                    date = get_date(entry, DATE_FIELDS)
                    
#                     if datetime.now() - datetime.fromtimestamp(time.mktime(date)) < timedelta (hours = MAX_HOURS):
                    if get_local_time() - date < timedelta (hours = MAX_HOURS):
                        
                        new_entry = Entry(feed['feed']['title'],
                                          entry['title_detail']['value'],
                                          entry['summary_detail']['value'],
                                          entry['link'],
                                          date)
                    
                        entries.append(new_entry)
                        
                        entries_in_feed += 1
        
    
    if sort:
        print "\n>> Sorting entries"
        entries.sort(key = lambda item: item.timestamp, reverse=True)
    
    return entries

def prepare_root(stream):
    
    print "\n>> Preparing HTML root"
    
    root = etree.Element("html")
    
    head = etree.SubElement(root, "head")
    
    style = etree.SubElement(head, "link")
    
    style.attrib["rel"] = "stylesheet"
    style.attrib["type"] = "text/css"
    style.attrib["href"] = "style.css"
    
    title = etree.SubElement(head, "title")
    
    try:
        with open(stream, "r") as stream_file:
            title.text = stream_file.readlines()[0]
    
    except:
        title.text = "Untitled"

    
    return root
    
def prepare_body(root, entries, stream):
    
    print "\n>> Preparing HTML body"
    
    body = etree.SubElement(root, "body")
    
    stream_id = stream.replace(".feeds", "")
    
    edit_link_div = etree.SubElement(body, "div")
     
    edit_link = etree.SubElement(edit_link_div, "a", href="/cgi-bin/edit.py?stream={0}".format(stream_id))
    edit_link.attrib["class"] = "edit_link"
    edit_link.text = u"\u2699"
    
    print "\n>> Laying out entries"
    
    for entry in merged_entries:
        body.append(entry_to_html(entry))

def entry_to_html(entry):
    
    #Entry container div
    
    entry_element = etree.Element("div")
    
    entry_element.attrib["class"] = "entry"
    
    #Headline and link
    
    title_element = etree.Element("h2")
    
    link_element = etree.Element("a")
    
    link_element.attrib["href"] = entry.link
    
    link_element.attrib["class"] = "title_link" 
    
    link_element.text = entry.title
    
    title_element.append(link_element)
    
    #Pub text
    
    pub_element = etree.Element("p")
    
    pub_element.attrib["class"] = "publication"
    
    pub_element.text = entry.feed
    
    #Date text
    
    date_element = etree.Element("p")
    
    date_element.attrib["class"] = "date"
    
    date_element.text = entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S %z")
    
    #Summary
    
    summary_element = etree.Element("p")
    
    summary_element.text = lxml.html.fromstring(entry.summary).text_content()
    
    summary_element.attrib["class"] = "summary"
    
    summary_element.tag = "p"
    
    #Append all child elements to entry element
    
    entry_element.append(title_element)
    
    entry_element.append(pub_element)
    
    entry_element.append(date_element)
    
    entry_element.append(summary_element)
    
    return entry_element
    

if __name__ == '__main__':

    streams = get_streams(STREAM_LOCATION)

    for stream in streams:

        parsed_feeds = parse_all_feeds(stream)
        
        merged_entries = merge_entries(parsed_feeds, sort=True)
        
        root = prepare_root(stream)
        
        body = prepare_body(root, merged_entries, stream)
            
        with open(stream.replace(".feeds", ".html"), "w") as f:
            print "\n>> Writing HTML"
            f.write(etree.tostring(root, pretty_print=True))
