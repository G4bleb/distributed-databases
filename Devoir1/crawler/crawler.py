import scrapy
import re

class SpellSpider(scrapy.Spider):
    name = "spell_spider"
    start_urls = ['https://www.d20pfsrd.com/magic/spell-lists-and-domains/spell-lists-sorcerer-and-wizard/']

    def parse(self, response):
        SPELL_URL_SELECTOR = 'td:first-child > a.spell ::attr(href)'
        for spell in response.css(SPELL_URL_SELECTOR):
            yield scrapy.Request( #yield
                response.urljoin(spell.get()),
                # response.urljoin(
                #     'https://www.d20pfsrd.com/magic/all-spells/a/acid-splash'),
                callback=self.spellParse
            )

    def spellParse(self, response):
        spell = {}

        NAME_SELECTOR = 'h1 ::text'
        spell['name'] = response.css(NAME_SELECTOR).get()
        
        SPELL_SELECTOR = 'article.magic .article-content'
        spell_response = response.css(SPELL_SELECTOR)

        selectors = []

        selectors.append('.article-content > p:first-of-type')#SCHOOL_SPELL_SELECTOR
        selectors.append('.article-content > p:nth-of-type(3)')#CASTING_SELECTOR
        selectors.append('.article-content > p:nth-of-type(5)')#EFFECT_SELECTOR

        for selector in selectors:
            titles, details = parseContent(
                spell_response.css(selector).get())
            for title, detail in zip(titles, details):
                if(len(detail) == 1 and title != 'components'):
                    detail = detail[0]
                spell[title] = detail
                
        if isinstance(spell['school'], list):
            spell['school'] = ', '.join(spell['school'])

        for title in ['level', 'domain', 'subdomain', 'elemental_school']:
            tmpDict = {}
            try:
                for detail in spell[title]:
                    try:
                        # -2 : on retire le chiffre et le ' '
                        tmp = [detail[:-2], detail[-1:]]
                        tmpDict[tmp[0]] = int(tmp[1])
                        if tmp[0] == '':
                            del tmpDict['']
                    except ValueError:  # Si ce n'est pas un tableau de strings
                        try:
                            tmpDict[spell[title][:-2]] = int(spell[title][-1:])
                        except TypeError:
                            pass
                spell[title] = tmpDict
            except KeyError:  # Si la caractéristique n'existe pas
                pass
        
        # try:
        #     spell['Casting Time'] = [int(spell['Casting Time'][:1]), spell['Casting Time'][2:]]
        # except KeyError:
        #     pass

        # try:
        #     spell['Duration'] = [int(spell['Duration'][:1]), spell['Duration'][1:].strip()]
        # except (ValueError, TypeError, KeyError):
        #     pass

        try:
            spell['spell_resistance'] = ("yes" in spell['spell_resistance'])
        except KeyError:
            spell['spell_resistance'] = False
        
        for title in list(spell):
            if "target" in title or "effect" in title or "area" in title:
                try:
                    spell['target/effect/area'] += ', ' + spell[title]
                except KeyError:
                    if(isinstance(spell[title], list)):
                        spell['target/effect/area'] = ', '.join(spell[title])
                    else:    
                        spell['target/effect/area'] = spell[title]
                del spell[title]
            if "component" in title:
                if(title != "components"):
                    spell['components'] = spell[title]
                    del spell[title]
            # if "<br>" in title:
            #     spell[title.replace('<br>', '')] = spell[title]
            #     del spell[title]

        try:
            del spell['*']
        except KeyError:
            pass

        try:
            del spell[',']
        except KeyError:
            pass


        DESCRIPTION_SELECTOR = '.article-content > p:nth-of-type(7) ::text'
        spell['description'] = spell_response.css(DESCRIPTION_SELECTOR).get()

        # print(spell)
        # yield spell
        yield {k: spell.get(k, None) for k in (
        'name',
         'school',
          'level',
           'casting_time',
            'components',
             'target/effect/area',
              'duration',
               'spell_resistance')}
        

def parseContent(response):
    contents = response.split('<b>')
    del contents[0]
    contents_it = iter(contents)
    titles, descs = [], []
    for content in contents_it:
        title_and_desc = content.split('</b>')  # Titre</b>...
        titles.append(title_and_desc[0].lower().replace(' ', '_'))
        title_and_desc[1] = re.sub('<[^<>]+>', '', title_and_desc[1])
        descs.append(title_and_desc[1])
    
    details = []
    for desc in descs:
        details.append(parseDescription(desc))
    # print(titles)
    # print(details)
    return titles, details
    
#Prend une string de détails de niveaux d'un sort, renvoie un tableau associatif classe => niveau
def parseDescription(desc):
    # content_pattern = re.compile('>[^><]+<')
    # details = content_pattern.findall(desc)
    details = desc.split(",")
    details = [d.strip() for d in details]
    details = [d.replace(';', '') for d in details]
    return details
