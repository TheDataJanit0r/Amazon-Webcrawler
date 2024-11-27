import scrapy
from ..items import LaptopItem
import json
class Amazon_Webcrawler(scrapy.Spider):
    name = "Amazon_Webcrawler"
    start_urls = ['https://www.amazon.de/s?k=macbook']  # replace with your start URL

    def start_requests(self):
        # GET request
        api_url = "http://proxy.zyte.com:8011"
        api_key = "YOUR_ZYTE_API_KEY"  # replace with your Zyte API key
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {api_key}"
        }
        payload = {
            "url": "https://www.amazon.de/s?k=macbook",
            "render": "true"
        }
        yield scrapy.Request(
            url=api_url,
            method="POST",
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse
        )

    def parse(self, response):
        for laptop in response.css('div[data-component-type="s-search-result"]'):
            item = LaptopItem()
            item['name'] = laptop.css('span.a-size-medium.a-color-base.a-text-normal::text').get()
            item['price'] = laptop.css('span.a-price-whole::text').get()
            display_size_label= laptop.xpath('.//div[@class="puisg-col-inner"]/span[@class="a-text-bold"]/text()').get()
            item['display_size'] = display_size_label if 'Zoll' in display_size_label else None            
            print(item)
            
            yield item
            with open('output.html', 'a') as f:
                f.write(response.text)
            next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)


    def extract_price(self, name):
        # Implement your logic to extract price from the name string
        pass

    def extract_display_size(self, name):
        # Implement your logic to extract display size from the name string
        pass