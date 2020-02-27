import scrapy
import re
import time

class CreatureSpider(scrapy.Spider):
    name = "creature_spider"
    start_urls = ['http://legacy.aonprd.com/bestiary/monsterIndex.html',
                  'http://legacy.aonprd.com/bestiary2/additionalMonsterIndex.html',
                  'http://legacy.aonprd.com/bestiary3/monsterIndex.html',
                  'http://legacy.aonprd.com/bestiary4/monsterIndex.html',
                  'http://legacy.aonprd.com/bestiary5/index.html',]
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.download_delay = 0.5
        
    def parse(self, response):
        PAGE_URL_SELECTOR = '.index > ul > li > a ::attr(href)'
        for page in response.css(PAGE_URL_SELECTOR):
            yield scrapy.Request(  # yield
                response.urljoin(page.get()),
                # response.urljoin('http://legacy.aonprd.com/bestiary/angel.html#angel-solar'),
                # response.urljoin('http://legacy.aonprd.com/bestiary/bat.html'),
                callback=self.parsePage
            )

    def parsePage(self, response):
        print("PARSING : "+response.url)
        # creature = {}

        NAME_SELECTOR = '.body .stat-block-title'
        creaturesStatBlockTitles = response.css(NAME_SELECTOR).getall()
        print(creaturesStatBlockTitles)

        CONTENT_SELECTOR = '.body'
        page_content = response.css(CONTENT_SELECTOR).get()
        spells = parseContent(page_content)
        for i, sbt in enumerate(creaturesStatBlockTitles):
            try:
                yield {'name': getCreatureNameFromStatBlockTitle(sbt), 'spells': spells[i]}
            except IndexError:
                yield {'name': getCreatureNameFromStatBlockTitle(sbt), 'spells': []}
            except AssertionError:
                pass
            # yield(creature)
            # creatures.append(
            #     {'name': getCreatureNameFromStatBlockTitle(sbt), 'spells': spells[i]})
            # yield(creatures[i])
        # print(creatures)
        
        # yield {k: spell.get(k, None) for k in (
        # 'name',
        #  'school',
        #   'level',
        #    'casting_time',
        #     'components',
        #      'target/effect/area',
        #       'duration',
        #        'spell_resistance')}
        
def getCreatureNameFromStatBlockTitle(statblocktitle):
    # p = re.compile('<b>([^<]+)')
    # p = re.compile('>([^<]+).*?<span')
    p = re.compile('>([^0-9<>]+?)<')
    try:
        name = p.search(statblocktitle).group(1).strip()
    except AttributeError:
        print('ERROR COULD NOT FIND CREATURE NAME IN ' + statblocktitle)
        raise AssertionError 
    print(name)
    return name
    
def removeEm(myStr):
    return re.sub('<\/?em>', '', myStr)

def parseContent(response):
    cutContent = re.split('class="stat-block-title"><b>[^<]+', response)
    print(len(cutContent))
    p = re.compile('href=".+?\/spells\/.+?">(.+?)<\/a>')
    ret = []
    for oneContent in cutContent:
        # print(oneContent)
        res = p.findall(oneContent)
        
        if res:
            res = list(map(removeEm, res))
            res = list(dict.fromkeys(res))
            print(res)
            ret.append(res)
    return ret
        
    
#Prend une string de détails de niveaux d'un sort, renvoie un tableau associatif classe => niveau
def parseDescription(desc):
    # content_pattern = re.compile('>[^><]+<')
    # details = content_pattern.findall(desc)
    details = desc.split(",")
    details = [d.strip() for d in details]
    details = [d.replace(';', '') for d in details]
    return details
