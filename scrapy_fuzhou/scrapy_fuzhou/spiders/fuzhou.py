import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from scrapy_fuzhou.items import ScrapyFuzhouItem
import urllib.request
from lxml import etree
import re

class FuzhouSpider(scrapy.Spider):
    name = "fuzhou"
    allowed_domains = ["fjrclh.fzu.edu.cn"]
    start_urls = ["http://fjrclh.fzu.edu.cn/cmss/sxzp?page=1.html"]
    base_url = "http://fjrclh.fzu.edu.cn/cmss/sxzp?page="
    page = 1
    # rules = (Rule(LinkExtractor(allow=r"/cmss/sxzp?page=\d+\.html"), callback="parse_item", follow=False),)
    def parse(self, response):
        url_list = response.xpath('//div[@class="am-tab-panel"]/ul/li/a/@href').extract()
        for url in url_list:
            url = "http://fjrclh.fzu.edu.cn/" + url[3:]
            print(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'
            }
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')
            tree = etree.HTML(content)
            title = tree.xpath('//div[@class="am-tab-panel"]/div/span/text()')[0].strip()
            # print(title)
            date = tree.xpath('//div[@class="am-tab-panel"]/div/div/div/span/text()')[0].strip()
            # print(date)
            try:
                emailRegex = r"[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}"
                email = re.search(emailRegex,content).group()
                # print(email)            
            except Exception as e:
                email = None
            # nameRegex = r'[\u4e00-\u9fa5]{2,3}'
            # name = re.findall(nameRegex,content)
            # print(name)
            # webRegex = re.compile(r'https?:\/\/(\w+\.)+\w{2,3}\/')
            # web = re.search(webRegex,content)
            # print(web)
        
            telRegex = re.compile(r'\d{11}\d*|\d{3,4}-\d{8}\d*')
            matches = re.findall(telRegex,content)
            tel = None
            for match in matches:
                if '-' in match:
                    tel = match.replace('-','')
                    if len(tel) == 11 or len(tel) == 12:
                        tel = match
                else:    
                    if len(match) == 11:
                        tel = match
            message = ScrapyFuzhouItem(title=title,date=date,email=email,tel=tel)
            yield message
        if self.page < 3:
            self.page += 1
            url = self.base_url + str(self.page)
            yield scrapy.Request(url=url, callback=self.parse)