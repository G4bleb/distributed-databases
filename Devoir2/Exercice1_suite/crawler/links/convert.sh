#!/bin/sh

# sed 's/SDB_SpellBlock.asp?SDBID=/http:\/\/www.dxcontent.com\/SDB_SpellBlock.asp?SDBID=/g' links_untreated > links_1 
# sed -r -e 's/href="([^"]+)"/\1\n/g' links_1 > links_2
# sed '/http/!d' links_2 > links_3
# awk -F' ' '{print $NF}' links_3 > links_4
# sort -V links_4 > links

sed 's/SDB_SpellBlock.asp?SDBID=/http:\/\/www.dxcontent.com\/SDB_SpellBlock.asp?SDBID=/g' links_untreated.txt | 
sed -r -e 's/href="([^"]+)"/\1\n/g' |
sed '/http/!d' |
awk -F' ' '{print $NF}' |
sort -V > links.txt