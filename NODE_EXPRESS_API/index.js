import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
// Importa las bibliotecas necesarias para interactuar con tu programa de Python
import { exec } from 'child_process';

import usersRoutes from './routes/users.js';


const app = express();
app.use(cors());
const PORT = 5000;

app.use(bodyParser.json());

app.use('/users', usersRoutes);

app.get('/', (req,res) => {res.send('Hello from Homepage.');});

// Ruta para enviar datos a Python y obtener resultados
app.get('/api/python', (req, res) => {
    const pythonScriptPath = 'DeviceFinder.py'; // Ruta al archivo Python
    const folderPath = './pyscript'; // Ruta a la carpeta que deseas ingresar
    // Comando para navegar a la carpeta deseada
    const cdCommand = `cd ${folderPath} && `;
    // Comando para ejecutar el script de Python
    const pythonCommand = `python ${pythonScriptPath}`;
    // Combinar los comandos para ejecutarlos en una sola llamada
    const command = cdCommand + pythonCommand;
    // Ejecutar el script de Python
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error al ejecutar el script de Python: ${error}`);
            res.status(500).send('Error interno del servidor');
            return;
        }
        res.json(JSON.parse(stdout));
        
    });
});

app.listen(PORT, () => console.log(`Server Running on port: http://localhost:${PORT}`));