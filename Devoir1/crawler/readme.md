# Crawler
This crawler (`crawler.py`) is made using scrapy.

It crawls [https://www.d20pfsrd.com/magic/spell-lists-and-domains/spell-lists-sorcerer-and-wizard/](https://www.d20pfsrd.com/magic/spell-lists-and-domains/spell-lists-sorcerer-and-wizard/) and makes a json collection of all spells listed on the page (`data.json`)

`import.sh` contains a mongoimport command importing `data.json` to the `spells` collection in the `Devoir1-spells` mongoDB database.
`map_reduce.js` contains the mongo commands to find the spells needed for the exercise (wizard/sorcerer level <= and only a verbal component).  