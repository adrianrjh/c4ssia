from h2o_wave import Q, app, main, ui, AsyncSite, site, data
import threading, json, time, datetime, math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/apps/iis/libs')
from common2_iis import *
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

client = Listener1(r, ['last_session', 'tickets_iis', 'yi_pdfs_iis'])
client.start()

async def paso1(q: Q):
    global data_rows

    del q.page['icon-stepper']
    del q.page['lista-ing-show']
    del q.page['infoStart']
    del q.page['infoticketcreated']
    del q.page['btns1']
    del q.page['paso0']
    del q.page['paso1']
    del q.page['paso2']
    del q.page['paso3']
    del q.page['paso4']
    del q.page['btnAtrasTickets']

    q.page['infoStart'] = ui.section_card(title='', subtitle='', box=ui.box('der1_11', order=1), items=[ui.text_xl('Selecciona un ticket para ver su trazabilidad')])
    
    data_rows = getAllTicketsIIS(r, 'tickets_iis_key', 'tickets_iis')
    q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
        ui.text_xl(content='Lista de Tickets'),
        ui.table(
            name='issues',
            multiple=True,
            columns=columnsIIS,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            ) for dato in data_rows],
            pagination=ui.table_pagination(total_rows=20, rows_per_page=10),
            events=['page_change'],
            groupable=False,
            downloadable=True,
            resettable=False,
        ),
        ui.button(name='btnOpenTicket', label='Abrir Ticket', disabled=False, primary=True)
    ])
    await q.page.save()

