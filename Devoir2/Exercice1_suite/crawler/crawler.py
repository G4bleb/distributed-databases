import scrapy
import re

class DXSpider(scrapy.Spider):
    name = "dx_spider"
    # start_urls = ['http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID=1']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.download_delay = 1  # 0.5

    def start_requests(self):
        ## grab the first URL to being crawling
        # PAGE_URL_SELECTOR = '.index > ul > li > a ::attr(href)
        base_url = "http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID="
        for i in range(1, 617):  # 1 to 616 : PFRPG Core
            yield scrapy.Request(  # yield
                base_url + str(i),
                # response.urljoin('http://legacy.aonprd.com/bestiary/angel.html#angel-solar'),
                callback=self.parsePage
            )

    def parsePage(self, response):
        print("PARSING : "+response.url)

        # NAME_SELECTOR = '.body .stat-block-title'
        # creaturesStatBlockTitles = response.css(NAME_SELECTOR).getall()
        # print(creaturesStatBlockTitles)

        # CONTENT_SELECTOR = '.body'
        # page_content = response.css(CONTENT_SELECTOR).get()
        # spells = parseContent(page_content)
        # for i, sbt in enumerate(creaturesStatBlockTitles):
        #     try:
        #         yield {'name': getCreatureNameFromStatBlockTitle(sbt), 'spells': spells[i]}
        #     except IndexError:
        #         yield {'name': getCreatureNameFromStatBlockTitle(sbt), 'spells': []}
        #     except AssertionError:
        #         pass
