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
    rol ENUM('ALUMNO','PROFESOR','PERSONALSERVICIO') NOT NULL,
    activo tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla modulo
--
CREATE TABLE IF NOT EXISTS modulo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla alumno
--
CREATE TABLE IF NOT EXISTS alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    matricula VARCHAR(80) NOT NULL UNIQUE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla profesor
--
CREATE TABLE IF NOT EXISTS profesor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    modulo_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (modulo_id) REFERENCES modulo(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla personal_servicio
--
CREATE TABLE IF NOT EXISTS personal_servicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    cargo VARCHAR(100) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Estructura de tabla para la tabla asistencia
--
CREATE TABLE IF NOT EXISTS asistencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha date NOT NULL,
    hora_inicio time NOT NULL,
    hora_fin time NOT NULL,
    estado ENUM('PRESENTE','AUSENTE','RETRASO','JUSTIFICADA') NOT NULL,
    modulo_id INT NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (modulo_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- -------------------------------------------------------------------------------------------------------------------