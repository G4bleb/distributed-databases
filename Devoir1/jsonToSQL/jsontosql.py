import json

with open('data.json', 'r') as f:
    spells = json.load(f)

sqlFile = open('commands.sql', 'w')

print(spells[0]['name'])

for spell in spells:
    tmp = "INSERT INTO spell VALUES(null, '{}', '{}', '{}', '{}', '{}', {});".format(spell['name'],
      spell['school'],
       spell['casting_time'],
        spell['target/effect/area'],
         spell['duration'],
          int(spell['spell_resistance']))
    print(tmp)
    
    exit()
