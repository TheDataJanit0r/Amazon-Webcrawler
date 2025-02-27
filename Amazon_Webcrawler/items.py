import scrapy

class LaptopItem(scrapy.Item):
    # Basic information
    asin = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    display_size = scrapy.Field()
    url = scrapy.Field()
    
    # Search metadata
    search_term = scrapy.Field()
    domain = scrapy.Field()
    
    # Additional product information
    rating = scrapy.Field()
    review_count = scrapy.Field()
    is_prime = scrapy.Field()
    is_sponsored = scrapy.Field()
    technical_details = scrapy.Field()
    
    # Timestamps
    timestamp = scrapy.Field()