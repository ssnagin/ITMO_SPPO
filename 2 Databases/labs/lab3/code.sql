-- NEW DATABASE HERE:

CREATE TABLE creature (
    id SERIAL PRIMARY KEY,
    is_alive BOOLEAN NOT NULL,

    name VARCHAR(64) NOT NULL
);

CREATE TABLE human (
    creature_id INTEGER NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 0),

    job VARCHAR(64),

    PRIMARY KEY (creature_id),
    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE
);

CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    model VARCHAR(64) NOT NULL
);

CREATE TABLE job (
    id SERIAL PRIMARY KEY,
    job VARCHAR(64) NOT NULL
);

CREATE TABLE robot (
    creature_id INTEGER NOT NULL UNIQUE,

    model_id INTEGER NOT NULL UNIQUE,
    
    PRIMARY KEY (creature_id),
    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES model(id) ON DELETE CASCADE
);

CREATE TABLE time (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL
);

CREATE OR REPLACE FUNCTION calculate_discount(price NUMERIC, discount_percent NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    discount_amount NUMERIC;
BEGIN
    discount_amount := price * discount_percent / 100;
    RETURN price - discount_amount;
END;
$$ LANGUAGE plpgsql;

CREATE [ OR REPLACE ] FUNCTION
    name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
    [ RETURNS rettype
      | RETURNS TABLE ( column_name column_type [, ...] ) ]
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | WINDOW
    | { IMMUTABLE | STABLE | VOLATILE }
    | [ NOT ] LEAKPROOF
    | { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT }
    | { [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER }
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST execution_cost
    | ROWS result_rows
    | SUPPORT support_function
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
    | sql_body
  } ...

CREATE OR REPLACE FUNCTION update_spacecraft_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.health = 100 THEN
        NEW.status_id := (SELECT id FROM status WHERE time = 'active');
    ELSIF NEW.health = 0 THEN
        NEW.status_id := (SELECT id FROM status WHERE time = 'inactive');
    ELSIF NEW.health BETWEEN 1 AND 99 THEN
        NEW.status_id := (SELECT id FROM status WHERE time = 'broken');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER spacecraft_status_trigger
BEFORE INSERT OR UPDATE OF health ON spacecraft
FOR EACH ROW
EXECUTE FUNCTION update_spacecraft_status();

CREATE TABLE color (
    id SERIAL PRIMARY KEY,
    color VARCHAR(64) NOT NULL
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    time VARCHAR(64) NOT NULL
);

CREATE TABLE spacecraft (
    id SERIAL PRIMARY KEY,

    health SMALLINT CHECK (health BETWEEN 0 AND 100),

    status_id INTEGER NOT NULL,
    color_id INTEGER NOT NULL,
    name VARCHAR(64) NOT NULL,

    FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
    FOREIGN KEY (color_id) REFERENCES color(id) ON DELETE CASCADE
);

CREATE TABLE location_info (
    id SERIAL PRIMARY KEY,

    name VARCHAR(64) UNIQUE,
    comments TEXT NULL
);

CREATE TABLE location_spacecraft (
    name VARCHAR(64) NOT NULL,
    spacecraft_id INTEGER NOT NULL,

    PRIMARY KEY (name, spacecraft_id),

    FOREIGN KEY (name) REFERENCES location_info(name) ON DELETE CASCADE,
    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE
);

CREATE TABLE camera (
    id SERIAL PRIMARY KEY,
    
    status_id INTEGER NOT NULL,
    size INTEGER CHECK (size > 0),

    FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE
);

CREATE TABLE manipulator (
    id SERIAL PRIMARY KEY, 

    size INTEGER NOT NULL CHECK (size > 0),

    status_id INTEGER NOT NULL,
    color_id INTEGER NOT NULL,

    FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
    FOREIGN KEY (color_id) REFERENCES color(id) ON DELETE CASCADE
);

CREATE TABLE spacecraft_manipulator (
    spacecraft_id INTEGER NOT NULL,
    manipulator_id INTEGER NOT NULL,

    PRIMARY KEY (manipulator_id, spacecraft_id),

    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE,
    FOREIGN KEY (manipulator_id) REFERENCES manipulator(id) ON DELETE CASCADE
);

CREATE TABLE spacecraft_camera (
    spacecraft_id INTEGER NOT NULL,
    camera_id INTEGER NOT NULL,

    PRIMARY KEY (camera_id, spacecraft_id),

    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE,
    FOREIGN KEY (camera_id) REFERENCES camera(id) ON DELETE CASCADE
);

CREATE TABLE creature_location_captain (
    spacecraft_id INTEGER NOT NULL,
    creature_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,


    PRIMARY KEY (creature_id, spacecraft_id, time_id),

    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE,
    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES time(id) ON DELETE CASCADE
);

CREATE TABLE creature_location_position (
    location_id INTEGER NOT NULL,
    creature_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,


    PRIMARY KEY (creature_id, location_id, time_id),

    FOREIGN KEY (location_id) REFERENCES spacecraft(id) ON DELETE CASCADE,
    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES time(id) ON DELETE CASCADE
);

-- -----------

INSERT INTO model (model) VALUES 
('Супер робот 3000'),
('Стандартная модель'),
('Продвинутая модель');

INSERT INTO job (job) VALUES 
('Космический сотрудник'),
('Капитан'),
('Инженер'),
('Научный сотрудник');

INSERT INTO status (time) VALUES 
('active'),
('inactive'),
('broken'),
('observing');

INSERT INTO color (color) VALUES 
('белый'),
('черный'),
('серебристый'),
('красный');

INSERT INTO time (time) VALUES 
('2001-01-01 00:00:00'),
('2001-01-02 00:00:00'),
('2001-01-03 00:00:00'),
('2001-01-04 00:00:00'),
('2001-01-05 00:00:00');

INSERT INTO location_info (name, comments) VALUES 
('Космос', 'Просто пустое пространство'),
('Дискавери', 'Нахождение внутри дискавери'),
('Аппарат 1', 'Нахождение внутри аппарата 1'),
('Аппарат 2', 'Нахождение внутри аппарата 2');

--------------

-- Creatures
INSERT INTO creature (is_alive, name) VALUES 
(true, 'Боумен'),
(false, 'Пул'),
(true, 'ЭАЛ');

INSERT INTO human (creature_id, age, job) VALUES 
(1, 50, (SELECT id FROM job WHERE job = 'Космический сотрудник')),
(2, 40, (SELECT id FROM job WHERE job = 'Космический сотрудник'));

INSERT INTO robot (creature_id, model_id) VALUES 
(3, (SELECT id FROM model WHERE model = 'Супер робот 3000'));

--------------

INSERT INTO spacecraft (health, status_id, color_id, name) VALUES 
(100, (SELECT id FROM status WHERE time = 'active'), (SELECT id FROM color WHERE color = 'белый'), 'Дискавери'),
(0, (SELECT id FROM status WHERE time = 'inactive'), (SELECT id FROM color WHERE color = 'черный'), 'Аппарат 1'),
(100, (SELECT id FROM status WHERE time = 'active'), (SELECT id FROM color WHERE color = 'серебристый'), 'Аппарат 2');

INSERT INTO location_spacecraft (name, spacecraft_id) VALUES 
('Дискавери', 1),
('Аппарат 1', 2),
('Аппарат 2', 3);

--------------------

INSERT INTO camera (status_id, size) VALUES 
((SELECT id FROM status WHERE time = 'inactive'), 10),
((SELECT id FROM status WHERE time = 'inactive'), 14),
((SELECT id FROM status WHERE time = 'inactive'), 20);

INSERT INTO spacecraft_camera (spacecraft_id, camera_id) VALUES 
(1, 1), (1, 2), (1, 3);

INSERT INTO manipulator (size, status_id, color_id) VALUES 
(100, (SELECT id FROM status WHERE time = 'active'), (SELECT id FROM color WHERE color = 'серебристый')),
(100, (SELECT id FROM status WHERE time = 'active'), (SELECT id FROM color WHERE color = 'серебристый'));

INSERT INTO spacecraft_manipulator (spacecraft_id, manipulator_id) VALUES 
(2, 1), (2, 2);

----------------

-- Боуман в дискавери (time_id = 1)
INSERT INTO creature_location_position (location_id, creature_id, time_id) VALUES 
(2, 1, 1);

-- ЭАЛ в дискавери (time_id = 1)
INSERT INTO creature_location_position (location_id, creature_id, time_id) VALUES 
(2, 3, 1);

-- Пул в дискавери (начальные данные, time_id = 1)
INSERT INTO creature_location_position (location_id, creature_id, time_id) VALUES 
(2, 2, 1);

-- Пул пересел на аппарат 1 (time_id = 2)
INSERT INTO creature_location_position (location_id, creature_id, time_id) VALUES 
(3, 2, 2);

-- Пул умер и поплыл в космос (time_id = 3)
INSERT INTO creature_location_position (location_id, creature_id, time_id) VALUES 
(1, 2, 3);

-- Боуман покинул дискавери на аппарате 2 (time_id = 4)
INSERT INTO creature_location_position (location_id, creature_id, time_id) VALUES 
(3, 1, 4);

-- Капитаны с временными метками
-- Боуман - капитан Дискавери (time_id = 1)
INSERT INTO creature_location_captain (spacecraft_id, creature_id, time_id) VALUES 
(1, 1, 1);

-- Пул - капитан аппарата 1 (time_id = 2)
INSERT INTO creature_location_captain (spacecraft_id, creature_id, time_id) VALUES 
(2, 2, 2);

-- ЭАЛ - новый капитан Дискавери (time_id = 3)
INSERT INTO creature_location_captain (spacecraft_id, creature_id, time_id) VALUES 
(1, 3, 3);

-- Боуман - капитан аппарата 2 (time_id = 4)
INSERT INTO creature_location_captain (spacecraft_id, creature_id, time_id) VALUES 
(3, 1, 4);

