-- 1. TABLES CREATION (надо ли в дата модели указывать эти доп. параметры?)

CREATE TABLE creature (
    id SERIAL PRIMARY KEY,
    is_alive BOOLEAN NOT NULL,

    name VARCHAR(64) NOT NULL
);

CREATE TABLE spacecraft (
    id SERIAL PRIMARY KEY,

    health SMALLINT CHECK (health BETWEEN 0 AND 100),

    is_alive BOOLEAN NOT NULL,
    name VARCHAR(64) NOT NULL
);


CREATE TABLE human (
    id SERIAL PRIMARY KEY,
    creature_id INTEGER NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 0),

    job VARCHAR(64),

    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE
);

CREATE TABLE robot (
    id SERIAL PRIMARY KEY,
    creature_id INTEGER NOT NULL UNIQUE,

    model VARCHAR(64) NOT NULL,

    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE
);

CREATE TABLE camera (
    id SERIAL PRIMARY KEY,

    is_observing BOOLEAN NOT NULL,
    size INTEGER CHECK (size > 0)
);

CREATE TABLE manipulator (
    id SERIAL PRIMARY KEY,

    is_active BOOLEAN NOT NULL,
    size INTEGER CHECK (size > 0),
    
    is_broken BOOLEAN NOT NULL
);

CREATE TABLE location (
    id SERIAL PRIMARY KEY,

    spacecraft_id INTEGER NULL UNIQUE,
    name VARCHAR(64) NULL,
    comments TEXT,

    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE
);

CREATE TABLE changelog (
    id SERIAL PRIMARY KEY,

    time INTEGER NOT NULL UNIQUE
);

ALTER TABLE s467525.creature_location_position ADD COLUMN time_id INTEGER NULL;

-- connections 

CREATE TABLE creature_location_position (
    id SERIAL PRIMARY KEY,
    creature_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,

    time_id INTEGER NULL;

    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES changelog(id) ON DELETE CASCADE
);

CREATE TABLE creature_location_captain (
    id SERIAL PRIMARY KEY,
    creature_id INTEGER NOT NULL,
    spacecraft_id INTEGER NOT NULL,

    FOREIGN KEY (creature_id) REFERENCES creature(id) ON DELETE CASCADE,
    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE
);

CREATE TABLE spacecraft_camera (
    camera_id INTEGER NOT NULL,
    spacecraft_id INTEGER NOT NULL,

    PRIMARY KEY (camera_id, spacecraft_id),
    FOREIGN KEY (camera_id) REFERENCES camera(id) ON DELETE CASCADE,
    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE
);

CREATE TABLE spacecraft_manipulator (
    manipulator_id INTEGER NOT NULL,
    spacecraft_id INTEGER NOT NULL,

    PRIMARY KEY (manipulator_id, spacecraft_id),
    FOREIGN KEY (manipulator_id) REFERENCES manipulator(id) ON DELETE CASCADE,
    FOREIGN KEY (spacecraft_id) REFERENCES spacecraft(id) ON DELETE CASCADE
);

-- 2. Filling with values, sometimes random one

INSERT INTO s467525.creature (is_alive, name) VALUES (true, 'Боумен');
INSERT INTO s467525.creature (is_alive, name) VALUES (false, 'Пул');
INSERT INTO s467525.creature (is_alive, name) VALUES (true, 'ЭАЛ');

INSERT INTO s467525.human (creature_id, age, job) VALUES (1, 50, 'Космический сотрудник');
INSERT INTO s467525.human (creature_id, age, job) VALUES (2, 40, 'Космический сотрудник');

INSERT INTO s467525.robot (creature_id, model) VALUES (3, 'Супер робот 3000');

INSERT INTO s467525.spacecraft (health, is_alive, name) VALUES (100, true, 'Дискавери');
INSERT INTO s467525.spacecraft (health, is_alive, name) VALUES (0, false, 'Аппарат 1');
INSERT INTO s467525.spacecraft (health, is_alive, name) VALUES (100, true, 'Аппарат 2');

INSERT INTO s467525.location (spacecraft_id, name, comments) VALUES (null, 'Космос', 'Просто пустое пространство');
INSERT INTO s467525.location (spacecraft_id, name, comments) VALUES (1, null, 'Нахождение внутри дискавери');
INSERT INTO s467525.location (spacecraft_id, name, comments) VALUES (2, null, 'Нахождение внутри аппарата 1');
INSERT INTO s467525.location (spacecraft_id, name, comments) VALUES (3, null, 'Нахождение внутри аппарата 2');

-- Some cameras:

-- Для дискавери
INSERT INTO s467525.camera (is_observing, size) VALUES (false, 10), (false, 14), (false, 20);

-- setting connections

-- POSITION

-- Боуман в дискавери
INSERT INTO s467525.creature_location_position (creature_id, location_id) VALUES (1, 2);
-- ЭАЛ в дискавери-- Боуман -- капитан Дискавери:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (1, 1);
-- Пул -- капитан аппарата 1:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (2, 2);

-- ЭАЛ -- новый капитан Дискавери:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (3, 1);
-- а Боуман -- каптан Аппарата 2:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (1, 3);
INSERT INTO s467525.creature_location_position (creature_id, location_id) VALUES (3, 2);
-- Пул в дискавери (начальные данные)
INSERT INTO s467525.creature_location_position (creature_id, location_id) VALUES (2, 2);

-- Далее, Пул покинул дискавери, т.е. пересел на аппарат 1:
INSERT INTO s467525.creature_location_position (creature_id, location_id) VALUES (2, 3);

-- Далее, Пул умер в корабле и поплыл в космос:
INSERT INTO s467525.creature_location_position (creature_id, location_id) VALUES (2, 1);

-- Далее, Боуман поплыл за Пулом на Аппарате 2, т.е. покинул дискавери:
INSERT INTO s467525.creature_location_position (creature_id, location_id) VALUES (1, 4);

-- CAPTAIN

-- Боуман -- капитан Дискавери:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (1, 1);
-- Пул -- капитан аппарата 1:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (2, 2);

-- ЭАЛ -- новый капитан Дискавери:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (3, 1);
-- а Боуман -- каптан Аппарата 2:
INSERT INTO s467525.creature_location_captain (creature_id, spacecraft_id) VALUES (1, 3);

-- SET CAMERAS

-- рандомные 3 камеры у дискавери, все выключенные:
INSERT INTO s467525.spacecraft_camera (camera_id, spacecraft_id) VALUES (1, 1), (2, 1), (3, 1);

-- рандомные 2 манипулятора у аппарата 1
INSERT INTO s467525.manipulator (is_active, size, is_broken) VALUES (true, 100, false), (true, 100, false);

-- Отследить время создания

ALTER TABLE s467525 SET 