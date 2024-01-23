El programa principal con nombre Ejecutable.ps1 o Ejecutable.sh (de acuerdo al sistema operativo donde corra) ejecuta la secuencia de scripts validando condiciones para avanzar:
* Previo a la ejecución elimina la carpeta Altamira/TEMP_DATA a fin de asegurarnos de siempre tomar el último registro. 
* En primer lugar el script ETL_python.py toma la información de la carpeta DATA selecciona y filtra los campos correspondientes acorde a los requerimientos de la base y los guarda en la carpeta TEMP_DATA (Al no existir al ejecutarse por primera vez la crea). Genera archivos .csv uno por cada archivo de origen. El script toma los archivos de la carpeta de origen por la forma en que comienza (validando ARG_UDO, MML y TAR_PROD) por lo que si no queremos actualizar los datos de una tabla en particular, simplemente lo eliminamos de la carpeta DATA o bien le modificamos el nombre agregándole un __ al comienzo. Esto hará que no reconozca el nombre, lo saltee en su lectura y no lo guarde en la carpeta TEMP_DATA.

* Luego los script en Java .jar, ubicados en la carpeta Altamira/AA_Envio_Lineas uno por cada tabla. Los mismos realizan la lectura del csv correspondiente ubicado en la carpeta Altamira/TEMP_DATA, establecen la conexión a la base de datos, eliminan los datos existentes en la tabla correspondiente e ingestan los datos del .csv tomando batch de a 100.000 registros. El Ejecutable valida la existencia del archivo .csv correspondiente en la carpeta Altamira/TEMP_DATA y si existe procede a la ejecución del .jar correspondiente. Si no existe el .csv imprime por pantalla que no existe el archivo y continúa con el siguiente. 


Finalmente el segundo programa CreadorMetadatos genera metadata de los archivos generados con el programa anterior, que campos, tipo de dato en cada campo, longitud máxima de cada campo, existencia o no de valores nulos y si el campo posee valores unicos o repetidos. 

El generador de metadatos CreadorMetadatos toma los archivos creados en la carpeta Altamira/TEMP_DATA por el Ejecutable por ende siempre es necesario haber ejecutado alguna vez el ejecutable a fin de que cree primero los archivos y evitar que de error. 

Para ejecución con ambiente linux ejecutar:
 *  ejecutable.sh
 *  creador_metadatos.sh
Para ejecución con ambiente Windows desde una terminal ejecutar:
 *  ejecutable.ps1
 *  creador_metadatos.ps1

Para ejecución con ambiente windows y directamente haciendo doble click a la aplicación en el directorio:
 * Ejecutable.exe
 * CreadorMetadatos.exe


Estructura del proyecto:

```

Altamira/
│   ├── DATA/
│       ├── ARG_UDO_restodelnombre.txt
│       ├── MML_restodelnombre.csv
│       └── TAR_PROD_restodelnombre.csv
│   ├── TEMP_DATA/      #Esta capeta no existe se crea con la ejecución del programa
│   └── AA_Envio_Lineas/
│       ├── MML.jar
│       ├── Productos.jar
│       └── Saldos
│   ├── entorno/
│       └── carpetas del entorno virtual 
|   ├── ETL_python.py
|   ├── creador_metadatos.py
|   ├── Ejecutable.ps1
|   ├── Ejecutable.exe
|   ├── Ejecutable.sh
|   ├── CreadorMetadatos.ps1
|   ├── CreadorMetadatos.exe
|   ├── CreadorMetadatos.sh
|   ├── requirements.txt
|   ├── _Lineas_AA_Importacion_Definiciones.txt
|   ├── Dockerfile
|   └── otros_archivos...

```

Saludos: 

*Pedro Bonafé*
