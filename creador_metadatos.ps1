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

# 4. Ejecuta el script ETL_python.py
python .\Metadatos.py

# Desactiva el entorno virtual cuando hayas terminado
deactivate
