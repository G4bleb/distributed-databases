SELECT
  s.name
FROM
  spell AS s
  INNER JOIN spell_comp AS sc ON s.name = sc.name_spell
  LEFT JOIN component AS c ON sc.name = c.name
  INNER JOIN spell_class_level AS scl ON s.name = scl.name
  LEFT JOIN class_level as cl ON scl.class = cl.class
  AND scl.level = cl.level
WHERE
  cl.class = 'sorcerer/wizard'
  AND cl.level <= 4
GROUP BY
  s.name
HAVING
  COUNT(*) = 1
  AND c.name = 'V';