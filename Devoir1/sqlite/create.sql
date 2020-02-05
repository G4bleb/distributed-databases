------------------------------------------------------------
--        Script SQLite  
------------------------------------------------------------
------------------------------------------------------------
-- Table: spell
------------------------------------------------------------
CREATE TABLE spell(
	name TEXT NOT NULL,
	school TEXT,
	casting_time TEXT,
	target_effect_area TEXT,
	duration TEXT,
	spell_resistance INTEGER NOT NULL,
	CONSTRAINT spell_PK PRIMARY KEY (name)
);

------------------------------------------------------------
-- Table: component
------------------------------------------------------------
CREATE TABLE component(
	name TEXT NOT NULL,
	CONSTRAINT component_PK PRIMARY KEY (name)
);

------------------------------------------------------------
-- Table: class_level
------------------------------------------------------------
CREATE TABLE class_level(
	class TEXT NOT NULL,
	level INTEGER NOT NULL,
	CONSTRAINT class_level_PK PRIMARY KEY (class, level)
);

------------------------------------------------------------
-- Table: spell_comp
------------------------------------------------------------
CREATE TABLE spell_comp(
	name TEXT NOT NULL,
	name_spell TEXT NOT NULL,
	CONSTRAINT spell_comp_PK PRIMARY KEY (name, name_spell),
	CONSTRAINT spell_comp_component_FK FOREIGN KEY (name) REFERENCES component(name),
	CONSTRAINT spell_comp_spell0_FK FOREIGN KEY (name_spell) REFERENCES spell(name)
);

------------------------------------------------------------
-- Table: spell_class_level
------------------------------------------------------------
CREATE TABLE spell_class_level(
	class TEXT NOT NULL,
	level INTEGER NOT NULL,
	name TEXT NOT NULL,
	CONSTRAINT spell_class_level_PK PRIMARY KEY (class, level, name),
	CONSTRAINT spell_class_level_class_level_FK FOREIGN KEY (class, level) REFERENCES class_level(class, level),
	CONSTRAINT spell_class_level_spell0_FK FOREIGN KEY (name) REFERENCES spell(name)
);