import scrapy

class LaptopSpider(scrapy.Spider):
    name = "Amazom_Webcrawler"
    start_urls = ['https://www.amazon.de/s?k=macbook']  # replace with your start URL

    def parse(self, response):
        for laptop in response.css('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal'):
            yield {
                'name': laptop.css('::text').get(),
                # Assuming price and display size are part of the name and need to be parsed out
                'price': laptop.css('span.a-price-whole::text').get(),
                'display_size': laptop.css('div.puisg-col-inner span.a-text-bold::text').get(),
            }

        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def extract_price(self, name):
        # Implement your logic to extract price from the name string
        pass

    def extract_display_size(self, name):
        # Implement your logic to extract display size from the name string
        pass