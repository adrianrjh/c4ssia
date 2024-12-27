import qrcode
import csv
import pandas as pd

def generar_qr(texto, nombre_archivo):
    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agrega el texto al objeto QRCode
    qr.add_data(texto)
    qr.make(fit=True)

    # Genera la imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Guarda la imagen en un archivo
    img.save('../data/qrs/'+nombre_archivo)

# Lee el archivo Excel
df = pd.read_excel('../data/villana.xlsx')
# Itera sobre cada fila del DataFrame
for index, row in df.iterrows():
    if index > 0:
        proyecto = row[0]
        poste = row[1]
        coordenadas = str(row[2])+','+str(row[3])
        idcaja = row[4]
        texto = proyecto+'/'+poste+'/'+coordenadas+'/'+idcaja
        nombre_archivo = idcaja+'.png'
        generar_qr(texto, nombre_archivo)