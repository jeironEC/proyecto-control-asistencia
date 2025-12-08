--
-- Base de datos: `control_asistencia`
--

-- -------------------------------------------------------------------------------------------------------------------

--
-- Estructura de tabla para la tabla usuario
--
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('ALUMNO','PROFESOR','PERSONAL_SERVICIO') NOT NULL,
    activo tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* Resultado de la query
+------------+----------------------------------------------+------+-----+---------+----------------+
| Field      | Type                                         | Null | Key | Default | Extra          |
+------------+----------------------------------------------+------+-----+---------+----------------+
| id         | int(11)                                      | NO   | PRI | NULL    | auto_increment |
| nombre     | varchar(100)                                 | NO   |     | NULL    |                |
| apellido   | varchar(100)                                 | NO   |     | NULL    |                |
| correo     | varchar(150)                                 | NO   | UNI | NULL    |                |
| contrasena | varchar(255)                                 | NO   |     | NULL    |                |
| rol        | enum('ALUMNO','PROFESOR','PERSONAL_SERVICIO')| NO   |     | NULL    |                |
| activo     | tinyint(1)                                   | NO   |     | 1       |                |
+------------+----------------------------------------------+------+-----+---------+----------------+
*/

/* INSERCIONES DE USUARIOS */
INSERT INTO usuario (nombre, apellido, correo, contrasena, rol, activo)
VALUES ('Manuel', 'Torres', 'manuel.torres@gmail.com', '123456789', 'ALUMNO', 1);

INSERT INTO usuario (nombre, apellido, correo, contrasena, rol, activo)
VALUES ('Antonio', 'Pedregal', 'antonio.pedregal@gmail.com', '123456789', 'PROFESOR', 1);

INSERT INTO usuario (nombre, apellido, correo, contrasena, rol, activo)
VALUES ('Otoniel', 'Escobar', 'otoniel.escobar@gmail.com', '123456789', 'PERSONAL_SERVICIO', 1);

--
-- Estructura de tabla para la tabla asistencia
--
CREATE TABLE IF NOT EXISTS asistencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('PRESENTE','AUSENTE','RETRASO','JUSTIFICADA') NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* Resultado de la query
+------------+----------------------------------------------------+------+-----+---------+----------------+
| Field      | Type                                               | Null | Key | Default | Extra          |
+------------+----------------------------------------------------+------+-----+---------+----------------+
| id         | int(11)                                            | NO   | PRI | NULL    | auto_increment |
| fecha      | date                                               | NO   |     | NULL    |                |
| hora       | time                                               | NO   |     | NULL    |                |
| estado     | enum('PRESENTE','AUSENTE','RETRASO','JUSTIFICADA') | NO   |     | NULL    |                |
| usuario_id | int(11)                                            | NO   | MUL | NULL    |                |
+------------+----------------------------------------------------+------+-----+---------+----------------+
*/

--
-- Estructura de tabla para la tabla horario_empleado
--
CREATE TABLE IF NOT EXISTS horario_empleado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dia_semana ENUM('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES') NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    margen TIME NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* Resultado de la query
+--------------+---------+------+-----+---------+----------------+
| Field        | Type    | Null | Key | Default | Extra          |
+--------------+---------+------+-----+---------+----------------+
| id           | int(11) | NO   | PRI | NULL    | auto_increment |
| hora_entrada | time    | NO   |     | NULL    |                |
| hora_salida  | time    | NO   |     | NULL    |                |
| margen       | int(11) | NO   |     | NULL    |                |
| usuario_id   | int(11) | NO   | MUL | NULL    |                |
+--------------+---------+------+-----+---------+----------------+
*/

/* INSERCIONES DE HORARIOS EMPLEADOS */
INSERT INTO horario_empleado (dia_semana, hora_entrada, hora_salida, margen, usuario_id)
VALUES ('LUNES', '14:30:00', '21:00:00', 10, 2);

INSERT INTO horario_empleado (dia_semana, hora_entrada, hora_salida, margen, usuario_id)
VALUES ('LUNES', '07:30:00', '14:30:00', 10, 3);


--
-- Estructura de tabla para la tabla modulo
--
CREATE TABLE IF NOT EXISTS modulo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    profesor_id INT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* Resultado de la query
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| nombre      | varchar(100) | NO   |     | NULL    |                |
| profesor_id | int(11)      | NO   | MUL | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
*/

/* INSERCIONES DE MODULOS */
INSERT INTO modulo (nombre, profesor_id)
VALUES ('Programación', 2);

INSERT INTO modulo (nombre, profesor_id)
VALUES ('Bases de datos', 2);

--
-- Estructura de tabla para la tabla modulo_horario
--
CREATE TABLE IF NOT EXISTS modulo_horario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dia_semana ENUM('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    margen INT NOT NULL,
    modulo_id INT NOT NULL,
    FOREIGN KEY (modulo_id) REFERENCES modulo(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/* Resultado de la query
+-------------+-------------------------------------------------------+------+-----+---------+----------------+
| Field       | Type                                                  | Null | Key | Default | Extra          |
+-------------+-------------------------------------------------------+------+-----+---------+----------------+
| id          | int(11)                                               | NO   | PRI | NULL    | auto_increment |
| dia_semana  | enum('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES') | NO   |     | NULL    |                |
| hora_inicio | time                                                  | NO   |     | NULL    |                |
| hora_fin    | time                                                  | NO   |     | NULL    |                |
| modulo_id   | int(11)                                               | NO   | MUL | NULL    |                |
+-------------+-------------------------------------------------------+------+-----+---------+----------------+
*/

/* INSERCIONES DE MODULOS HORARIOS */
INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('LUNES', '08:00:00', '09:00:00', 10, 1);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('MARTES', '09:00:00', '10:00:00', 10, 1);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('MIERCOLES', '10:00:00', '11:00:00', 10, 1);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('JUEVES', '11:30:00', '12:30:00', 10, 1);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('VIERNES', '12:30:00', '13:30:00', 10, 1);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('LUNES', '15:30:00', '16:30:00', 10, 2);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('MARTES', '16:30:00', '17:30:00', 10, 2);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('MIERCOLES', '18:00:00', '19:00:00', 10, 2);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('JUEVES', '19:30:00', '20:30:00', 10, 2);

INSERT INTO modulo_horario (dia_semana, hora_inicio, hora_fin, margen, modulo_id)
VALUES ('VIERNES', '20:00:00', '21:00:00', 10, 2);
