import scrapy


class LazadacrawlerSpider(scrapy.Spider):
    name = "lazadacrawler"

    def start_requests(self):
        yield scrapy.Request(
            url = "https://www.lazada.com.my/shop-laptops-gaming/",
            meta={
                "playwright": True
            }
        )

    def parse(self, response):
        products_selector = response.css('[data-tracking="product-card"]')

        for product in products_selector:
            link = response.urljoin(product.xpath('.//a[text()]/@href').get())
            yield scrapy.Request(link, meta={"playwright": True},callback=self.parse_product)

    def parse_product(self, response):
        # yyy = response.css('.pdp-price_color_orange ::Text')

        # print("================================")        
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # print("================================")
        
        yield {
            'Product': response.css('.pdp-mod-product-badge-title ::Text').get(),
            'Price': response.css('.pdp-price_color_orange ::Text').get()
        }