async def get_activity_from_ticket(q: Q):
    global ticketSelectioned, ticketcomplete, data_rows_materials, data_rows_materials1, data_rows_materials_send
    global installerWorker, matsdevsIIS, marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS

    del q.page['icon-stepper']
    del q.page['infoStart']
    del q.page['lista-ing-show']
    del q.page['btns1']
    del q.page['paso0']
    del q.page['paso1']
    del q.page['paso2']
    del q.page['paso3']
    del q.page['paso4']
    ticketcomplete = getTicketIIS(r, ticketSelectioned[0][0])
    ################# P    A   S   O       0 #################
    if ticketSelectioned[0][8] == 'Active':
        ################# S     T    E    P    P    E    R #################
        q.page['icon-stepper'] = ui.section_card(
            title='', subtitle='',
            box=ui.box('der1_11', order=1),
            items=[
                ui.stepper(name='icon-stepper', items=[
                    ui.step(label='Info x Asignación', icon='AccountBrowser', done=False),
                    ui.step(label='Confirmar Cita', icon='TaskManagerMirrored', done=False),
                    ui.step(label='Asignar Instalación', icon='Assign', done=False),
                    ui.step(label='Entregar Material', icon='DoubleChevronLeftMedMirrored', done=False),
                    ui.step(label='En Transito', icon='ProgressRingDots', done=False),
                    ui.step(label='En Proceso', icon='ProcessMetaTask', done=False),
                    ui.step(label='Instalación Terminada', icon='InstallToDrive', done=False),
                    ui.step(label='Aprovisionar Cliente', icon='VerticalDistributeCenter', done=False),
                    ui.step(label='Subir Evidencia', icon='BulkUpload', done=False),
                    ui.step(label='Recibir Pago', icon='Money', done=False),
                ])
            ]
        )

        q.page['paso0'] = ui.form_card(
            box=ui.box('der1_12', order=2),
            items=[
                ui.textbox(name='textid_client', label='ID Cliente', trigger=True, value=''),
                ui.textbox(name='textip_client', label='IP Cliente', trigger=True, value=''),
                ui.textbox(name='textpassword_client', label='Password PPoE', trigger=True, value=''),
                ui.button(name='btnSaveRegister1', label='Crear Cita', disabled=False, primary=True)
            ]
        )

        ################# I    N   F   O        T   I   C   K   E   T #################
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
                ui.textbox(name='register_paqueteplan', label='Paquete Plan', disabled=True, value=str(ticketcomplete['paqueteplan'])),
                ui.textbox(name='register_anchobanda', label='Ancho de Banda', disabled=True, value=str(ticketcomplete['anchoBanda'])),
                ui.textbox(name='register_precioinstalacion', label='Precio de Instalación', disabled=True, value='$'+str(ticketcomplete['precio_client'])),
                ui.textbox(name='register_preciomensual', label='Precio Mensual', disabled=True, value=str(ticketcomplete['precioMensual'])),
                ui.textbox(name='register_formatopago', label='Formato de pago', disabled=True, value=str(ticketcomplete['formatoPago'])),
                ui.textbox(name='register_factura', label='Factura', disabled=True, value=str(ticketcomplete['factura'])),
                ui.textbox(name='register_creacionticket', label='Fecha de creación de ticket', disabled=True, value=str(ticketcomplete['date_ticket'])),
                ui.textbox(name='register_supporter1', label='Creador del ticket', disabled=True, value=str(ticketcomplete['username'])),
                ui.textbox(name='register_status', label='Status', disabled=True, value=str(ticketcomplete['status'])),
                ui.textbox(name='register_datestatus', label='Date Status', disabled=True, value=str(ticketcomplete['date_status'])),
            ]
        )

    ################# P    A   S   O       2 #################
    if ticketSelectioned[0][8] == 'InfoXAsig':
        ################# S     T    E    P    P    E    R #################
        q.page['icon-stepper'] = ui.section_card(
            title='', subtitle='',
            box=ui.box('der1_11', order=1),
            items=[
                ui.stepper(name='icon-stepper', items=[
                    ui.step(label='Info x Asignación', icon='AccountBrowser', done=True),
                    ui.step(label='Confirmar Cita', icon='TaskManagerMirrored', done=False),
                    ui.step(label='Asignar Instalación', icon='Assign', done=False),
                    ui.step(label='Entregar Material', icon='DoubleChevronLeftMedMirrored', done=False),
                    ui.step(label='En Transito', icon='ProgressRingDots', done=False),
                    ui.step(label='En Proceso', icon='ProcessMetaTask', done=False),
                    ui.step(label='Instalación Terminada', icon='InstallToDrive', done=False),
                    ui.step(label='Aprovisionar Cliente', icon='VerticalDistributeCenter', done=False),
                    ui.step(label='Subir Evidencia', icon='BulkUpload', done=False),
                    ui.step(label='Recibir Pago', icon='Money', done=False),
                ])
            ]
        )

        q.page['paso1'] = ui.form_card(
            box=ui.box('der1_12', order=2),
            items=[
                ui.date_picker(name='date_picker_cita', label='Dia Propuesto', trigger=True, value=datetime.datetime.now().strftime("%Y-%m-%d")),
                ui.combobox(name='comboboxHorario_cita', label='Horario', value='Seleccionar', choices=comboboxHorarios, trigger=True),
                ui.button(name='btnConfirmCita', label='Confirmar Cita', disabled=False, primary=True)
            ]
        )

        ################# I    N   F   O        T   I   C   K   E   T #################
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
                ui.textbox(name='register_paqueteplan', label='Paquete Plan', disabled=True, value=str(ticketcomplete['paqueteplan'])),
                ui.textbox(name='register_anchobanda', label='Ancho de Banda', disabled=True, value=str(ticketcomplete['anchoBanda'])),
                ui.textbox(name='register_precioinstalacion', label='Precio de Instalación', disabled=True, value='$'+str(ticketcomplete['precio_client'])),
                ui.textbox(name='register_preciomensual', label='Precio Mensual', disabled=True, value=str(ticketcomplete['precioMensual'])),
                ui.textbox(name='register_formatopago', label='Formato de pago', disabled=True, value=str(ticketcomplete['formatoPago'])),
                ui.textbox(name='register_factura', label='Factura', disabled=True, value=str(ticketcomplete['factura'])),
                ui.textbox(name='register_creacionticket', label='Fecha de creación de ticket', disabled=True, value=str(ticketcomplete['date_ticket'])),
                ui.textbox(name='register_supporter1', label='Creador del ticket', disabled=True, value=str(ticketcomplete['username'])),
                ui.textbox(name='register_status', label='Status', disabled=True, value=str(ticketcomplete['status'])),
                ui.textbox(name='register_datestatus', label='Date Status', disabled=True, value=str(ticketcomplete['date_status'])),
                ui.textbox(name='textid_client', label='ID Cliente', disabled=True, value=str(ticketcomplete['id_client'])),
                ui.textbox(name='textip_client', label='IP Cliente', disabled=True, value=str(ticketcomplete['ip_client'])),
                ui.textbox(name='textpassword_client', label='Password PPoE', disabled=True, value=str(ticketcomplete['password_client'])),
            ]
        )

    ################# P    A   S   O       3 #################
    if str(ticketSelectioned[0][8]) == 'Date Created':
        ################# S     T    E    P    P    E    R #################
        q.page['icon-stepper'] = ui.section_card(
            title='', subtitle='',
            box=ui.box('der1_11', order=1),
            items=[
                ui.stepper(name='icon-stepper', items=[
                    ui.step(label='Info x Asignación', icon='AccountBrowser', done=True),
                    ui.step(label='Confirmar Cita', icon='TaskManagerMirrored', done=True),
                    ui.step(label='Asignar Instalación', icon='Assign', done=False),
                    ui.step(label='Entregar Material', icon='DoubleChevronLeftMedMirrored', done=False),
                    ui.step(label='En Transito', icon='ProgressRingDots', done=False),
                    ui.step(label='En Proceso', icon='ProcessMetaTask', done=False),
                    ui.step(label='Instalación Terminada', icon='InstallToDrive', done=False),
                    ui.step(label='Aprovisionar Cliente', icon='VerticalDistributeCenter', done=False),
                    ui.step(label='Subir Evidencia', icon='BulkUpload', done=False),
                    ui.step(label='Recibir Pago', icon='Money', done=False),
                ])
            ]
        )
        comboboxUsers = []
        users = getAllUsers(r, 'user_key', 'user_')
        for x in range(0,len(users)):
            comboboxUsers.append(users[x][2]+' '+users[x][3]+'/'+users[x][7])

        q.page['paso3'] = ui.form_card(
            box=ui.box('der1_12', order=2),
            items=[
                ui.combobox(name='comboboxInstaller', label='Instalador', value=str(installerWorker), choices=comboboxUsers, trigger=True),
                ui.combobox(name='comboboxmatdevs', label='Tipo de material', value=str(matsdevsIIS), choices=comboboxMatDevs,trigger=True),
                ui.combobox(name='combomarca', label='Marca', value=str(marcaIIS), choices=comboboxMarca,trigger=True, disabled=False),
                ui.combobox(name='combomodelo', label='Modelo', value=str(modeloIIS), choices=comboboxModelo,trigger=True, disabled=False),
                ui.combobox(name='combodescripcion', label='Descripción', value=str(descripcionIIS), choices=comboboxDescripcion,trigger=True, disabled=False),
                ui.textbox(name='textunidad', label='Unidad', value=str(unidadIIS), trigger=True, disabled=True),
                ui.spinbox(name='textcantidad', label='Cantidad', value=int(cantidadIIS), trigger=False, disabled=False),
                ui.button(name='btnAgregarAsig', label='Agregar', disabled = False, primary=True),
                ui.separator(''),
                ui.text_xl(content='Lista de equipos/material para instalación de nuevo cliente'),
                ui.table(
                    name='issues',
                    multiple=True,
                    columns=columnsAsigIIS1,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    ) for dato in data_rows_materials1],
                    pagination=ui.table_pagination(total_rows=20, rows_per_page=10),
                    events=['page_change'],
                    groupable=False,
                    downloadable=True,
                    resettable=False,
                ),
                ui.button(name='btnDeleteArticle', label='Eliminar', disabled=False, primary=True),
                ui.button(name='btnAsignArts', label='Asignar', disabled=False, primary=True)
            ]
        )

        ################# I    N   F   O        T   I   C   K   E   T #################
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
                ui.textbox(name='register_paqueteplan', label='Paquete Plan', disabled=True, value=str(ticketcomplete['paqueteplan'])),
                ui.textbox(name='register_anchobanda', label='Ancho de Banda', disabled=True, value=str(ticketcomplete['anchoBanda'])),
                ui.textbox(name='register_precioinstalacion', label='Precio de Instalación', disabled=True, value='$'+str(ticketcomplete['precio_client'])),
                ui.textbox(name='register_preciomensual', label='Precio Mensual', disabled=True, value=str(ticketcomplete['precioMensual'])),
                ui.textbox(name='register_formatopago', label='Formato de pago', disabled=True, value=str(ticketcomplete['formatoPago'])),
                ui.textbox(name='register_factura', label='Factura', disabled=True, value=str(ticketcomplete['factura'])),
                ui.textbox(name='register_creacionticket', label='Fecha de creación de ticket', disabled=True, value=str(ticketcomplete['date_ticket'])),
                ui.textbox(name='register_supporter1', label='Creador del ticket', disabled=True, value=str(ticketcomplete['username'])),
                ui.textbox(name='register_status', label='Status', disabled=True, value=str(ticketcomplete['status'])),
                ui.textbox(name='register_datestatus', label='Date Status', disabled=True, value=str(ticketcomplete['date_status'])),
                ui.textbox(name='textid_client', label='ID Cliente', disabled=True, value=str(ticketcomplete['id_client'])),
                ui.textbox(name='textip_client', label='IP Cliente', disabled=True, value=str(ticketcomplete['ip_client'])),
                ui.textbox(name='textpassword_client', label='Password PPoE', disabled=True, value=str(ticketcomplete['password_client'])),
                ui.textbox(name='textcita_instalacion', label='Cita de Instalación', disabled=True, value=str(ticketcomplete['cita_instalacion'])),
            ]
        )

    ################# P    A   S   O       4 #################
    if ticketSelectioned[0][8] == 'Ticket Asigned':
        ################# S     T    E    P    P    E    R #################
        q.page['icon-stepper'] = ui.section_card(
            title='', subtitle='',
            box=ui.box('der1_11', order=1),
            items=[
                ui.stepper(name='icon-stepper', items=[
                    ui.step(label='Info x Asignación', icon='AccountBrowser', done=True),
                    ui.step(label='Confirmar Cita', icon='TaskManagerMirrored', done=True),
                    ui.step(label='Asignar Instalación', icon='Assign', done=True),
                    ui.step(label='Entregar Material', icon='DoubleChevronLeftMedMirrored', done=False),
                    ui.step(label='En Transito', icon='ProgressRingDots', done=False),
                    ui.step(label='En Proceso', icon='ProcessMetaTask', done=False),
                    ui.step(label='Instalación Terminada', icon='InstallToDrive', done=False),
                    ui.step(label='Aprovisionar Cliente', icon='VerticalDistributeCenter', done=False),
                    ui.step(label='Subir Evidencia', icon='BulkUpload', done=False),
                    ui.step(label='Recibir Pago', icon='Money', done=False),
                ])
            ]
        )

        data_rows_materials1 = json.loads(ticketcomplete['materiales_instalador'].replace("'","["))
        q.page['paso4'] = ui.form_card(
            box=ui.box('der1_12', order=2),
            items=[
                ui.textbox(name='textqrcode', label='QR CODE',trigger=True),
                ui.button(name='btnAgregarQRCode', label='Agregar', disabled = False, primary=True),
                ui.separator(''),
                ui.text_xl(content='Lista de equipos/material para instalación de nuevo cliente'),
                ui.table(
                    name='issues',
                    multiple=False,
                    columns=columnsAsigIIS1,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    ) for dato in data_rows_materials1],
                    groupable=False,
                    downloadable=True,
                    resettable=False,
                ),
                ui.separator(''),
                ui.text_xl(content='Listo para entregar'),
                ui.table(
                    name='issues1',
                    multiple=True,
                    columns=columnsAsig,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    ) for dato in data_rows_materials_send],
                    groupable=False,
                    downloadable=True,
                    resettable=False,
                ),
                ui.button(name='btnFinAsig', label='Finalizar Asignación', disabled = False, primary=True)
            ],
        )
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
                ui.textbox(name='register_paqueteplan', label='Paquete Plan', disabled=True, value=str(ticketcomplete['paqueteplan'])),
                ui.textbox(name='register_anchobanda', label='Ancho de Banda', disabled=True, value=str(ticketcomplete['anchoBanda'])),
                ui.textbox(name='register_precioinstalacion', label='Precio de Instalación', disabled=True, value='$'+str(ticketcomplete['precio_client'])),
                ui.textbox(name='register_preciomensual', label='Precio Mensual', disabled=True, value='$'+str(ticketcomplete['precioMensual'])),
                ui.textbox(name='register_formatopago', label='Formato de pago', disabled=True, value=str(ticketcomplete['formatoPago'])),
                ui.textbox(name='register_factura', label='Factura', disabled=True, value=str(ticketcomplete['factura'])),
                ui.textbox(name='register_creacionticket', label='Fecha de creación de ticket', disabled=True, value=str(ticketcomplete['date_ticket'])),
                ui.textbox(name='register_supporter1', label='Creador del ticket', disabled=True, value=str(ticketcomplete['username'])),
                ui.textbox(name='register_status', label='Status', disabled=True, value=str(ticketcomplete['status'])),
                ui.textbox(name='register_datestatus', label='Date Status', disabled=True, value=str(ticketcomplete['date_status'])),
                ui.textbox(name='textid_client', label='ID Cliente', disabled=True, value=str(ticketcomplete['id_client'])),
                ui.textbox(name='textip_client', label='IP Cliente', disabled=True, value=str(ticketcomplete['ip_client'])),
                ui.textbox(name='textpassword_client', label='Password PPoE', disabled=True, value=str(ticketcomplete['password_client'])),
                ui.textbox(name='textcita_instalacion', label='Cita de Instalación', disabled=True, value=str(ticketcomplete['cita_instalacion'])),
                ui.textbox(name='textinstalador', label='Instalador', disabled=True, value=str(instalador[0])),
            ]
        )

    ################# P    A   S   O       5 #################
    if ticketSelectioned[0][8] == 'Asigned Material':
        ################# S     T    E    P    P    E    R #################
        q.page['icon-stepper'] = ui.section_card(
            title='', subtitle='',
            box=ui.box('der1_11', order=1),
            items=[
                ui.stepper(name='icon-stepper', items=[
                    ui.step(label='Info x Asignación', icon='AccountBrowser', done=True),
                    ui.step(label='Confirmar Cita', icon='TaskManagerMirrored', done=True),
                    ui.step(label='Asignar Instalación', icon='Assign', done=True),
                    ui.step(label='Entregar Material', icon='DoubleChevronLeftMedMirrored', done=True),
                    ui.step(label='En Transito', icon='ProgressRingDots', done=False),
                    ui.step(label='En Proceso', icon='ProcessMetaTask', done=False),
                    ui.step(label='Instalación Terminada', icon='InstallToDrive', done=False),
                    ui.step(label='Aprovisionar Cliente', icon='VerticalDistributeCenter', done=False),
                    ui.step(label='Subir Evidencia', icon='BulkUpload', done=False),
                    ui.step(label='Recibir Pago', icon='Money', done=False),
                ])
            ]
        )

        data_rows_materials1 = json.loads(ticketcomplete['materiales_instalador'].replace("'","["))
        q.page['paso4'] = ui.form_card(
            box=ui.box('der1_12', order=2),
            items=[
                ui.textbox(name='textqrcode', label='QR CODE',trigger=True),
                ui.button(name='btnAgregarQRCode', label='Agregar', disabled = False, primary=True),
                ui.separator(''),
                ui.text_xl(content='Lista de equipos/material para instalación de nuevo cliente'),
                ui.table(
                    name='issues',
                    multiple=False,
                    columns=columnsAsigIIS1,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    ) for dato in data_rows_materials1],
                    groupable=False,
                    downloadable=True,
                    resettable=False,
                ),
                ui.separator(''),
                ui.text_xl(content='Listo para entregar'),
                ui.table(
                    name='issues1',
                    multiple=True,
                    columns=columnsAsig,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    ) for dato in data_rows_materials_send],
                    groupable=False,
                    downloadable=True,
                    resettable=False,
                ),
                ui.button(name='btnFinAsig', label='Finalizar Asignación', disabled = False, primary=True)
            ],
        )
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
                ui.textbox(name='register_paqueteplan', label='Paquete Plan', disabled=True, value=str(ticketcomplete['paqueteplan'])),
                ui.textbox(name='register_anchobanda', label='Ancho de Banda', disabled=True, value=str(ticketcomplete['anchoBanda'])),
                ui.textbox(name='register_precioinstalacion', label='Precio de Instalación', disabled=True, value='$'+str(ticketcomplete['precio_client'])),
                ui.textbox(name='register_preciomensual', label='Precio Mensual', disabled=True, value=str(ticketcomplete['precioMensual'])),
                ui.textbox(name='register_formatopago', label='Formato de pago', disabled=True, value=str(ticketcomplete['formatoPago'])),
                ui.textbox(name='register_factura', label='Factura', disabled=True, value=str(ticketcomplete['factura'])),
                ui.textbox(name='register_creacionticket', label='Fecha de creación de ticket', disabled=True, value=str(ticketcomplete['date_ticket'])),
                ui.textbox(name='register_supporter1', label='Creador del ticket', disabled=True, value=str(ticketcomplete['username'])),
                ui.textbox(name='register_status', label='Status', disabled=True, value=str(ticketcomplete['status'])),
                ui.textbox(name='register_datestatus', label='Date Status', disabled=True, value=str(ticketcomplete['date_status'])),
                ui.textbox(name='textid_client', label='ID Cliente', disabled=True, value=str(ticketcomplete['id_client'])),
                ui.textbox(name='textip_client', label='IP Cliente', disabled=True, value=str(ticketcomplete['ip_client'])),
                ui.textbox(name='textpassword_client', label='Password PPoE', disabled=True, value=str(ticketcomplete['password_client'])),
                ui.textbox(name='textcita_instalacion', label='Cita de Instalación', disabled=True, value=str(ticketcomplete['cita_instalacion'])),
                ui.textbox(name='textinstalador', label='Instalador', disabled=True, value=str(instalador[0])),
                ui.textbox(name='textinstaller_client', label='Materiales Asignados', disabled=True, value=str(ticketcomplete['materiales_instalador_asignado'])),
            ]
        )
    q.page['btnAtrasTickets'] = ui.section_card(box=ui.box('izq1_12', order=1), title='', subtitle='', items=[ui.button(name='btnAtrasTickets', label='', icon='Ticket', disabled=False, primary=True)])  
    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4

    try:
        while 1:
            if paso1P == 1 and bandPaso1 == 0:
                bandPaso1 = 1
                await q.run(paso1,q)
                await q.page.save()
            if paso2P == 1 and bandPaso2 == 0:
                bandPaso2 = 1
                await q.run(get_activity_from_ticket,q)
                await q.page.save()
            if paso3P == 1 and bandPaso3 == 0:
                bandPaso3 = 1
                await q.run(paso3,q)
                await q.page.save()
            if paso4P == 1 and bandPaso4 == 0:
                bandPaso4 = 1
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

