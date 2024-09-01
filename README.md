Se diseña un proyecto que me permita recopilar la información del inicio de sesión de usuarios a traves de botones de acceso con cuentas Google.

El desarrollo contará con una interfaz muy sencilla en HTML integrado a Python con un botón que diga "Iniciar sesión con Google"

![image](https://github.com/user-attachments/assets/371ac2a7-1c58-4314-86d6-707d33c62040)

Una vez el usuario se registre por medio de la API Google, obtendremos la imformación de Username, Email, Foto de Perfil y Fecha de inicio de sesión. 
La información será capturada por POST mediante Ajax y se retorna a una función que me permitirá transmitir los datos por medio de un topico creado en Kafka.

Entendiendo una posible escalabilidad del proyecto, se crea un broker con kafka para permitr el streaming de datos a partir de diferentes microservicios o fuentes de información, donde almacenaremos los datos en un Data Lake de Azure a través de una estructura ELT para permitir su posterior procesamiento sin realentizar la obtención inicial de datos.

![proyectoPresentacion](https://github.com/user-attachments/assets/3d68c8e5-3694-45ae-8834-5cb29d332b68)

Para establecer conexión con el broker kafka se debe inicializar zookeper y crear un tópico y un producer para enviar los mensajes. Se crea el scriptconfigPipeline el cual se suscribirá al topico creado y almacenerá todos los mensajes publicados por el broker en el Data Lake de azure. Los mensajes se guardaran en formato JSON.

Para la extracción de datos y almacenamiento a traves de un primer ETL se configurarán DAG´s a traves de Airflow. Se creará un DAG con actividades importadas de un script llamado azureEtl el cual se encuenra en la carpeta LinuxDags. Para el uso de Airflow, optaremos por inicializar ubuntu en windows y crear un entonrno virtual para no interferir con las demás dependencias.

Una vez ejecutado el airflow, el DAG dagEtl me extraerá los datos, los transformará eliminando elementos repetidos y elementos nulos y los cargará en formato JSON para obtener una nueva capa silver en Azure Blob. Esta capa silver nos permitirá disponer de los datos de manera sencilla y con la información necesaria para generar datos en una capa Gold según sea necesario.

Para finalizar el procesamiento y presentación de daos se creará una base de datos no estructurada en mongoDB, la cual tendrá como proposito almacenar la capa gold de la información permitiendonos así la extracción de datos necesaria haciendo mas rápida la consulta.
Este proceso de ETL se llevará a cabo en el script goldDB.py.

Una vez los datos procesados se creará un DashBoard simple utilizando la librería Dash de python.

![image](https://github.com/user-attachments/assets/35165bdd-eef8-41e0-a481-4a2963896161)

Diagrama de procesos:

![Etl](https://github.com/user-attachments/assets/6ce71215-34f0-4c64-9376-0eb52878f39d)




