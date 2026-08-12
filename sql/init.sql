CREATE TABLE usuarios (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    sexo            CHAR(1) CHECK (sexo IN ('M', 'F', 'O')),
    nivel_actividad VARCHAR(255) CHECK (nivel_actividad IN ('Sedentario', 'Ligero', 'Moderado', 'Muy activo')),
    objetivo        VARCHAR(255) CHECK (objetivo IN ('Definición', 'Mantenimiento', 'Volumen')),
    altura_cm       INT,
    edad            INT,
    peso_kg         DECIMAL(5, 2)
);

CREATE TABLE alimentos (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(255) NOT NULL,
    kcal        DECIMAL(6, 2),
    proteinas   DECIMAL(6, 2),
    carbos      DECIMAL(6, 2),
    grasas      DECIMAL(6, 2)
);

CREATE TABLE registros (
    id          SERIAL PRIMARY KEY,
    id_usuario  INT REFERENCES usuarios(id),
    id_alimento INT REFERENCES alimentos(id),
    gramos      INT NOT NULL,
    fecha       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);