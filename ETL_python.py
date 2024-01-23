import os
import pandas as pd
from datetime import datetime
import pyodbc

class ETL:
    def __init__(self, parametros_conexion):
        """Inicializamos el ETL."""

        self.parametros_conexion = parametros_conexion
        self.path_carpeta_entrada = os.path.join(os.getcwd(), 'DATA')
        self.path_carpeta_salida = os.path.join(os.getcwd(), 'TEMP_DATA')
        self.crear_carpetas()

    def crear_carpetas(self):
        """Crea las carpetas de entrada y salida si no existen."""
        for carpeta in [self.path_carpeta_entrada, self.path_carpeta_salida]:
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                print(f"Se creó la carpeta: {carpeta}")

    def read_files(self):
        """Cargamos archivos CSV en la carpeta de entrada."""
        dfs = {}
        for archivo in os.listdir(self.path_carpeta_entrada):
            archivo_path = os.path.join(self.path_carpeta_entrada, archivo)
            try:
                if archivo.startswith("MML"):
                    df = pd.read_csv(
                        archivo_path,
                        header= 0,
                        sep=";"
                        )
                    dfs[archivo] = df
                elif archivo.startswith("TAR_PROD"):
                    df = pd.read_csv(
                        archivo_path,
                        header= 0,
                        sep=","
                        )
                    dfs[archivo] = df
                elif archivo.startswith("ARG_UDO"):
                    df = pd.read_csv(
                        archivo_path,
                        header= 0,
                        sep=","
                        )
                    dfs[archivo] = df
            except pd.errors.ParserError as e:
                print(f"Error al cargar {archivo}: {e}")
        return dfs

    def perform_operations(self, dataframes):
        """Realizamos las operaciones de selección de columnas correspondientes a la base."""
        transformed_dataframes = []
        
        for nombre_archivo, df in dataframes.items():
            try:
                if nombre_archivo.startswith("TAR_PROD"):
                    selected_columns = ['MSISDN', 'PRODUCT_ID', 'CREATIONDATE']
                elif nombre_archivo.startswith("MML"):
                    selected_columns = ['Linea', 'Tipo Documento', 'Nro de Documento', 'Genero', "ESTADO LINEA"]
                elif nombre_archivo.startswith("ARG_UDO"):
                    selected_columns = ["MSISDN", "BALANCE"]
                else:
                    raise ValueError(f"Nombre de archivo no manejado: {nombre_archivo}")

                transformed_df = df[selected_columns]
                transformed_dataframes.append(transformed_df)

            except (AttributeError, ValueError) as e:
                print(f"Error al procesar {nombre_archivo}: {e}")

        return transformed_dataframes
    def conectar_bd(self):
        try:
            conexion = pyodbc.connect('DRIVER={SQL Server};'
                                      f'SERVER={self.parametros_conexion["port"]};'
                                      f'DATABASE={self.parametros_conexion["database"]};'
                                      'Trusted_Connection=yes;'
                                      f'UID={self.parametros_conexion["username"]};'
                                      f'PWD={self.parametros_conexion["password"]};')
            print("Conexión exitosa")
            return conexion  # Devuelve la conexión para que pueda ser utilizada fuera del método si es necesario.

        except pyodbc.Error as e:
            print("Ocurrió un error de pyodbc al conectar a SQL Server: ", e)
            return None  # Devuelve None en caso de error.
        except Exception as e:
            print(f"Error general en la función de carga: {e}")
            return None  # Devuelve None en caso de error.

    def load_database(self, dfs, transformed_dataframes):
        """Cargamos los DataFrames en la base de datos."""
        try:
            conexion = self.conectar_bd()

            if conexion:
                for nombre_archivo, df in zip(dfs.keys(), transformed_dataframes):
                    try:
                        if nombre_archivo.startswith("TAR_PROD"):
                            nombre_tabla = self.parametros_conexion["TAR_PROD"]
                            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
                        elif nombre_archivo.startswith("MML"):
                            nombre_tabla = self.parametros_conexion["MML"]
                            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
                        elif nombre_archivo.startswith("ARG_UDO"):
                            nombre_tabla = self.parametros_conexion["ARG_UDO"]
                            df.to_sql(nombre_tabla, conexion, if_exists='replace', index=False)
                        else:
                            raise ValueError(f"Nombre de archivo no manejado: {nombre_archivo}")
                    except Exception as e:
                        print(f"Error al cargar {nombre_archivo}: {e}")
        except Exception as e:
            print(f"Error general en la función de carga: {e}")
        finally:
            if conexion:
                conexion.close()
                print("Conexión cerrada")
    
    def save_files(self, dfs, transformed_dataframes):
        """Guardamos los archivos en la carpeta de salida."""
        try:
            for nombre_archivo, df in zip(dfs.keys(), transformed_dataframes):
                try:

                    if nombre_archivo.startswith("TAR_PROD"):
                        nombre_archivo_salida = "TAR_PROD"
                    elif nombre_archivo.startswith("MML"):
                        nombre_archivo_salida = "MML"
                    elif nombre_archivo.startswith("ARG_UDO"):
                        nombre_archivo_salida = "ARG_UDO"
                    else:
                        raise ValueError(f"Nombre de archivo no manejado: {nombre_archivo}")

                    ruta_completa = os.path.join(self.path_carpeta_salida, nombre_archivo_salida)
                    df.to_csv(f"{ruta_completa}.csv", index=False) 
                except Exception as e:
                    print(f"Error al escribir {nombre_archivo} como archivo en carpeta destino. {e}")
        except Exception as e:
            print(f"Error general en la función de carga: {e}") 

    def main(self):
        """Ejecutamos el ETL."""
        try:
            dfs = self.read_files()
            transformed_dataframes = self.perform_operations(dfs)
            self.save_files(dfs, transformed_dataframes)
            print("Archivos guardados")
        except Exception as e:
            print(f"Error al ejecutar el ETL: {e}")

        #try:
            #self.load_database(dfs, transformed_dataframes)
        #except Exception as e:
            #print(f"Error intentando cargar datos en la base de datos: {e}")

if __name__ == "__main__":
    parametros_conexion = {
        "host": "dbsqlsudp01",
        "port": "1433",
        "username": "dcolapie",
        "password": "Chuni*1518+",
        "database": "SUDP",
        "TAR_PROD": "[TMOVILES\ALCARRIZ].Pedro_AA_Producto",
        "MML": "[TMOVILES\ALCARRIZ].Pedro_AA_MML",
        "ARG_UDO": "[TMOVILES\ALCARRIZ].Pedro_AA_Saldos"
        }
    etl = ETL(parametros_conexion)
    etl.main()