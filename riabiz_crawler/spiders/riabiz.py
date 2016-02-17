# -*- coding: utf-8 -*-
import scrapy
import time

url_hash = {
    "Asset Custodian":"http://www.riabiz.com/d?cat=64270",
    # "Compliance Expert": "http://www.riabiz.com/d?cat=64274",
    # "Document Management": "http://www.riabiz.com/d?cat=17060821", 
    # "Financial Planning Software": "http://www.riabiz.com/d?cat=63400",
    # "Performance Reporting": "http://www.riabiz.com/d?cat=2116007",
    # "Portfolio Management System": "http://www.riabiz.com/d?cat=87191"
}
inv_url_hash = {v: k for k, v in url_hash.items()}

class RiabizSpider(scrapy.Spider):
    name = "riabiz"
    allowed_domains = ["riabiz.com"]

    start_urls = url_hash.values()

    def normalize(self, response, blob_class):
        try:
          blob = response.xpath('//div[@id="'+blob_class + '"]').extract()[0]
          url = ''
          if response.xpath('//div[@id="'+blob_class + '"]/a/@href').extract() != []:
            url = str(response.xpath('//div[@id="'+blob_class + '"]/a/@href').extract()[0])
          result = [url]
          ignore_list = ['',"\n",'\n']
          new_list = []
          for e in blob.split("\t")[1:]:
              my_str = str(e).strip()
              if my_str == '' or my_str == '</div>':
                  continue
              if "<br>" in my_str:
                  for i in my_str.split("<br>"):
                      if i == ''  or '<script type=' in i or '</div>' in i:
                          continue
                      if '<a href=' in i:
                          continue
                      else:
                        result.append(i)
              else: 
                result.append(my_str)  
          if blob_class == 'corporate_info':
              firm_name = response.xpath('//div[@class="listing-company-name"]/text()').extract()[0]     
              result.insert(0, firm_name.strip())   
          return "$$$$$".join(result)    
        except Exception, e:
          print str(e)  

    def normalize_etc(self, response):
        result = []
        try:
          for li in response.xpath('//div[@id="etcetera"]/ul/li'):
              result.append(li.extract()[4:-5].replace('<strong>','').replace('</strong>',''))
          return "$$$$$".join(result)    
        except Exception, e:
          print str(e) 

    def parse(self, response):
        firms = response.xpath('//td[@class="dir-toc-title"]')
        for idx, firm in enumerate(firms):
            # if idx > 0:
            #     break
            # item = RiabizDirItem()
            # item['firm_name'] = firm.xpath('h3/a/text()').extract()[0].encode('ascii', 'ignore').strip()
            # yield item
            time.sleep(0.3)
            directory_url = firm.xpath('h3/a/@href').extract()[0].encode('ascii', 'ignore').strip()
            yield scrapy.Request(directory_url, callback=self.parse_dir_contents)
            # f.write(str(firm_name) + "\t" + str(directory_url) +"\n")

    def parse_dir_contents(self, response):
        print inv_url_hash
        line = ""
        ria_blob = ""
        etc_blob = ""
        corporate_info_blob = self.normalize(response, 'corporate_info')
        print corporate_info_blob
        if response.xpath('//div[@id="ria_info"]') != []:
            ria_blob = self.normalize(response, 'ria_info')
        print ria_blob
        if response.xpath('//div[@id="etcetera"]/ul/li') != []:
            etc_blob = self.normalize_etc(response)
        filename = "_"
        # print url_hash
        # url = response.url
        # filename = "_".join(inv_url_hash[url].split(" "))
        # print inv_url_hash[url]
        # print filename     
        with open(filename, 'a') as f:
            f.write(corporate_info_blob + '$$$$$' + ria_blob + '$$$$$' + etc_blob+"\n")

        # company_info_blob = response.xpath('//div[@id="corporate_info"]').extract()[0].split("\t")
        # ria_info_blob = response.xpath('//div[@id="ria_info"]').extract()[0].split("\t")
        # print company_info_blob 
        # for sel in response.xpath('//ul/li'):
        #     item = DmozItem()
        #     item['title'] = sel.xpath('a/text()').extract()
        #     item['link'] = sel.xpath('a/@href').extract()
        #     item['desc'] = sel.xpath('text()').extract()
        #     yield item