Se diseña un proyecto que me permita recopilar la información del inicio de sesión de usuarios a traves de botones de acceso con cuentas Google.

El desarrollo contará con una interfaz muy sencilla en HTML integrado a Python con un botón que diga "Iniciar sesión con Google"

![image](https://github.com/user-attachments/assets/371ac2a7-1c58-4314-86d6-707d33c62040)

Una vez el usuario se registre por medio de la API Google, obtendremos la imformación de Username, Email, Foto de Perfil y Fecha de inicio de sesión. 
La información será capturada por POST mediante Ajax y se retorna a una función que me permitirá transmitir los datos por medio de un topico creado en Kafka.

