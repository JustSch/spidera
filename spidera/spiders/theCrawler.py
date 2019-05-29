import scrapy
from scrapy.linkextractors import LinkExtractor
from collections import Counter
from spidera.site_item import site_item
import lxml.etree
import lxml.html

class theCrawler(scrapy.Spider):
    name = "theCrawler"
    start_urls = ['http://www.nostalgianerd.com/']

    def parse(self, response):
        
        yield self.parse_items(response)
       
        
        link_extractor = LinkExtractor( attrs=('href')).extract_links(response)

        for Link in link_extractor[:100]: 
           
           yield scrapy.Request(
                response.urljoin(Link.url),
                callback=self.parse
            )

    def parse_items(self, response):
        last_modified = response.headers.get('Last-Modified')
        title = response.xpath('//title/text()').get()
        if "\n" in title:
            title =title.strip("\n")
        url = response.url
        
        word_list = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(word_list, lxml.etree.Comment, "script", "head")
   
        
        keyword_list = lxml.html.tostring(word_list, method="text", encoding="unicode").split()
        
        description = response.xpath('//meta[@name=\'description\']/@content').get()
        page = response.url.split("/")[-2]
        
        
        common_words = Counter(keyword_list).most_common(5)
        
        items = site_item()
        
        items['link_title'] = title
        if (description == None):
            description = response.xpath('//head/meta[@property=\'og:description\']/@content').get()
        if (description == ''):
            description = "unable to retrieve description"
        if (last_modified == None):
            last_modified = '1970-01-01 12:12:12'
        
        items['link_description'] = description
        items['link_url'] = url
        items['last_update'] = last_modified
        
        
        items['word1'] = common_words[0][0].upper()
        items['word2'] = common_words[1][0].upper()
        items['word3']= common_words[2][0].upper()
        items['word4']= common_words[3][0].upper()
        items['word5']= common_words[4][0].upper()

        return items
