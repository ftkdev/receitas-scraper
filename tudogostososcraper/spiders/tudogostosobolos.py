import scrapy
from ..items import TudogostososcraperItem
from scrapy.loader import ItemLoader


class TudogostosobolosSpider(scrapy.Spider):
    name = 'tudogostosobolos'
    allowed_domains = ['https://www.tudogostoso.com.br/']
    start_urls = ['https://www.tudogostoso.com.br/categorias/1000-bolos-e-tortas-doces-1956?filter=light']

    # Scrape the information from the initial list page
    def parse(self, response):
        bolos_list = response.xpath("//div[@class='rounded']/div[@class=\
                'mb-3 recipe-card recipe-card-with-hover']")

        for bolo in bolos_list:
            l = ItemLoader(item=TudogostososcraperItem(), selector=bolo)
            l.add_xpath('name', ".//h3/text()")
            l.add_xpath('preparation_time',".//div[@class='time']/text()[2]")
            l.add_xpath('portions',".//div[@class='portion']/text()[2]")
            l.add_xpath('link',".//a[@class='link row m-0']/@href")
            l.add_xpath('author',".//h3/following::span[1]/text()")
            l.add_xpath('likes',".//div[@class='favorites']/text()[2]")

            # Acess the detail page to scrape ingredients
            bolo_href= response.xpath("//div[@class='rounded']//a[@class=\
                    'link row m-0']/@href").get()
            yield response.follow(url=bolo_href, meta={'item' : l.load_item()},
                    callback=self.parse_ingredients, dont_filter=True)

        # Iterates through the pages list
        next_page = response.xpath(".//a[@class='next']/@href").get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url = next_page_link, callback = self.parse,
                    dont_filter=True)

    # Scrape the ingredients from the detail page
    def parse_ingredients(self, response):
        l = ItemLoader(item=response.meta['item'], selector=response)
        l.add_xpath('ingredients', "//div[@class='col-lg-8 ingredients-card']\
                //span[@class='p-ingredient']/text()")
        yield l.load_item()

