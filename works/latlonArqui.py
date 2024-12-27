############ L 	A 	T - L 	O   N 		T 	O 		 U 	T 	M ############
import numpy as np
from pandas import DataFrame, read_excel
from pyproj import Proj

# Leer datos desde un archivo Excel
df = read_excel('coordenadasvilla.xlsx')

# Configuración del proyector para convertir a UTM
myProj = Proj("+proj=utm +zone=13 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
# Convertir latitudes y longitudes a UTM
UTMx, UTMy = myProj(df['LONGITUD'].values, df['LATITUD'].values)
# Crear DataFrame y guardar en CSV
df_utm = DataFrame(np.c_[df['POSTE'], df['MATERIAL'], UTMx, UTMy, df['LATITUD'], df['LONGITUD']], columns=['POSTE', 'MATERIAL', 'UTMx', 'UTMy', 'LATITUD', 'LONGITUD'])
# Guardar en archivo Excel

df_utm.to_excel('coordenadasvilla'+'-converted'+'.xlsx', index=False)

############ U 	T 	M 		T 	O 		L 	A 	T - L 	O   N ############
#import pandas as pd
#from pyproj import Proj, Transformer
#
## Define el sistema de coordenadas UTM y WGS84
#transformer = Transformer.from_crs("epsg:32613", "epsg:4326")  # Ajusta el EPSG de la zona UTM según sea necesario
## Lee el archivo de Excel
#df = pd.read_excel('Coordenadas_Amarradero_Tinajas_PAnzar.xlsx')
## Asumiendo que las columnas se llaman 'Easting' y 'Northing'
#def utm_to_latlon(utmx, utmy):
#    lon, lat = transformer.transform(utmx, utmy)
#    return lon, lat
## Aplica la conversión a cada fila
#df[['LATITUD', 'LONGITUD']] = df.apply(lambda row: utm_to_latlon(row['UTMx'], row['UTMy']), axis=1, result_type='expand')
#
## Guarda el resultado en un nuevo archivo de Excel
#df.to_excel('Coordenadas_Amarradero_Tinajas_PAnzar-converted.xlsx', index=False)