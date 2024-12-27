from h2o_wave import Q, app, main, ui, AsyncSite, site, data
import threading, json, time, datetime, math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/apps/iis/libs')
from common3_iis import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import csv
import asyncio

class Listener1(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis, self.init = r, 0
        self.pubsub = self.redis.pubsub()
        print('Listener1...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)

    def work(self, item):
        global session, puesto, username
        data = 0
        try:
            data = json.loads(item.decode('utf8'))
            session = data['session']
            puesto = data['puesto']
            username = data['username']
        except Exception as e:
            print(e)

    def work2(self, item):
        global data_rows
        global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4

        data = 0
        try:
            data = json.loads(item.decode('utf8'))
            data_rows.append([
                str(data['id_ticket']),
                str(data['name_client']),
                str(data['address_client']),
                str(data['localidad_client']),
                str(data['phone_client']),
                str(data['paqueteplan']),
                str(data['date_ticket']),
                str(data['username']),
                str(data['status']),
                str(data['date_status'])])
            paso1P = 1
            paso2P = 0
            paso3P = 0
            bandPaso1 = 0
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message['channel'].decode("utf-8") == "last_session":
                        self.work(message['data'])
                    if message['channel'].decode("utf-8") == "tickets_iis":
                        self.work2(message['data'])
                    else:
                        pass
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['last_session', 'tickets_iis', 'yi_pdfs_iis'])
                        break
            time.sleep(0.001)  # be nice to the system :)

#client = Listener1(r, ['last_session', 'tickets_iis', 'yi_pdfs_iis'])
#client.start()

async def paso1(q: Q):
    ################# P    A   S   O       1 #################
    global data_rows
    del q.page['lista-ing-show']
    del q.page['infoticketcreated']
    del q.page['listado-materials']
    del q.page['btnTransitoMaps']
    del q.page['aprovisioning-client']

    data_rows = getAllTicketsIIS(r, 'tickets_iis_key', 'tickets_iis')
    for x in range(0, len(data_rows)):
        counter =+ 1
        ticketcomplete = getTicketIIS(r, data_rows[x][0])
        q.page['lista-ing-show'+str(counter)] = ui.form_card(box=ui.box('der1_12', order=counter), items=[
            ui.text_xl(content='Ticket '+str(ticketcomplete['proceso'])+' '+str(counter)),
            ui.text_l(content="Nombre del cliente: "+str(ticketcomplete['name_client'])),
            ui.text_l(content="Domicilio: "+str(ticketcomplete['address_client'])),
            ui.text_l(content="Localidad: "+str(ticketcomplete['localidad_client'])),
            ui.text_l(content="Contacto: "+str(ticketcomplete['phone_client'])),
            ui.text_l(content="Cita instalación: "+str(ticketcomplete['cita_instalacion'])),
            ui.button(name='btnOpenTicket'+str(counter), label='Abrir Ticket', disabled=False, primary=True)
        ])

    await q.page.save()

async def paso2(q: Q, noticket: str):
    global ticketSelectioned, ticketcomplete, data_rows_materials, data_rows_materials1, data_rows_materials_send
    global installerWorker, matsdevsIIS, marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS

    del q.page['lista-ing-show1']
    del q.page['lista-ing-show2']
    del q.page['lista-ing-show3']
    del q.page['lista-ing-show4']
    del q.page['lista-ing-show5']
    del q.page['lista-ing-show']
    del q.page['infoticketcreated']
    del q.page['listado-materials']
    del q.page['btnTransitoMaps']
    del q.page['aprovisioning-client']

    ticketcomplete = getTicketIIS(r, noticket)
    ################# P    A   S   O       2 #################
    if ticketcomplete['status'] == 'Asigned Material' or ticketcomplete['status'] == 'In Transit':
        instalador = ticketcomplete['instalador'].split('/')
        q.page['infoticketcreated'] = ui.form_card(
            box=ui.box('der1_12', order=1),
            items=[
                ui.text_xl('Información completa de ticket de nuevo cliente'),
                ui.textbox(name='register_noticket', label='N° Ticket', disabled=True, value=str(ticketcomplete['id_ticket'])),
                ui.textbox(name='register_identificacion', label='Identificación Oficial', disabled=True, value=str(ticketcomplete['identificacion'])),
                ui.textbox(name='register_comprobante', label='Comprobante de Domicilio', disabled=True, value=str(ticketcomplete['comprobante'])),
                ui.textbox(name='register_diapropuesto', label='Dia Propuesto', disabled=True, value=str(ticketcomplete['datepicker_client'])),
                ui.textbox(name='register_horapropuesto', label='Hora Propuesto', disabled=True, value=str(ticketcomplete['hora_propuesta'])),
                ui.textbox(name='register_cliente', label='Nombre del Cliente', disabled=True, value=str(ticketcomplete['name_client'])),
                ui.textbox(name='register_domicilio', label='Domicilio', disabled=True, value=str(ticketcomplete['address_client'])),
                ui.textbox(name='register_colonia', label='Colonia', disabled=True, value=str(ticketcomplete['colonia_client'])),
                ui.textbox(name='register_localidad', label='Localidad', disabled=True, value=str(ticketcomplete['localidad_client'])),
                ui.textbox(name='register_municipio', label='Municipio', disabled=True, value=str(ticketcomplete['municipio_client'])),
                ui.textbox(name='register_estado', label='Estado', disabled=True, value=str(ticketcomplete['estado_client'])),
                ui.textbox(name='register_refaddress', label='Referencia', disabled=True, value=str(ticketcomplete['refaddress_client'])),
                ui.textbox(name='register_location', label='Ubicación Geografica', disabled=True, value=str(ticketcomplete['location_client'])),
                ui.textbox(name='register_telefono', label='Teléfono', disabled=True, value=str(ticketcomplete['phone_client'])),
                ui.textbox(name='register_email', label='E-Mail', disabled=True, value=str(ticketcomplete['email_client'])),
                ui.textbox(name='register_creacionticket', label='Fecha de creación de ticket', disabled=True, value=str(ticketcomplete['date_ticket'])),
                ui.textbox(name='register_supporter1', label='Creador del ticket', disabled=True, value=str(ticketcomplete['username'])),
                ui.textbox(name='register_status', label='Status', disabled=True, value=str(ticketcomplete['status'])),
                ui.textbox(name='register_datestatus', label='Date Status', disabled=True, value=str(ticketcomplete['date_status'])),
                ui.textbox(name='textcita_instalacion', label='Cita de Instalación', disabled=True, value=str(ticketcomplete['cita_instalacion'])),
                ui.textbox(name='textinstalador', label='Instalador', disabled=True, value=str(instalador[0])),
            ]
        )

        table_materials_asigned = []
        data_rows_materials1 = json.loads(ticketcomplete['materiales_instalador_asignado'].replace("'","["))
        for x in range(0, len(data_rows_materials1)):
            noserie = data_rows_materials1[x][1]
            marca = data_rows_materials1[x][3]
            modelo = data_rows_materials1[x][4]
            descripcion = data_rows_materials1[x][5]
            table_materials_asigned.append([noserie, marca, modelo, descripcion])
        q.page['listado-materials'] = ui.form_card(
            box=ui.box('der1_12', order=2),
            items=[
                ui.text_xl(content='Lista de equipos/material para instalación de nuevo cliente'),
                ui.table(
                    name='issues',
                    multiple=False,
                    columns=columnsAsigIIS2,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    ) for dato in table_materials_asigned],
                    groupable=False,
                    downloadable=True,
                    resettable=False,
                ),
            ],
        )
        if ticketcomplete['status'] == 'Asigned Material':
            q.page['btnTransitoMaps'] = ui.section_card(title='', subtitle='',box=ui.box('der1_12', order=3),items=[ui.button(name='btnSeeInMaps', label='Mostrar en Maps', disabled = False, primary=False), ui.button(name='btnEnTransito', label='Ir al sitio', disabled = False, primary=True)])
        if ticketcomplete['status'] == 'In Transit':
            q.page['btnTransitoMaps'] = ui.section_card(title='', subtitle='',box=ui.box('der1_12', order=3),items=[ui.button(name='btnSeeInMaps', label='Mostrar en Maps', disabled = False, primary=False), ui.button(name='btnEnProceso', label='En Proceso', disabled = False, primary=True)])
    
    if ticketcomplete['status'] == 'In Process':
        instalador = ticketcomplete['instalador'].split('/')
        q.page['converterFile1'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
            ui.text_xl('Roseta y jumper'),
            ui.file_upload(name='upload_file1', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile2'] = ui.form_card(box=ui.box('der1_12', order=2), items=[
            ui.text_xl('N° SERIE ONT'),
            ui.file_upload(name='upload_file2', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile3'] = ui.form_card(box=ui.box('der1_12', order=3), items=[
            ui.text_xl('Terminal Óptica'),
            ui.file_upload(name='upload_file3', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile4'] = ui.form_card(box=ui.box('der1_12', order=4), items=[
            ui.text_xl('Potencia ONT'),
            ui.file_upload(name='upload_file4', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile5'] = ui.form_card(box=ui.box('der1_12', order=5), items=[
            ui.text_xl('Test de Velocidad'),
            ui.file_upload(name='upload_file5', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile6'] = ui.form_card(box=ui.box('der1_12', order=6), items=[
            ui.text_xl('Etiqueta (sinchos)'),
            ui.file_upload(name='upload_file6', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile7'] = ui.form_card(box=ui.box('der1_12', order=7), items=[
            ui.text_xl('Contrato/Recibo Completado'),
            ui.file_upload(name='upload_file7', label='Subir', multiple=True, compact=False),
        ])

        q.page['converterFile8'] = ui.form_card(box=ui.box('der1_12', order=8), items=[
            ui.text_xl('INE - Comprobante de Domicilio'),
            ui.file_upload(name='upload_file8', label='Subir', multiple=True, compact=False),
        ])

        q.page['textbox-comentarios'] = ui.form_card(box=ui.box('der1_12', order=9), items=[
            ui.textbox(name='text_descripcion', label='Observaciones', trigger=True, multiline=True, width='390px'),
            ui.button(name='btnEndInstallation', label='Aprovisionar', disabled = False, primary=False),
        ])
    await q.page.save()

async def paso3(q: Q):
    ################# P    A   S   O       3 #################
    global ticketcomplete
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4

    del q.page['lista-ing-show1']
    del q.page['lista-ing-show2']
    del q.page['lista-ing-show3']
    del q.page['lista-ing-show4']
    del q.page['lista-ing-show5']
    del q.page['lista-ing-show']
    del q.page['infoticketcreated']
    del q.page['listado-materials']
    del q.page['btnTransitoMaps']
    del q.page['converterFile1']
    del q.page['converterFile2']
    del q.page['converterFile3']
    del q.page['converterFile4']
    del q.page['converterFile5']
    del q.page['converterFile6']
    del q.page['converterFile7']
    del q.page['converterFile8'] 
    del q.page['textbox-comentarios'] 
    del q.page['aprovisioning-client']  
    try:
        while 1:
            ticketcomplete = getTicketIIS(r, ticketcomplete['id_ticket'])
            if ticketcomplete['status'] == "Installation Finished":
                q.page['aprovisioning-client'] = ui.form_card(
                    box=ui.box('der1_12', order=1),
                    items=[ui.progress(label='Esperando a que el cliente sea aprovisionado...', caption='Esta pantalla cambiará cuando el proceso se haya completado...')]
                )
            if ticketcomplete['status'] == "Provisioned Client":
                paso1P = 1
                paso2P = 0
                paso3P = 0
                paso4P = 0
                bandPaso1 = 0
            await q.page.save()
            await q.sleep(10)
    except asyncio.CancelledError:
        print("La tarea 'paso3' fue cancelada")
        return

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    global current_paso3_task
    try:
        while 1:
            if paso1P == 1 and bandPaso1 == 0:
                bandPaso1 = 1
                if current_paso3_task and not current_paso3_task.done():
                    current_paso3_task.cancel()
                    try:
                        await current_paso3_task
                    except asyncio.CancelledError:
                        pass
                await q.run(paso1,q)
                await q.page.save()
            if paso2P == 1 and bandPaso2 == 0:
                bandPaso2 = 1
                if current_paso3_task and not current_paso3_task.done():
                    current_paso3_task.cancel()
                    try:
                        await current_paso3_task
                    except asyncio.CancelledError:
                        pass
                await q.run(paso2,q)
                await q.page.save()
            if paso3P == 1 and bandPaso3 == 0:
                bandPaso3 = 1
                await q.run(start_or_restart_paso3,q)
                await q.page.save()
            if paso4P == 1 and bandPaso4 == 0:
                bandPaso4 = 1
                if current_paso3_task and not current_paso3_task.done():
                    current_paso3_task.cancel()
                    try:
                        await current_paso3_task
                    except asyncio.CancelledError:
                        pass
                await q.run(paso4,q)
                await q.page.save()
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global bandPaso1, bandPaso2, bandPaso3, bandPaso4
    bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 0, 0, 0, 0
    # Cancela la tarea anterior si existe y aún está corriendo
    if current_refresh_task and not current_refresh_task.done():
        current_refresh_task.cancel()
        try:
            # Espera a que la tarea sea cancelada (opcional)
            await current_refresh_task
        except asyncio.CancelledError:
            # Maneja el caso en que la tarea fue cancelada
            pass
    # Inicia una nueva tarea
    current_refresh_task = asyncio.create_task(refresh(q))

async def start_or_restart_paso3(q: Q):
    global current_paso3_task
    if current_paso3_task and not current_paso3_task.done():
        current_paso3_task.cancel()
        try:
            await current_paso3_task
        except asyncio.CancelledError:
            pass
    current_paso3_task = asyncio.create_task(paso3(q))

async def iis_workers(q: Q):
    print(str("starting iis_workers..."))
    global ipGlobal, session, data_rows, data_rows_materials, data_rows_materials_keycount, data_rows_materials1, data_rows_materials_send
    global ticketSelectioned, ticketcomplete
    global trabajador, qr_code_iis, noserie, proyecto, marcaDev, modeloDev, descripcion, garantia, motivo, ubicacion, status
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    global id_client, ip_client, password_client, date_picker_cita, horario_cita, installerWorker
    global matsdevsIIS, marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS
    global comboboxMarca, comboboxModelo, comboboxDescripcion
    global res1, res2, res3, res4, res5, res6, res7, res8
    q.page['meta'] = ui.meta_card(box='')

    if q.args.home:
        if session == True:
            q.page['meta'].redirect = 'http://' + ipGlobal + ':10101/'
        else:
            q.page['meta'].redirect = 'http://' + ipGlobal + ':10101/login'
        await q.page.save()

    if q.args.settings:
        if session == True:
            q.page['meta'].redirect = 'http://' + ipGlobal + ':10101/settings'
        else:
            q.page['meta'].redirect = 'http://' + ipGlobal + ':10101/login'
        await q.page.save()

    if q.args.logout:
        session = False
        puesto = ''
        json_datos = json.dumps({"session": session, "puesto": puesto})
        try:
            r.publish("last_session", json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://' + ipGlobal + ':10101/login'
        await q.page.save()

    ###############    A    C   T   I   V   A   T   E       F    U    N    C    T    I    O    N    S    ###############
    if q.args.btnOpenTicket1:
        await q.run(paso2, q, data_rows[0][0])
        await q.page.save()

    if q.args.btnEnTransito:
        updateTicketIIS(r, 'paso5', ticketcomplete['id_ticket'], [])
        q.page['example'] = ui.form_card(
            box=ui.box('der1_12', order=3),
            items=[ui.progress(label='En transito al domicilio del cliente.', caption='Presionar En Proceso cuando haya empezado el trabajo...')]
        )
        del q.page['btnTransitoMaps']
        q.page['btnTransitoMaps'] = ui.section_card(title='', subtitle='',box=ui.box('der1_12', order=4),items=[ui.button(name='btnSeeInMaps', label='Mostrar en Maps', disabled = False, primary=False), ui.button(name='btnEnProceso', label='En Proceso', disabled = False, primary=True)])
        await q.page.save()

    if q.args.btnEnProceso:
        updateTicketIIS(r, 'paso6', ticketcomplete['id_ticket'], [])
        q.page['example'] = ui.form_card(
            box=ui.box('der1_12', order=3),
            items=[ui.progress(label='Working on...', caption='Presionar En Proceso cuando haya empezado el trabajo...')]
        )
        del q.page['btnTransitoMaps']
        q.page['btnTransitoMaps'] = ui.section_card(title='', subtitle='',box=ui.box('der1_12', order=4),items=[ui.button(name='btnSeeInMaps', label='Mostrar en Maps', disabled = False, primary=False), ui.button(name='btnEnProceso', label='En Proceso', disabled = False, primary=True)])
        await q.page.save()

    if q.args.btnSeeInMaps:
        # Construir la URL de Google Maps
        location = str(ticketcomplete['location_client'])
        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={ticketcomplete['location_client']}"
        # Redirigir a la URL de Google Maps
        q.page['meta'].redirect = maps_url
        await q.page.save()

    if q.args.upload_file1:
        import base64
        links = q.args.upload_file1
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res1 = updateTicketIIS(r, 'evidencia1', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile1']
                q.page['converterFile1'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back1', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file2:
        import base64
        links = q.args.upload_file2
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res2 = updateTicketIIS(r, 'evidencia2', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile2']
                q.page['converterFile2'] = ui.form_card(box=ui.box('der1_12', order=2), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back2', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file3:
        import base64
        links = q.args.upload_file3
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res3 = updateTicketIIS(r, 'evidencia3', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile3']
                q.page['converterFile3'] = ui.form_card(box=ui.box('der1_12', order=3), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back3', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file4:
        import base64
        links = q.args.upload_file4
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res4 = updateTicketIIS(r, 'evidencia4', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile4']
                q.page['converterFile4'] = ui.form_card(box=ui.box('der1_12', order=4), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back4', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file5:
        import base64
        links = q.args.upload_file5
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res5 = updateTicketIIS(r, 'evidencia5', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile5']
                q.page['converterFile5'] = ui.form_card(box=ui.box('der1_12', order=5), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back5', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file6:
        import base64
        links = q.args.upload_file6
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res6 = updateTicketIIS(r, 'evidencia6', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile6']
                q.page['converterFile6'] = ui.form_card(box=ui.box('der1_12', order=6), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back6', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file7:
        import base64
        links = q.args.upload_file7
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res7 = updateTicketIIS(r, 'evidencia7', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile7']
                q.page['converterFile7'] = ui.form_card(box=ui.box('der1_12', order=7), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back7', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.upload_file8:
        import base64
        links = q.args.upload_file8
        if links:
            # Verificar si el archivo es una imagen
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = links[0].split('.')[-1].lower()
            if file_extension in valid_extensions:
                try:
                    # Leer datos desde un archivo Excel
                    local_path = await q.site.download(links[0], '../../data')  # Descargar el archivo al directorio actual
                    # Abrir la imagen y convertirla a JPEG
                    with open(local_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    res8 = updateTicketIIS(r, 'evidencia8', ticketcomplete['id_ticket'], encoded_string)
                except Exception as e:
                    print(e)
            else:
                del q.page['converterFile8']
                q.page['converterFile8'] = ui.form_card(box=ui.box('der1_12', order=8), items=[
                    ui.text_xl('El archivo subido no es una imagen válida.'),
                    ui.button(name='back8', label='Back', primary=True)
                ])
        await q.page.save()

    if q.args.back1:
        del q.page['converterFile1']
        q.page['converterFile1'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
            ui.text_xl('Roseta y jumper'),
            ui.file_upload(name='upload_file1', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back2:
        del q.page['converterFile2']
        q.page['converterFile2'] = ui.form_card(box=ui.box('der1_12', order=2), items=[
            ui.text_xl('N° SERIE ONT'),
            ui.file_upload(name='upload_file2', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back3:
        del q.page['converterFile3']
        q.page['converterFile3'] = ui.form_card(box=ui.box('der1_12', order=3), items=[
            ui.text_xl('Terminal Óptica'),
            ui.file_upload(name='upload_file3', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back4:
        del q.page['converterFile4']
        q.page['converterFile4'] = ui.form_card(box=ui.box('der1_12', order=4), items=[
            ui.text_xl('Potencia ONT'),
            ui.file_upload(name='upload_file4', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back5:
        del q.page['converterFile5']
        q.page['converterFile5'] = ui.form_card(box=ui.box('der1_12', order=5), items=[
            ui.text_xl('Test de Velocidad'),
            ui.file_upload(name='upload_file5', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back6:
        del q.page['converterFile6']
        q.page['converterFile6'] = ui.form_card(box=ui.box('der1_12', order=6), items=[
            ui.text_xl('Etiqueta (sinchos)'),
            ui.file_upload(name='upload_file6', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back7:
        del q.page['converterFile7']
        q.page['converterFile7'] = ui.form_card(box=ui.box('der1_12', order=7), items=[
            ui.text_xl('Contrato/Recibo Completado'),
            ui.file_upload(name='upload_file7', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.back8:
        del q.page['converterFile8']
        q.page['converterFile8'] = ui.form_card(box=ui.box('der1_12', order=8), items=[
            ui.text_xl('INE - Comprobante de Domicilio'),
            ui.file_upload(name='upload_file8', label='Subir', multiple=True, compact=False),
        ])
        await q.page.save()

    if q.args.text_descripcion:
        descripcion = str(q.args.text_descripcion)
        await q.page.save()

    if q.args.btnEndInstallation:
        updateTicketIIS(r, 'paso7', ticketcomplete['id_ticket'], [])
        #if res1 == False: #and res2 == False and res3 == False and res4 == False and res5 == False and res6 == False and res7 == False and res8 == False:
        paso1P = 0
        paso2P = 0
        paso3P = 1
        paso4P = 0
        bandPaso3 = 0
        #else:
        #    q.page["meta"].side_panel = ui.side_panel(
        #        title="",
        #        items=[ui.text("Para aprovisionar se deben enviar todas las imagenes que se piden.")],
        #        name="side_panel",
        #        events=["dismissed"],
        #        closable=True,
        #        width='400px',
        #    )
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
        await q.page.save()

    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                zones=[
                    ui.zone('left1_11', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                        ui.zone('header', size='7%'),
                        ui.zone('body', size='93', direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('der1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('der1_12', size='100%', align='stretch', direction=ui.ZoneDirection.COLUMN),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_devices'] = ui.header_card(
            box='header',
            title='C 4 S S I A',
            subtitle='YAA Internet',
            items=[
                ui.menu(
                    image=image,
                    items=[
                        ui.command(name='home', label='Home', icon='Home'),
                        ui.command(name='settings', label='Settings', icon='Settings'),
                        ui.command(name='logout', label='Logout', icon='SignOut'),
                    ]
                )
            ],
        )

        q.page['btnAtras'] = ui.section_card(box=ui.box('izq1_11', order=1), title='', subtitle='', items=[ui.button(name='btnAtras', label='', icon='Back', disabled=False, primary=True)])  
        await q.run(start_or_restart_refresh, q)
        await q.page.save()

@app('/iis_workers', mode='unicast')
async def serve(q: Q):
    route = q.args['#']
    await iis_workers(q)