# Usa una imagen base que incluya Python y Java
FROM openjdk:11-jre-slim

# Establece el directorio de trabajo en /Altamira
WORKDIR /Altamira

# Copia los archivos necesarios al contenedor
COPY Altamira /Altamira
COPY tu_script_python.py /Altamira

# Instala las dependencias de Python (si es necesario)
RUN apt-get update && apt-get install -y python3

# Define el comando por defecto al ejecutar el contenedor
CMD ["sh", "Ejecutable.sh"]
