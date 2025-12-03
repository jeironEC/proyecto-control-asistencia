Ese es el flujo de Node-Red, hay algunos nodos function demas, ya que estoy haciendo pruebas y trato de similar el arduino ya que no lo tengo

El error que me sale es este:

msg.payload should be an object or an array containing the query arguments.


Codigo probado para el function:

// msg.payload viene del Inject:
// {
//   "thing": "ESP32",
//   "tag": "63768a18",
//   "datetime": "2025-12-03 15:55:10",
//   "evento": "lectura",
//   "estado": "PRESENTE",
//   "user": { "id": "1", "nombre": "jusepe", "apellido": "hogwart", "email": "jusepe@gmail.com" }
// }

// 1️ Separar fecha y hora
let datetime = msg.payload.datetime || new Date().toISOString();
let parts = datetime.split(' ');
let fecha = parts[0];
let hora = parts[1];

// 2️ Preparar INSERT
msg.topic = "INSERT INTO asistencia (fecha, hora, estado, usuario_id) VALUES (?, ?, ?, ?)";

// 3️ msg.payload debe ser un array con los valores
msg.payload = [
    fecha,
    hora,
    msg.payload.estado || 'PRESENTE',
    msg.payload.user.id
];

return msg;