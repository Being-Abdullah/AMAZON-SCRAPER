import scrapy
# from scrapy_playwright.page import PageMethod
from time import sleep
# from playwright.async_api import async_playwright
from urllib.parse import urlencode
import json
from random import randint
import whiskyscraper.database
from latest_user_agents import get_latest_user_agents, get_random_user_agent
import random
import asyncio
from datetime import datetime
from scrapy.spidermiddlewares.httperror import HttpError
from whiskyscraper.pipelines import AvailabilityPipeline, ProductPipeline2

class amazonSpider(scrapy.Spider):
    name='amazon_non'
    handle_httpstatus_list = [503]
    header = {
        
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
       }
    custom_settings = {
    'FEEDS': { 'amazon.csv': { 'format': 'csv',}}
    
    }
    found_product=False
    product_value=False
    def start_requests(self):
       
        print("WORKING")
        yield from self.request_asi()
        

       
  
        
        
       
       
   
        
    def request_asi(self):
        asin_list=whiskyscraper.database.read_all_documents_nllproduct()
        print(f"Total asin to scrape {len(asin_list)}")

        for asin_data in asin_list:
           
            
            
            user_agent=random.choice(get_latest_user_agents())
           
            amazon_url = f'https://www.amazon.com/dp/{asin_data["ASIN"]}' 
            #amazon_url = 'https://www.amazon.com/dp/B07F7KGJ83' 
            # amazon_url=asin_data
            print(amazon_url)
                 
          

            yield scrapy.Request(url=amazon_url ,headers={"User-Agent": user_agent, 'dnt': '1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.amazon.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}, callback=self.parse,errback=self.errback,dont_filter = True, meta={'id':asin_data["_id"],'max_retry_times': 300,"proxy": "xxxxxxxxxxx"})
        
        if len(asin_list)>0 and len(asin_list)!=1 :
            print("check --------------------------------------------------------------------------------------------")
            new_asin_list = whiskyscraper.database.check_documents_nllproduct()
            if len(new_asin_list) > 0:
                yield from self.request_asi()  # Recursively call request_asi() to scrape new ASINs

        
    def errback(self, failure):
        request = failure.request
        response = failure.value.response
        object_id = response.meta['id']
        data_list = {'price':None,'discount':None,'last_price':None}
        print('response----------------',response)
        if response.status == 404:
            print('response. status ----------------',response.status)
            # print('object_id',object_id,'product_value',product_value)
            # yield {'url':response.url}
            self.product_value=False
            whiskyscraper.database.update_nllproduct_field_by_id(object_id,data_list,self.product_value)
            
            # self.found_product=True



    
      
    def parse(self , response):
        print('aggent',response.request.headers['User-Agent'])
        object_id = response.meta['id']
        print(object_id)
        data_list = {'price':None,'discount':None,'last_price':None}
        user_agent=random.choice(get_latest_user_agents())
       
        temp_list=[]
        product_price=None
        product_discount=None
        last_price=None
        
        status_check=response.status
       
        # if response.status == 404:
        
        # sleep(10)

        
        
        
        product_title  = response.xpath('//h1[@id="title"]/span[@id="productTitle"]/text()').get()
        
       
        # image_url = image_P.xpath('@src').get()
        print('title',product_title,'price',product_price,'discount',product_discount,'last_price',last_price)
        
        
        
        if product_title:
            product_title = product_title.strip()
            
            product_availability=response.xpath('//div[@id="availability"]/span/span/text()').get()
            if product_availability and 'Currently unavailable' in product_availability :
                print('status1----------------------------------------------------',product_availability)
                
                print('status2----------------------------------------------------',product_availability)
                # yield {'url':response.url,'status':product_availability}
                # yield whiskyscraper.pipelines.AvailabilityPipeline(url=response.url, status=product_availability)
                yield {'url': response.url, 'status': product_availability, 'type': 'availability'}
    
                self.product_value=False
                whiskyscraper.database.update_nllproduct_field_by_id(object_id,data_list,self.product_value)
                
            else:
                product_discount = response.xpath('//div[@style=""]//span[@class="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage"]/text()').get()
                if product_discount is not None:
                    product_price = response.xpath('//div[@id="centerCol"]//div[@style=""]//span[@class="a-price-whole"]/text()').get()
                    last_price = response.xpath('//span[@class="a-price a-text-price" and @data-a-color="secondary"]/span/text()').get()
                else:
                    product_price = response.xpath('//div[@id="centerCol"]//div[@style=""]//span[@class="a-price-whole"]/text()').get()
                if product_price is None:
                    product_price = response.xpath('//div[@id="centerCol"]//span[@class="a-offscreen"]/text()').get()
                print(f"prodouct price:{product_price}")
                if product_price ==" ":
                    print("YESSS")
                    product_price = response.xpath('//div[@id="centerCol"]//span[@class="a-price-whole"]/text()').get()
                print('title',product_title,'price',product_price,'discount',product_discount,'last_price',last_price)
                if 'The price is' in product_price:
                    product_price =''
                if product_price:
                    if not '$' in str(product_price):
                            product_price  = '$'+product_price 
                

                    
                utc_time = datetime.utcnow()
                utc_time_str = utc_time.strftime('%Y-%m-%d %H:%M:%S')
                self.product_value=True
                print('title',product_title,'price',product_price,'discount',product_discount,'last_price',last_price,'utc time',utc_time_str,'pro',self.product_value)
                data_list = {'price':product_price,'discount':product_discount,'last_price':last_price,'utc_time':utc_time_str}
                # yield whiskyscraper.pipelines.ProductPipeline(url=response.url, title="product_title", price=product_price, discount=product_discount, last_price=last_price, utc_time=utc_time_str)
                yield {
                        'url': response.url,
                        'title': "product_title",
                        'price': product_price,
                        'discount': product_discount,
                        'last_price': last_price,
                        'utc_time': utc_time_str,
                        'type': 'product_update'
                    }
                whiskyscraper.database.update_nllproduct_field_by_id(object_id,data_list,self.product_value)
                
            
            
            

        else:
            print("No product title found, retrying...")
            
            # Manually implement retry logic
            if 'retry_times' not in response.meta:
                response.meta['retry_times'] = 1

            else:
                response.meta['retry_times'] += 1
                print(product_title,response.meta['max_retry_times'],response.meta['retry_times'])

            if response.meta['retry_times'] <= 30:  # Retry up to 3 times
                amazon_url = response.url
                max_retry_times=response.meta['max_retry_times']
                
                yield scrapy.Request(
                    url=amazon_url,
                    headers={
                        "User-Agent": user_agent, 
                        'dnt': '1',
                        'upgrade-insecure-requests': '1',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-user': '?1',
                        'sec-fetch-dest': 'document',
                        'referer': 'https://www.amazon.com/',
                        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
                    },
                    callback=self.parse,
                    errback=self.errback,
                    dont_filter=True,
                    meta={
                        
                        'max_retry_times': max_retry_times,
                        'retry_times': response.meta['retry_times'],
                        'id':object_id,
                        "proxy": "xxxxxxxxxxx"
                    }
                )
            else:
                print("Failed to retrieve product title after 3 retries")

        print(product_title)
                 
    def saveData(self,response):
        
        watch_id=response.meta['watch_id']
        watch_pid=response.meta['watch_pid']
        keyword=response.meta['keyword']
        model=response.meta['model']
        exclude=response.meta['exclude']
        date=response.meta['date']
        url=response.meta['url']
       
        yield {'watch_id':watch_id,'watch_pid':watch_pid,'keyword':keyword,'model':model,'exclude':exclude,'date':date,'url':url}
        
        # filename = 'test.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)