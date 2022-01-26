import scrapy
from ..items import TudogostososcraperItem
from scrapy.loader import ItemLoader


class TudogostosobolosSpider(scrapy.Spider):
    name = 'tudogostosobolos'
    # allowed_domains = ['https://www.tudogostoso.com.br/categorias/1000-bolos\
            # -e-tortas-doces-1300?filter=rapida']
    start_urls = ['https://www.tudogostoso.com.br/categorias/1000-bolos-e-tor\
            tas-doces-1300?filter=rapida']

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
            # yield l.load_item()

            bolo_href= bolo.xpath("//div[@class='rounded']//a[@class='link row m-0']/@href").get()
            bolo_link = response.urljoin(bolo_href)
            # print(bolo_link)
            yield scrapy.Request(url=bolo_link, meta={'item' : l.load_item()},
                    callback=self.parse_ingredients, dont_filter=True)
            # yield response.follow(url=bolo_link, meta={'item' : l.load_item()},
                    # callback=self.parse_ingredients, dont_filter=True)

        next_page = response.xpath(".//a[@class='next']/@href").get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url = next_page_link, callback = self.parse,
                    dont_filter=True)
            # yield response.follow(next_page, callback=self.parse,
                    # dont_filter=True)

    #Scrape the ingredients from the detail page
    def parse_ingredients(self, response):
        ingredients_location=response.xpath("//div[@class='col-LG-8 ingredients-card']")
        l = ItemLoader(item=response.meta['item'],
                selector=ingredients_location)
        l.add_xpath('first_ingredient', "//span[@class='p-ingredient']/p/text()")
        yield l.load_item()

