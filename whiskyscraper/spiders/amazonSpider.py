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
from whiskyscraper.pipelines import AvailabilityPipeline, ProductPipeline,ProductPipeline3
import re

class amazonSpider(scrapy.Spider):
    name='amazon'
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
    brand_name=None
    product_name=None
    def start_requests(self):
       
        print("WORKING")
        yield from self.request_asi()
        

       
  
        
        
       
       
   
        
    def request_asi(self):
        asin_list=whiskyscraper.database.read_all_documents()
        print(f"Total asin to scrape {len(asin_list)}")

        for asin_data in asin_list:
           
            
            
            user_agent=random.choice(get_latest_user_agents())
            print('asin ',asin_data)
            amazon_url = f'https://www.amazon.com/dp/{asin_data["ASIN"]}'
            # amazon_url = 'https://www.amazon.com/dp/B09YSWMQSQ'
            # amazon_url=asin_data
            print(amazon_url)
            if asin_data.get('product_name') is None:
                product_name=None

            else:

                product_name=asin_data["product_name"]

            if asin_data.get('brand') is None:
                brand_name=None
            else:
                brand_name=asin_data["brand"]

            if asin_data.get('commission_payout_aff') is None:
                commission_payout=None

            else:

                commission_payout=asin_data["commission_payout_aff"]    

            yield scrapy.Request(url=amazon_url ,headers={"User-Agent": user_agent, 'dnt': '1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.amazon.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}, callback=self.parse,errback=self.errback,dont_filter = True, meta={'id':asin_data["_id"],'commission_payout':commission_payout,'product_name':product_name,'brand_name':brand_name,'max_retry_times': 300,"proxy": "xxxxxxxxxxx"})

        if len(asin_list)>0 and len(asin_list)!=1 :
            print("check --------------------------------------------------------------------------------------------")
            new_asin_list = whiskyscraper.database.check_documents()
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
            # whiskyscraper.database.update_field_by_id(object_id,data_list,self.product_value)
            
            # self.found_product=True



    
      
    def parse(self , response):
        print('aggent',response.request.headers['User-Agent'])
        object_id = response.meta['id']
        productName=response.meta['product_name']
        brandName=response.meta["brand_name"]
        commission_payout=response.meta['commission_payout']
        print(object_id)
        data_list = {'price':None,'discount':None,'last_price':None}
        user_agent=random.choice(get_latest_user_agents())
       
        temp_list=[]
        product_price=None
        product_discount=None
        last_price=None
        asin_pattern = r'/dp/([A-Z0-9]{10})'
        Assin=None
        couponPercent=None
        couponPrice=None
        discount_price=None
        final_price=None
        couperValue=None
        totalDiscount=None
        total_discount=None
        subscription = None
        status_check=response.status
       
        # if response.status == 404:
        
        # sleep(10)

        
        
        
        product_title  = response.xpath('//h1[@id="title"]/span[@id="productTitle"]/text()').get()
        
       
        # image_url = image_P.xpath('@src').get()
        print('title',product_title,'price',product_price,'discount',product_discount,'last_price',last_price)
        
        
        if product_title:
            pattern = r'(\$?\d+(\.\d+)?%?)'
            print('respopnse',response)
            #break
            product_title = product_title.strip()
            
            product_availability=response.xpath('//div[@id="availability"]/span/span/text()').get()
            img_src=None
            img_src = response.xpath('//div[@id="imgTagWrapperId"]/img/@src').get()
            self.product_value=False
            whiskyscraper.database.update_field_by_id(object_id,data_list,self.product_value,img_src)
            
            if product_availability and 'Currently unavailable' in product_availability :
                print('status1----------------------------------------------------',product_availability)
                
                print('status2----------------------------------------------------',product_availability)
                # yield {'url':response.url,'status':product_availability}
                # yield whiskyscraper.pipelines.AvailabilityPipeline(url=response.url, status=product_availability)
                yield {'url': response.url, 'status': product_availability, 'type': 'availability'}
    
                
                
            else:
                img_src = response.xpath('//div[@id="imgTagWrapperId"]/img/@src').get()
                print('status2 img----------------------------------------------------',img_src)
                product_discount = response.xpath('//div[@style=""]//span[@class="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage"]/text()').get()
                if product_discount is not None:
                    product_price = response.xpath('//div[@id="centerCol"]//div[@style=""]//span[@class="a-price-whole"]/text()').get()
                    product_fraction = response.xpath('//div[@id="centerCol"]//div[@style=""]//span[@class="a-price-fraction"]/text()').get()
                    if product_price and product_fraction:
                        product_price = f"{product_price}.{product_fraction}"
                    print(f"prodouct price1:{product_price}")
                    last_price = response.xpath('//span[@class="a-price a-text-price" and @data-a-color="secondary"]/span/text()').get()
                else:
                    product_price = response.xpath('//div[@id="centerCol"]//div[@style=""]//span[@class="a-price-whole"]/text()').get()
                    product_fraction = response.xpath('//div[@id="centerCol"]//div[@style=""]//span[@class="a-price-fraction"]/text()').get()
                    if product_price and product_fraction:
                        product_price = f"{product_price}.{product_fraction}"
                    print(f"prodouct price2:{product_price}")    
                if product_price is None:
                    
                    product_price = response.xpath('//div[@id="centerCol"]//span[@class="a-offscreen"]/text()').get()
                print(f"prodouct price:{product_price}")
                if product_price ==" " or product_price is None:
                    print("YESSS")

                    product_price = response.xpath('//div[@id="centerCol"]//span[@class="a-price-whole"]/text()').get()
                    product_fraction = response.xpath('//div[@id="centerCol"]//span[@class="a-price-fraction"]/text()').get()
                    if product_price and product_fraction:
                        product_price = f"{product_price}.{product_fraction}"
                    print(f"prodouct price3:{product_price}")    
                print('title',product_title,'price',product_price,'discount',product_discount,'last_price',last_price)
                if product_price:
                    if not '$' in str(product_price):
                            product_price  = '$'+product_price
                if product_price is not None:
                    try:
                        if 'The price is' in product_price:
                            product_price =None
                    except:
                        print('prduct--------',product_price)

                if product_price is not None:
                    base_price = float(re.sub(r'[^\d.]', '', product_price))
                    
                    couperValue=response.xpath('//div[@id="reinvent_price_desktop_newAccordionRow" and @style=""]//label[contains(@id, "coupon") and contains(@for,"checkboxpctch")]/text()').get()
                    if couperValue is None:
                        couperValue=response.xpath('//div[@id="reinvent_price_desktop_snsAccordionRowMiddle" and @style=""]//label[contains(@id, "coupon") and contains(@for,"checkboxpctch")]/text()').get()
                        if couperValue is None:
                            couperValue=response.xpath('//div[@id="amazonGlobal_feature_div"]//span[@class="a-size-base a-color-secondary"]/text()').get()
                    
                    # Step 3: Extract the number and symbol using regex
                    if couperValue:
                        
                        # Use regex to find the numeric value and the symbol
                        if 'Subscribe' in couperValue:
                            subscription = 'Yes'
                        else:
                            subscription = 'No'

                        print(f"Subscription: {subscription}")

                        match = re.search(pattern, couperValue)
                        if match:
                            # Extract the matched value (number and symbol)
                            matched_value = match.group(0)  # The full match (number and symbol)
                            
                            if '%' in matched_value:
                                couponPercent = float(matched_value.replace('%', ''))  # Store the percentage value
                                # Extract the numeric part from the percentage (remove the '%' symbol)
                                percentage_value = float(matched_value.replace('%', '')) / 100
                                # Apply the percentage discount to the base price
                                discount_price = base_price * percentage_value
                                final_price = base_price - discount_price  # Subtract the discount from the base price
                                
                            elif '$' in matched_value:  # Can be extended for other currencies
                                couponPrice = float(matched_value.replace('$', ''))  # Store the price (currency symbol)
                                # Extract the numeric part from the price (remove the '$' or '€' symbol)
                                price_value = float(matched_value.replace('$', ''))
                                # Apply the fixed price discount to the base price
                                discount_price=price_value
                                final_price = base_price - price_value 
                        print('couponPercent',couponPercent,'couponPrice',couponPrice,'discount_price',discount_price,'subscription',subscription,'final_price',final_price)
                        data_coupon = {'couponPercent':couponPercent,'couponPrice':couponPrice,'discount_price':discount_price,'subscription':subscription,'final_price':final_price}
                        
                        

                    
                utc_time = datetime.utcnow()
                utc_time_str = utc_time.strftime('%Y-%m-%d %H:%M:%S')
                self.product_value=True
                print('title',product_title,'price',product_price,'discount',product_discount,'last_price',last_price,'utc time',utc_time_str,'pro',self.product_value)
                data_list = {'price':product_price,'discount':product_discount,'last_price':last_price,'utc_time':utc_time_str}
                # yield whiskyscraper.pipelines.ProductPipeline(url=response.url, title="product_title", price=product_price, discount=product_discount, last_price=last_price, utc_time=utc_time_str)
                # whiskyscraper.database.update_field_by_id(object_id,data_list,self.product_value,img_src)
                if product_discount is None:
                    last_price=product_price
                if last_price is not None:    
                    if '$' in str(last_price):
                        last_price = float(last_price.replace('$', '').replace(',', ''))
                    else:
                        last_price = float(last_price)
                if final_price is not None and last_price is not None:
                    final_price = float(final_price)  # Remove '$' and ',' before converting
                    total_discount = ((last_price - final_price) / last_price) * 100
                # else:
                    # final_price = 0.0  # Set default value if final_price is missing  # Convert final_price to float

                # Now you can perform the calculation without errors
                
                match2=re.search(asin_pattern, response.url)
                if match2:
                    Assin=match2.group(1) 
                yield {
                        'url': response.url,
                        'Asin':Assin,
                        'title': product_title,
                        'price': product_price,
                        'Dealdiscount': product_discount,
                        'Orignalprice': last_price,
                        'utc_time': utc_time_str,
                        'Brand':brandName,
                        'Coupon%': couponPercent,
                        'Coupon$': couponPrice,
                        'DiscountPrice': discount_price,
                        'subscription': subscription,
                        'FinalPrice': final_price,
                        'TotalDiscount':total_discount,
                        'Commisisonpayout':commission_payout,
                        'type': 'product'
                    }
                  
                

            
            
            

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
                        'product_name':productName,
                        'brand_name':brandName,
                        'commission_payout':commission_payout,
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