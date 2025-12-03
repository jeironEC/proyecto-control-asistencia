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

--
-- Estructura de tabla para la tabla asistencia
--
CREATE TABLE IF NOT EXISTS asistencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha date NOT NULL,
    hora time NOT NULL,
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