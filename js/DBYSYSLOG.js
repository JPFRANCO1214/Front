const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const net = require('net');

const app = express();
const port = 3015; // Cambiado a puerto 3001

// Configuración de la base de datos
const db = new sqlite3.Database('deviceConfiguration.db');

// Configuración de conexión del servidor syslog
const syslogHost = '127.0.0.1';  // Dirección IP del servidor syslog
const syslogPort = 12349;         // Puerto del servidor syslog

let receivedList = [];  // Variable para almacenar la lista recibida

// Crear servidor TCP para syslog
const syslogServer = net.createServer((socket) => {
    console.log('Cliente syslog conectado desde: ' + socket.remoteAddress + ':' + socket.remotePort);

    // Manejar datos recibidos del cliente syslog
    socket.on('data', (data) => {
        try {
            const receivedData = JSON.parse(data.toString()); // Convertir datos recibidos a objeto JavaScript
            console.log('Datos recibidos del cliente syslog:', receivedData);

            // Almacenar la lista recibida en la variable receivedList
            receivedList = receivedData;

            // Aquí puedes hacer más operaciones con los datos recibidos, como guardarlos en la base de datos, etc.

        } catch (error) {
            console.error('Error al procesar datos recibidos del cliente syslog:', error.message);
        }
    });

    // Manejar eventos de cierre de conexión con el cliente syslog
    socket.on('close', () => {
        console.log('Cliente syslog desconectado.');
    });

    // Manejar errores de conexión con el cliente syslog
    socket.on('error', (error) => {
        console.error('Error de conexión con cliente syslog:', error.message);
    });
});

// Iniciar el servidor syslog
syslogServer.listen(syslogPort, syslogHost, () => {
    console.log(`Servidor syslog TCP escuchando en ${syslogHost}:${syslogPort}`);
});

// Ruta para obtener la lista de dispositivos desde la base de datos
app.get('/devices', (req, res) => {
    db.all("SELECT * FROM DeviceConfiguration", (err, rows) => {
        if (err) {
            console.error('Error al obtener configuraciones de dispositivos desde la base de datos:', err.message);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            console.log("Configuraciones de dispositivos obtenidas desde la base de datos.");
            res.json(rows);
        }
    });
});

// Ruta de inicio para servir la página web
app.get('/', (req, res) => {
    // Sirve tu página HTML aquí
    res.sendFile(__dirname + '/../../index.html');
});

// Manejar errores de servidor Express
app.use((err, req, res, next) => {
    console.error('Error en el servidor Express:', err.stack);
    res.status(500).send('Something broke!');
});

// Iniciar el servidor Express en el puerto 3001
app.listen(port, () => {
    console.log(`Servidor Express corriendo en http://localhost:${port}`);
});
