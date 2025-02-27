import scrapy
from ..items import LaptopItem
import json
import re
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class Amazon_Webcrawler(scrapy.Spider):
    name = "Amazon_Webcrawler"
    
    # Track product count and pages
    product_count = 0
    current_page = 1
    
    def start_requests(self):
        url = "https://www.amazon.de/s?k=macbook"
        self.logger.info(f"{Fore.CYAN}Starting Amazon scraping at {url}{Style.RESET_ALL}")
        
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={
                "zyte_api": {
                    "renderJs": True,
                    "browserHtml": True
                }
            }
        )

    def parse(self, response):
        self.logger.info(f"{Fore.GREEN}======= PAGE {self.current_page} ======={Style.RESET_ALL}")
        
        # Create a list to store products on this page
        page_products = []
        
        # Extract laptop information
        for laptop in response.css('div[data-component-type="s-search-result"]'):
            item = LaptopItem()
            
            # Try multiple selectors for the name
            name_selectors = [
                'h2 a span::text',
                'h2 span::text',
                '.a-size-medium.a-color-base.a-text-normal::text',
                '.a-link-normal .a-text-normal::text',
                '.a-link-normal span::text'
            ]
            
            # Try each selector until we find a match
            for selector in name_selectors:
                name = laptop.css(selector).get()
                if name:
                    item['name'] = name.strip()
                    break
            
            # Extract price (first look for the whole price, then try the general price field)
            price = laptop.css('span.a-price-whole::text').get()
            if not price:
                price_text = laptop.css('span.a-offscreen::text').get()
                if price_text:
                    # Extract numeric part from price text (e.g. "€24,99" -> "24")
                    match = re.search(r'(\d+)', price_text)
                    if match:
                        price = match.group(1)
            
            item['price'] = price
            
            # Check if the product description or title contains "Zoll" for display size
            # First check the name we just found
            display_size = None
            
            if item['name'] and 'Zoll' in item['name']:
                # Try to extract the display size from the name
                match = re.search(r'(\d+[\.,]?\d*)\s*Zoll', item['name'])
                if match:
                    display_size = f"{match.group(1)} Zoll"
            
            if not display_size:
                # Look in product features or description
                for text in laptop.xpath('.//text()').getall():
                    if isinstance(text, str) and 'Zoll' in text:
                        display_size = text.strip()
                        break
            
            item['display_size'] = display_size
            
            # Add to page products if we have a name
            if item.get('name'):
                self.product_count += 1
                page_products.append(item)
                yield item
        
        # Print pretty table of results
        if page_products:
            # Prepare data for tabulate
            table_data = []
            for idx, product in enumerate(page_products, 1):
                # Truncate name if too long
                name = product.get('name', 'N/A')
                if name and len(name) > 60:
                    name = name[:57] + '...'
                
                # Format price with Euro symbol
                price = product.get('price')
                price_formatted = f"€{price}" if price else 'N/A'
                
                table_data.append([
                    f"{self.product_count - len(page_products) + idx}",
                    name,
                    price_formatted,
                    product.get('display_size', 'N/A')
                ])
            
            # Print table
            table = tabulate(
                table_data, 
                headers=["#", "Product Name", "Price", "Display Size"],
                tablefmt="grid"
            )
            self.logger.info(f"\n{table}")
            
            self.logger.info(f"{Fore.YELLOW}Found {len(page_products)} products on page {self.current_page}{Style.RESET_ALL}")
        else:
            self.logger.warning(f"{Fore.RED}No products found on page {self.current_page}{Style.RESET_ALL}")
        
        # Follow pagination
        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
        if next_page is not None:
            self.current_page += 1
            self.logger.info(f"{Fore.CYAN}Following next page: {next_page}{Style.RESET_ALL}")
            yield response.follow(next_page, self.parse, meta={"zyte_api": {"renderJs": True, "browserHtml": True}})
        else:
            # Final summary
            self.logger.info(f"{Fore.GREEN}====== SCRAPING COMPLETE ======{Style.RESET_ALL}")
            self.logger.info(f"{Fore.GREEN}Total products found: {self.product_count}{Style.RESET_ALL}")
            self.logger.info(f"{Fore.GREEN}Total pages scraped: {self.current_page}{Style.RESET_ALL}")