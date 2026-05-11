# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class WhiskyscraperPipeline:
    def process_item(self, item, spider):
        return item
class AvailabilityPipeline:
    def open_spider(self, spider):
        self.file = open('availability.csv', 'a', newline='')
        self.writer = csv.writer(self.file)
        # Check if the file is empty, then write the header
        if self.file.tell() == 0:
            self.writer.writerow(['url', 'status'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item.get('type') == 'availability':
            self.writer.writerow([item['url'], item['status']])
        return item

class ProductPipeline:
    def open_spider(self, spider):
        self.file = open('product.csv', 'a', newline='')
        self.writer = csv.writer(self.file)
        # Check if the file is empty, then write the header
        if self.file.tell() == 0:
            self.writer.writerow(['url', 'Asin', 'title', 'price', 'Deal discount', 'Orignal price','utc_time','Brand','Coupon %','Coupon $','Discount Price','subscription','Final Price','Total discouunt % ','Commisison payout ','ranking_list','product_review','product_rating','img'])
         
                   
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item.get('type') == 'product':
            self.writer.writerow([item['url'], item['Asin'], item['title'], item['price'], item['Dealdiscount'], item['Orignalprice'],item['utc_time'], item['Brand'],item['Coupon%'],item['Coupon$'],item['DiscountPrice'],item['subscription'],item['FinalPrice'],item['TotalDiscount'],item['Commisisonpayout'],item['ranking_list'],item['product_review'],item['product_rating'],item['img']])
        return item

class ProductPipeline2:
    def open_spider(self, spider):
        self.file = open('product_update.csv', 'a', newline='')
        self.writer = csv.writer(self.file)
        # Check if the file is empty, then write the header
        if self.file.tell() == 0:
            self.writer.writerow(['url', 'title', 'price', 'discount', 'last_price', 'utc_time','product_review','product_rating','Brand','Parent_asin','Root_total','Month_stock','raking'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item.get('type') == 'product_update':
            self.writer.writerow([item['url'], item['title'], item['price'], item['discount'], item['last_price'], item['utc_time'],item['product_review'],item['product_rating'],item['Brand'],item['Parent_asin'],item['Root_total'],item['Month_stock'],item['raking']])
        return item    
class ProductPipeline3:
    def open_spider(self, spider):
        self.file = open('coupon.csv', 'a', newline='')
        self.writer = csv.writer(self.file)
        # Check if the file is empty, then write the header
        
        if self.file.tell() == 0:
            self.writer.writerow(['Asin', 'Brand', 'price', 'url', 'Coupon %', 'Coupon $','Discount Price','subscription','Final Price'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item.get('type') == 'Coupon':
            self.writer.writerow([item['Asin'], item['Brand'], item['price'], item['url'], item['Coupon%'], item['Coupon$'],item['DiscountPrice'],item['subscription'],item['FinalPrice']])
        return item             