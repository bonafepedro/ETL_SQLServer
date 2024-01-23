$scriptDirectory = Get-Location
$entornoVirtual = Join-Path $scriptDirectory "entorno\Scripts\activate"
# 1. Activa el entorno virtual
#& $entornoVirtual
#entorno\Scripts
 .\entorno\Scripts\activate

# 2. Actualiza pip
py -m pip install --upgrade pip
# 3. Instala las dependencias desde requirements.txt
#pip install -r requirements.txt si este no anda ejecutar las lineas de abajo	
pip install pandas
pip install numpy
pip install pyodbc
pip install pyarrow
pip install fastparquet
pip install openpyxl

# 4. Eliminamos la carpeta TEMP_DATA si existe
if (Test-Path -Path .\TEMP_DATA) {
    Remove-Item -Path .\TEMP_DATA -Recurse -Force
}

# 5. Ejecuta el script ETL_python.py
python .\ETL_python.py

# 6. Desactiva el entorno virtual cuando hayas terminado
deactivate

# 7. Verifica si el archivo MML.csv existe en la carpeta TEMP_DATA y ejecuta el archivo .jar si existe
if (Test-Path -Path .\TEMP_DATA\MML.csv -PathType Leaf) {
    java -jar .\AA_Envio_Lineas\MML.jar
} else {
    Write-Host "El archivo MML.csv no existe en la carpeta TEMP_DATA. No se ejecutara el archivo MML.jar"
}
if (Test-Path -Path .\TEMP_DATA\TAR_PROD.csv -PathType Leaf) {
    java -jar .\AA_Envio_Lineas\Productos.jar
} else {
    Write-Host "El archivo TAR_PROD.csv no existe en la carpeta TEMP_DATA. No se ejecutara el archivo Productos.jar"
}
if (Test-Path -Path .\TEMP_DATA\ARG_UDO.csv -PathType Leaf) {
    java -jar .\AA_Envio_Lineas\Saldos.jar
} else {
    Write-Host "El archivo ARG_UDO.csv no existe en la carpeta TEMP_DATA. No se ejecutara el archivo Saldos.jar"
}

