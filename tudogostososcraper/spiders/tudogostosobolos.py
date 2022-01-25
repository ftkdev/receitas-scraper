import scrapy
from ..items import TudogostososcraperItem
from scrapy.loader import ItemLoader


class TudogostosobolosSpider(scrapy.Spider):
    name = 'tudogostosobolos'
    allowed_domains = ['https://www.tudogostoso.com.br/categorias/1000-bolos\
            -e-tortas-doces-1300?filter=rapida']
    start_urls = ['https://www.tudogostoso.com.br/categorias/1000-bolos-e-tor\
            tas-doces-1300?filter=rapida']

    def parse(self, response):
        bolos_list = response.xpath("//div[@class='rounded']/div[@class=\
                'mb-3 recipe-card recipe-card-with-hover']")

        for bolo in bolos_list:
            l = ItemLoader(item = TudogostososcraperItem(), selector=bolo)
            l.add_xpath('name', ".//h3/text()")
            l.add_xpath('preparation_time',".//div[@class='time']/text()")
            l.add_xpath('portions',".//div[@class='portion']/text()")
            l.add_xpath('link',".//a[@class='link row m-0']/@href")
            l.add_xpath('author',".//h3/following::span[1]/text()")
            l.add_xpath('likes',".//div[@class='favorites']/text()")
            yield l.load_item()
            
        next_page = response.xpath(".//a[@class='next']").attrib['href']
        if next_page is not None:
            # next_page_link = response.urljoin(next_page)
            # yield scrapy.Request(url = next_page_link, callback = self.parse)
            yield response.follow(next_page, callback=self.parse,
                    dont_filter=True)
