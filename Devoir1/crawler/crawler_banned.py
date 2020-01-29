import scrapy

class SpellSpider(scrapy.Spider):
    name = 'spell_spider'
    allowed_domains = ['www.dxcontent.com']

    def start_requests(self):
        for i in range(5):
            yield scrapy.Request('http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID=' + str(i), self.parse)

    def parse(self, response):
        SPELL_SELECTOR = '.SpellDiv'
        NAME_SELECTOR = '.heading p'
        SPECS_SELECTOR = '.SPDet'
        for spec in response.css(SPECS_SELECTOR):
            print(spec.get());

        spell = response.css(SPELL_SELECTOR)
        print(response.body)
        yield {
            'name': spell.css(NAME_SELECTOR).get()
        }
        # if spell:
        #     print("FOUND A SPELL")
        # for spell in response.css(SPELL_SELECTOR):
        #     NAME_SELECTOR = 'a ::text'
        #     URL_SELECTOR = 'a ::attr(href)'
        #     yield {
        #         'name': spell.css(NAME_SELECTOR).get(),
        #         'url': spell.css(URL_SELECTOR).get(),
        #     }
    
