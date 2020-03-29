import scrapy
import re

class DXSpider(scrapy.Spider):
    name = "dx_spider"
    # start_urls = ['http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID=1']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.download_delay = 2  # 0.5
    
    def start_requests(self):
        with open('links/links.txt', 'r') as f:  # read the list of urls
           for url in f.readlines():             # process each of them
                yield scrapy.Request(  # yield
                    url,
                    # response.urljoin('http://legacy.aonprd.com/bestiary/angel.html#angel-solar'),
                    callback=self.parse
                )
                # break

    # def start_requests(self):
    #     ## grab the first URL to being crawling
    #     # PAGE_URL_SELECTOR = '.index > ul > li > a ::attr(href)
    #     base_url = "http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID="
    #     for i in range(1, 617):  # 1 to 616 : PFRPG Core
    #         yield scrapy.Request(  # yield
    #             base_url + str(i),
    #             callback=self.parsePage
    #         )

    def parse(self, response):
        spell = {}

        NAME_SELECTOR = '.heading ::text'
        spell['name'] = response.css(NAME_SELECTOR).get()
        
        # INFOS_SELECTOR = '.SPDet'
        # infos_response = response.css(INFOS_SELECTOR)

        INFOS_SELECTOR = '.SPDet ::text'
        # print(infos_content)
        infos = response.css(INFOS_SELECTOR).getall()

        for title, content in zip(infos[0::2], infos[1::2]): #syntax : (list[start:end:step])
            spell[title.strip().lower().replace(' ', '_')] = content.strip().strip(';')

        details = parseDetails(spell['level'])
        spell['level'] = {}
        for detail in details:
            caster, level = detail.split(' ')
            spell['level'][caster] = int(level)

        details = parseComponents(spell['components'])
        spell['components'] = []
        for detail in details:
            # component = detail.split(' ')[0]
            spell['components'].append(detail)
        
        try:
            spell['spell_resistance'] = ("yes" in spell['spell_resistance'])
        except KeyError:
            spell['spell_resistance'] = False

        DESCRIPTION_SELECTOR = '.SPDesc'
        spell['description'] = response.css(DESCRIPTION_SELECTOR).get()

        # print(spell)
        return spell

def parseInfos(infos_content):
    print(infos_content)
    return infos_content

#Separates values by commas
def parseDetails(desc):
    details = desc.split(",")
    details = [d.strip() for d in details]
    # details = [d.replace(';', '') for d in details]
    return details

def parseComponents(desc):
    material = re.match(r"\(.+\)", desc)
    if material is not None:
        material = material.group(0)
        material_withoutcommas = material.replace('a', '')
        desc = desc.replace(material, material_withoutcommas)
    return parseDetails(desc)
