# -*- coding: utf-8 -*-
import scrapy


class RiabizSpider(scrapy.Spider):
    name = "riabiz"
    allowed_domains = ["riabiz.com"]
    url_hash = {
        "Asset Custodian":"http://www.riabiz.com/d?cat=64270",
    }

    start_urls = url_hash.values()


    def normalize(self, response, type):
        try:
          blob = response.xpath('//div[@id="'+type + '"]').extract()[0]
          url = ''
          if response.xpath('//div[@id="'+type + '"]/a/@href').extract() != []:
            url = str(response.xpath('//div[@id="'+type + '"]/a/@href').extract()[0])
          result = []
          ignore_list = ['',"\n",'\n']
          new_list = []
          for e in blob.split("\t")[1:-1]:
              my_str = str(e).strip()
              if my_str == '':
                  continue
              if "<br>" in my_str:
                  for i in my_str.split("<br>"):
                      if i == '':
                          continue
                      if '<a href=' in i:
                          result.append(url)
                          continue
                      else:
                        result.append(i)
                  continue    
              result.append(my_str)    
          return "$$$$$".join(result)    
        except Exception, e:
          print str(e)  

    def parse(self, response):
        url_hash = {
            "Asset Custodian":"http://www.riabiz.com/d?cat=64270",
            # "Compliance Expert": "http://www.riabiz.com/d?cat=64274",
            # "Document Management": "http://www.riabiz.com/d?cat=17060821", 
            # "Financial Planning Software": "http://www.riabiz.com/d?cat=63400",
            # "Performance Reporting": "http://www.riabiz.com/d?cat=2116007",
            # "Portfolio Management System": "http://www.riabiz.com/d?cat=87191"
        }

        filename = "_"
        for name, url in url_hash.iteritems():
            if url == response.url:
                filename = "_".join(name.split(" "))

        firms = response.xpath('//td[@class="dir-toc-title"]')
        with open(filename, 'wb') as f:
          # f.write("firm_name\tdirectory_url\n")
          for idx, firm in enumerate(firms):
              if idx > 6:
                  break
              # item = RiabizDirItem()
              # item['firm_name'] = firm.xpath('h3/a/text()').extract()[0].encode('ascii', 'ignore').strip()
              # yield item
              directory_url = firm.xpath('h3/a/@href').extract()[0].encode('ascii', 'ignore').strip()
              yield scrapy.Request(directory_url, callback=self.parse_dir_contents)
              # f.write(str(firm_name) + "\t" + str(directory_url) +"\n")

    def parse_dir_contents(self, response):
        print self.normalize(response, 'corporate_info')
        print self.normalize(response, 'ria_info')
        # company_info_blob = response.xpath('//div[@id="corporate_info"]').extract()[0].split("\t")
        # ria_info_blob = response.xpath('//div[@id="ria_info"]').extract()[0].split("\t")
        # print company_info_blob 
        # for sel in response.xpath('//ul/li'):
        #     item = DmozItem()
        #     item['title'] = sel.xpath('a/text()').extract()
        #     item['link'] = sel.xpath('a/@href').extract()
        #     item['desc'] = sel.xpath('text()').extract()
        #     yield item