async def iis_dashboard(q: Q):
    print(str("starting iis_dashboard..."))
    global ipGlobal, session, data_rows, data_rows_materials, data_rows_materials_keycount, data_rows_materials1, data_rows_materials_send
    global ticketSelectioned, ticketcomplete
    global trabajador, qr_code_iis, noserie, proyecto, marcaDev, modeloDev, descripcion, garantia, motivo, ubicacion, status
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    global id_client, ip_client, password_client, date_picker_cita, horario_cita, installerWorker
    global matsdevsIIS, marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS
    global comboboxMarca, comboboxModelo, comboboxDescripcion

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

    if q.args.btnAtras:
        q.page['meta'].redirect = 'http://' + ipGlobal + ':10101/home_iis'
        await q.page.save()

    if q.args.btnAtrasTickets:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        await q.page.save()

    ###############    C  O   L   L   E   C   T   O   R       V   A   R   I   A   B   L   E   S   ###############
    if q.args.textid_client:
        id_client = str(q.args.textid_client)
        await q.page.save()

    if q.args.textip_client:
        ip_client = str(q.args.textip_client)
        await q.page.save()

    if q.args.textpassword_client:
        password_client = str(q.args.textpassword_client)
        await q.page.save()

    if q.args.date_picker_cita:
        date_picker_cita = str(q.args.date_picker_cita)
        await q.page.save()

    if q.args.comboboxHorario_cita:
        horario_cita = str(q.args.comboboxHorario_cita)
        await q.page.save()

    if q.args.textqrcode:
        qr_code_iis = str(q.args.textqrcode)
        await q.page.save()

    if q.args.comboboxInstaller and installerWorker!=str(q.args.comboboxInstaller):
        installerWorker = str(q.args.comboboxInstaller)
        await q.page.save()

    if q.args.comboboxmatdevs and str(q.args.comboboxmatdevs) != 'Seleccionar':
        if matsdevsIIS != str(q.args.comboboxmatdevs):
            matsdevsIIS = str(q.args.comboboxmatdevs)
            res = getAllMatsDevs(r, matsdevsIIS)
            comboboxMarca = list(set([str(x[0]) for x in res]))  # Obtener marcas únicas
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.combomarca and str(q.args.combomarca) != 'Seleccionar':
        if marcaIIS!=str(q.args.combomarca):
            marcaIIS = str(q.args.combomarca)
            if matsdevsIIS == 'Materiales de construccion':
                res = getAllMatsMarca(r, marcaIIS)
            if matsdevsIIS == 'Equipos de Red':
                res = getAllDevsMarca(r, marcaIIS)
            modeloBefore = ''
            comboboxModelo = []
            for x in range(0, len(res)):
                if modeloBefore != str(res[x][1]):
                    modeloBefore = res[x][1]
                    comboboxModelo.append(res[x][1])
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.combomodelo and str(q.args.combomodelo) != 'Seleccionar':
        if modeloIIS!=str(q.args.combomodelo):
            modeloIIS = str(q.args.combomodelo)
            if matsdevsIIS == 'Materiales de construccion':
                res = getAllMatsModelo(r, modeloIIS)
            if matsdevsIIS == 'Equipos de Red':
                res = getAllDevsModelo(r, modeloIIS)
            descripcionBefore = ''
            comboboxDescripcion = []
            for x in range(0, len(res)):
                if descripcionBefore != str(res[x][2]):
                    descripcionBefore = res[x][2]
                    comboboxDescripcion.append(res[x][2])
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.combodescripcion and str(q.args.combodescripcion) != 'Seleccionar':
        if descripcionIIS!=str(q.args.combodescripcion):
            descripcionIIS = str(q.args.combodescripcion)
            if matsdevsIIS == 'Materiales de construccion':
                res = getAllMatsDescripcion(r, descripcionIIS)
            if matsdevsIIS == 'Equipos de Red':
                res = getAllDevsDescripcion(r, descripcionIIS)
            unidadIIS = res
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.textcantidad:
        cantidadIIS=str(q.args.textcantidad)
        await q.page.save()

    ###############    A    C   T   I   V   A   T   E       F    U    N    C    T    I    O    N    S    ###############
    if q.args.btnOpenTicket:
        ticketSelectioned = []
        selectioned = q.args.issues
        if selectioned is None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un ticket para ver su trazabilidad.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width='400px',
            )
        if selectioned is not None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0]) == str(x):
                            found = 1
                            data_rows_send.append(y)
                    if found == 0:
                        data_rows_temp.append(y)
                    found = 0
                ticketSelectioned = data_rows_send
                await q.run(get_activity_from_ticket, q)
        await q.page.save()

    if q.args.btnSaveRegister1:
        data = [id_client, ip_client, password_client]
        updateTicketIIS(r, 'paso1', ticketSelectioned[0][0], data)
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnConfirmCita:
        data = [date_picker_cita, horario_cita]
        updateTicketIIS(r, 'paso2', ticketSelectioned[0][0], data)
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnAgregarAsig:
        data_rows_materials1.append([marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS])
        matsdevsIIS, marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS = '', '', '', '', '', 0.0
        paso1P = 0
        paso2P = 1
        paso3P = 0
        bandPaso2 = 0
        await q.page.save()

    if q.args.btnDeleteArticle:
        eliminados = q.args.issues
        if eliminados == None:
            pass
        if eliminados != None:
            data_rows_temp, data_rows_send, found = [], [], 0
            for y in data_rows_materials1:
                for x in eliminados:
                    if str(y[0])==str(x):
                        found=1
                        # si quieres quitar los que seleccionaste
                        data_rows_send.append(y)
                if found==0:
                    # si quieres quitar los que no seleccionaste
                    data_rows_temp.append(y)
                found = 0
        data_rows_materials1 = data_rows_temp
        paso1P = 0
        paso2P = 1
        paso3P = 0
        bandPaso2 = 0
        await q.page.save()

    if q.args.btnAsignArts:
        selectioned = q.args.issues
        if selectioned == None:
            pass
        if selectioned != None:
            if len(selectioned) == len(data_rows_materials1):
                data = [installerWorker, data_rows_materials1]
                updateTicketIIS(r, 'paso3', ticketSelectioned[0][0], data)
                data_rows_materials1 = []
                paso1P = 1
                paso2P = 0
                paso3P = 0
                bandPaso1 = 0
        await q.page.save()

    if q.args.btnAgregarQRCode:
        data_rows_temp, data_rows_send, found = [], [], 0
        qr_code_iis = qr_code_iis.replace("-", "/")
        qr_code_iis = qr_code_iis.replace("'", "-")
        res = getSingleArticle(r, qr_code_iis)
        if res != 'NO':
            try:
                if res != None:
                    noserie = res['noserie']
                    proyecto = res['proyecto']
                    marcaDev = res['marca']
                    modeloDev = res['modelo']
                    descripcion = res['descripcion']
                    ubicacion = res['ubicacion']
                    status = res['status']
                    data_rows_materials_keycount += 1
                    data_rows_materials_send.append([str(data_rows_materials_keycount), noserie, proyecto, marcaDev, modeloDev, descripcion, ubicacion, status])
                    paso1P = 0
                    paso2P = 1
                    paso3P = 0
                    bandPaso2 = 0
                else:
                    qr_code = ''
            except Exception as e:
                print(e)
        else:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Dispositivo no encontrado en el inventario nuevo y usado.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width='400px',
            )
        await q.page.save()

    if q.args.btnFinAsig:
        selectioned = q.args.issues1
        if selectioned == None:
            pass
        if selectioned != None:
            if len(selectioned) == len(data_rows_materials_send):
                data_user = getUser('user_key', 'user_', 'robert')
                json_datos={
                    'usuarioA':str(data_user[0]),
                    'puestoA':str(data_user[1]),
                    'lista':data_rows_materials_send,
                    'ticketcompleto':ticketcomplete
                }
                if ticketcomplete['paqueteplan'] == "Comprado":
                    try:
                        r.publish("yi_pdfs_iis_comprado",json.dumps(json_datos))
                        time.sleep(0.3)
                    except Exception as e:
                        print(e)
                    changeStateArticle(data_rows_materials_send, data_user[0], 'asignar')
                    data = [data_rows_materials_send]
                    updateTicketIIS(r, 'paso4', ticketSelectioned[0][0], data)
                    data_rows_materials_send = []
                if ticketcomplete['paqueteplan'] == "Comodato":
                    try:
                        r.publish("yi_pdfs_iis_comodato",json.dumps(json_datos))
                        time.sleep(0.3)
                    except Exception as e:
                        print(e)
                    changeStateArticle(data_rows_materials_send, data_user[0], 'asignar')
                    data = [data_rows_materials_send]
                    updateTicketIIS(r, 'paso4', ticketSelectioned[0][0], data)
                    data_rows_materials_send = []
                paso1P = 1
                paso2P = 0
                paso3P = 0
                bandPaso1 = 0
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
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
                            ui.zone('izq1_1', size='5%', direction=ui.ZoneDirection.COLUMN, align='start', zones=[
                                ui.zone('izq1_11', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_12', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_13', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_14', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_15', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ]),
                            ui.zone('der1_1', size='95%', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('der1_11', size='8%', align='center', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('der1_12', size='92%', align='stretch', direction=ui.ZoneDirection.ROW),
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

@app('/iis_dashboard', mode='unicast')
async def serve(q: Q):
    route = q.args['#']
    await iis_dashboard(q)