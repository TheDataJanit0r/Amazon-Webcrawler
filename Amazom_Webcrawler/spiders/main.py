import scrapy
from ..items import LaptopItem
class Amazom_Webcrawler(scrapy.Spider):
    name = "Amazom_Webcrawler"
    start_urls = ['https://www.amazon.de/s?k=macbook']  # replace with your start URL

    def start_requests(self):
        # GET request
        yield scrapy.Request("https://www.amazon.de/s?k=macbook", meta={"playwright": True})

    def parse(self, response):
        for laptop in response.css('div[data-component-type="s-search-result"]'):
            item = LaptopItem()
            item['name'] = laptop.css('span.a-size-medium.a-color-base.a-text-normal::text').get()
            item['price'] = laptop.css('span.a-price-whole::text').get()
            display_size_label= laptop.xpath('.//div[@class="puisg-col-inner"]/span[@class="a-text-bold"]/text()').get()
            item['display_size'] = display_size_label if 'Zoll' in display_size_label else None            
            print(item)
            
            yield item

            next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
        

    def extract_price(self, name):
        # Implement your logic to extract price from the name string
        pass

    def extract_display_size(self, name):
        # Implement your logic to extract display size from the name string
        pass