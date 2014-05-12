# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import urllib
import urlparse
import hashlib
import re
import socket
import sys
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

true_socket = socket.socket
source_ip = '127.0.0.1'

output = open('D:\\outputTT.txt','w')

true_socket = socket.socket
source_ip = '127.0.0.1'
def bound_socket(*a,  **k):
    sock = true_socket(*a, **k)
    log.msg('Outbound IP: ' + source_ip)
    sock.bind((source_ip, 0))
    return sock

class ChinagsmSpider(CrawlSpider):
    name = 'chinagsm'
    allowed_domains = ['china-gsm.ru']
    start_urls = [
        'http://china-gsm.ru/posts/novosti/',
        'http://china-gsm.ru/forum/'
    ]

    rules = (
        # Extract links
        # and follow links from them (since no callback means follow=True by default).
        Rule(SgmlLinkExtractor(allow=(r'posts/novosti/\?p=\d+$', ), )),
        Rule(SgmlLinkExtractor(allow=(r'forum/forum/\d+/', ), )),

        # Extract links and parse them with the spider's method
        Rule(SgmlLinkExtractor(allow=(r'posts/novosti/[-_0-9a-zA-Z]+', )), callback='parse_item_page'),
        Rule(SgmlLinkExtractor(allow=(r'forum/topic/\d+/', )), callback='parse_forum_page'),
    )

    def __init__(self, total_num_jobs='2', job_no='0', ip='127.0.0.1',  *args, **kwargs):
        # Set up outbound IP
        global source_ip
        source_ip = ip
        #socket.socket = bound_socket
        self.job_no = int(job_no)
        self.total_num_jobs = int(total_num_jobs)
        super(ChinagsmSpider, self).__init__(*args, **kwargs)

    def parse_forum_page(self, response):        
        print response.url()

        sel = Selector(response)
        sites = sel.xpath('//@href').extract()
        print sites
        for site in sites:
            print site
            output.write(site)
            output.flush()
            #yield Request(site)