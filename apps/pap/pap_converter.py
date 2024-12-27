from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys, random
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common4 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import *
import csv
import os, qrcode, shutil
import os.path
import numpy as np
from pandas import DataFrame, read_excel
from pyproj import Proj
import pandas as pd
from pyproj import Proj, Transformer

async def paso1(q: Q):
    del q.page['converterFile']

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    q.page['converterFile'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
        ui.text_xl('Convertidor de Coordenadas'),
        ui.combobox(name='textconvertir', label='Convertir a:', value='Seleccionar', choices=['UTM->GEOGRAFICA', 'GEOGRAFICA->UTM'],trigger=True),
        ui.text_l('Ahorrate tiempo, es gratis! (Solo por hoy)'),
        ui.file_upload(name='upload_convert', label='Convert', multiple=True, compact=False),
    ])

    q.page['creatorQR'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
        ui.text_xl('Generador de códigos QR'),
        ui.text_l('Ahorrate tiempo, es gratis! (Solo por hoy)'),
        ui.file_upload(name='upload_generator', label='Generate', multiple=True, compact=False),
    ])

    await q.page.save()

async def pap_converter(q: Q):
    print(str("starting pap_converter..."))
    global ipGlobal,session, convertir

    q.page['meta'] = ui.meta_card(box='')

    if q.args.home:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.settings:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/settings'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.logout:
        session = False
        puesto = ''
        json_datos = json.dumps({"session":session, "puesto":puesto})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAtrasH:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_pap'
        await q.page.save()

    if q.args.textconvertir:
        if q.args.textconvertir != 'Seleccionar':
            convertir = str(q.args.textconvertir)
        await q.page.save()

    if q.args.upload_convert:
        links = q.args.upload_convert
        if links:
            if convertir != 'Seleccionar' and convertir != '':
                if convertir == 'UTM->GEOGRAFICA':
                    try:
                        # Leer datos desde un archivo Excel
                        local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                        local_path1 = local_path.split('/')
                        docConverted = local_path1[7].split('.')
                        docConverted1 = '../../data/'+docConverted[0]+'-converted.'+docConverted[1]                
                        # Define el sistema de coordenadas UTM y WGS84
                        transformer = Transformer.from_crs("epsg:32613", "epsg:4326")  # Ajusta el EPSG de la zona UTM según sea necesario
                        # Lee el archivo de Excel
                        df = pd.read_excel(local_path)
                        # Asumiendo que las columnas se llaman 'Easting' y 'Northing'
                        def utm_to_latlon(utmx, utmy):
                            lon, lat = transformer.transform(utmx, utmy)
                            return lon, lat
                        # Aplica la conversión a cada fila
                        df[['LATITUD', 'LONGITUD']] = df.apply(lambda row: utm_to_latlon(row['UTMx'], row['UTMy']), axis=1, result_type='expand')
                        # Guarda el resultado en un nuevo archivo de Excel
                        df.to_excel(docConverted1, index=False)
                    except Exception as e:
                        print(e)
                if convertir == 'GEOGRAFICA->UTM':
                    try:
                        # Leer datos desde un archivo Excel
                        local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                        df = read_excel(local_path)
                        local_path1 = local_path.split('/')
                        docConverted = local_path1[7].split('.')
                        docConverted1 = '../../data/'+docConverted[0]+'-converted.'+docConverted[1]
                        ## Configuración del proyector para convertir a UTM
                        myProj = Proj("+proj=utm +zone=13 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
                        ## Convertir latitudes y longitudes a UTM
                        UTMx, UTMy = myProj(df['LONGITUD'].values, df['LATITUD'].values)
                        ## Crear DataFrame y guardar en CSV
                        df_utm = DataFrame(np.c_[df['POSTE'], df['MATERIAL'], UTMx, UTMy, df['LATITUD'], df['LONGITUD']], columns=['POSTE', 'MATERIAL', 'UTMx', 'UTMy', 'LATITUD', 'LONGITUD'])
                        ## Guardar en archivo Excel
                        df_utm.to_excel(docConverted1, index=False)
                    except Exception as e:
                        print(e)
                download_path, = await q.site.upload([docConverted1])
                del q.page['converterFile']
                q.page['converterFile'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
                    ui.text_xl('Convertido con éxito, disfrutalo!'),
                    ui.link(label=f'{os.path.basename(download_path)}', download=True, path=download_path),
                    ui.button(name='back', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_generator:
        links = q.args.upload_generator
        if links:
            try:
                # Leer datos desde un archivo Excel
                local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                # Lee el archivo Excel
                df = read_excel(local_path)
                # Itera sobre cada fila del DataFrame
                for index, row in df.iterrows():
                    #if index > 0:
                    proyecto = row[0]
                    poste = row[1]
                    coordenadas = str(row[2])+','+str(row[3])
                    idcaja = row[4]
                    texto = proyecto+'/'+poste+'/'+coordenadas+'/'+idcaja
                    nombre_archivo = idcaja+'.png'
                    namedir = proyecto.replace(" ", "")
                    output_dir = generar_qr(texto, nombre_archivo, namedir)
                shutil.make_archive(output_dir, 'zip', output_dir)
                # Eliminar la carpeta después de crear el archivo ZIP
                shutil.rmtree(output_dir)
            except Exception as e:
                print(e)
            filezip = output_dir.split("/")
            output_dir = filezip[0]+'/'+filezip[1]+'/'+filezip[2]+'/'+filezip[3]+'/'+filezip[4]+'/'+filezip[5]+'/'+filezip[6]+'/'+filezip[7]+'/'+filezip[8]+'.zip'
            download_path, = await q.site.upload([output_dir])
            del q.page['creatorQR']
            q.page['creatorQR'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
                ui.text_xl('Archivo generado con éxito, disfrutalo!'),
                ui.link(label=f'{os.path.basename(download_path)}', download=True, path=download_path),
                ui.button(name='back', label='Back', primary=True)
            ])
        await q.page.save()

    if q.args.back:
        await q.run(paso1, q)
        await q.page.save()

    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        #if session != True:
        #    q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        #    await q.page.save()
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='8%', zones=[
                                ui.zone('izq1_11',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('der1',size='92%', zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='50%', align='center', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_12', size='50%', align='center', direction=ui.ZoneDirection.ROW),
                                    ]),
                                    ui.zone('der1_2',size='0%', zones=[
                                        ui.zone('der1_21', size='100%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_pap_converter'] = ui.header_card(
            box='header',
            title='C 4 S S I A',
            subtitle='YAA Internet',
            items=[ui.menu(image=image,items=[ui.command(name='home', label='Home', icon='Home'),ui.command(name='settings', label='Settings', icon='Settings'),ui.command(name='logout', label='Logout', icon='SignOut')])]
        )

        await q.run(paso1, q)
        await q.page.save()

@app('/pap_converter', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_converter(q)