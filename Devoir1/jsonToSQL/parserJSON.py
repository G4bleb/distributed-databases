#!/usr/bin/python3

import json

f = open("data.json", "r")
data = json.loads(f.read())
f.close()

sql = ""

for d in data:
    #print(d)

    sql += "INSERT INTO spell VALUES('{}','{}','{}','{}','{}',{});\n".format(d["name"],
                                                                             d["school"],
                                                                             d["casting_time"],
                                                                             d["target/effect/area"],
                                                                             d["duration"],
                                                                             int(d["spell_resistance"])) 
    def insert_comp_spellcomp(component):
        global sql

        sql += "INSERT INTO component VALUES('{}');\n".format(component)
        sql += "INSERT INTO spell_comp SELECT c.name, s.name FROM spell as s, component as c WHERE s.name LIKE '{}' AND c.name LIKE '{}';\n".format(d["name"], component)
    
    try:
        for component in d["components"]:
            insert_comp_spellcomp(component)
    except TypeError:
        continue
        

    def insert_classlevel_spellclasslevel(level,value):
        global sql

        sql += "INSERT INTO class_level VALUES('{}','{}');\n".format(level, value)
        sql += "INSERT INTO spell_class_level SELECT c.class, c.level, s.name FROM spell as s, class_level as c WHERE s.name LIKE '{}' AND c.class LIKE '{}' AND c.level = {};\n".format(d["name"], level, value)
                    

    if type(d["level"]).__name__ == "NoneType":
        continue

    for level in d["level"]:
        try:
            value = d["level"][level]
            insert_classlevel_spellclasslevel(level,value)
        except TypeError:
            try:
                level = d["level"]
                value = d["level"][level]
                insert_classlevel_spellclasslevel(level,value)
            except:
                continue

print(len(sql))
            

f = open("data.sql", "w+")
f.write(sql)
f.close()



