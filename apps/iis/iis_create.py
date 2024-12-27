from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,math
import os
from datetime import datetime
from dateutil import parser
import re
import sys
import json
import random
import calendar
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/apps/iis/libs')
from common1_iis import *
import csv
from typing import Tuple, Optional

session_dir = os.path.expanduser('/home/adrian/ws/wave/cassia/apps/iis/assets')
session_file = os.path.join(session_dir, 'session_data.json')

os.makedirs(session_dir, exist_ok=True)

def load_session():
    try:
        with open(session_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_session(data):
    with open(session_file, 'w') as f:
        json.dump(data, f)

class Listener1(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis,self.init = r,0
        self.pubsub = self.redis.pubsub()
        print('Listener1...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)

    def work(self, item):
        global session, puesto, username
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            session = data['session']
            puesto = data['puesto']
            username = data['username']
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
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
                        self.pubsub.subscribe(['last_session'])
                        break
            time.sleep(0.001)  # be nice to the system :)

#client = Listener1(r, ['last_session'])
#client.start()

def extract_lat_long_from_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract latitude and longitude from a Google Maps URL.

    :param url: Google Maps URL as a string.
    :return: A tuple containing latitude and longitude as strings, or (None, None) if not found.
    """
    regex = r"@([0-9.-]+),([0-9.-]+)"
    match = re.search(regex, url)
    if match:
        latitude, longitude = match.groups()
        return latitude, longitude
    else:
        return None, None
    
async def formu_ticket(q: Q):
    global comboboxHorarios, comboboxPaquetePlan, comboboxAnchoBanda
    global name_client, lastname_client, phone_client, address_client, refaddress_client, location_client, datepicker_client, colonia_client
    global localidad_client, municipio_client, estado_client, precio_client, paqueteprecio, anchoprecio, email_client, formatoPago, precioMensual
    global today, today_day, ultimo_dia, year, month, ndays, ultimo_paquete, ultimo_banda, ultima_location, tiposervicio, paqueteplan, anchoBanda
    global identificacion, comprobante, factura

    session_data = load_session()

    # Cargar los datos de la sesión
    name_client = session_data.get('name_client', '')
    lastname_client = session_data.get('lastname_client', '')
    phone_client = session_data.get('phone_client', '')
    email_client = session_data.get('email_client', '')
    address_client = session_data.get('address_client', '')
    refaddress_client = session_data.get('refaddress_client', '')
    location_client = session_data.get('location_client', '')
    colonia_client = session_data.get('colonia_client', '')
    localidad_client = session_data.get('localidad_client', '')
    municipio_client = session_data.get('municipio_client', '')
    estado_client = session_data.get('estado_client', '')
    tiposervicio = session_data.get('tiposervicio', 'Seleccionar')
    paqueteplan = session_data.get('paqueteplan', 'Seleccionar')
    formatoPago = session_data.get('formatoPago', 'Seleccionar')
    anchoBanda = session_data.get('anchoBanda', 'Seleccionar')

    identificacion = session_data.get('identificacion', False)
    comprobante = session_data.get('comprobante', False)
    factura = session_data.get('factura', False)

    precio_client = 0

    precioMensual = 0

    paqueteprecio = 0

    anchoprecio = 0

    today = datetime.datetime.now()

    today += datetime.timedelta(days=3) # Saltar 3 días

    # Comprobar si el día de hoy es domingo (6 en Python, donde 0 es lunes)
    if today.weekday() == 6:  # 6 es domingo
        today += datetime.timedelta(days=1)  # Saltar al lunes

    # Comprobar si el día de hoy es sabado (5 en Python, donde 0 es lunes)
    if today.weekday() == 5:  # 5 es sabado
        comboboxHorarios = ['9am-11am', '11am-13pm']
    
    today_day = today.day
 
    year = today.year

    month = today.month

    ultimo_dia = calendar.monthrange(year, month)[1]

    ultimo_paquete = 'Seleccionar'

    ultimo_banda = 'Seleccionar'

    ultima_location = ''

    precio_client = 0

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']

    # Renderizar el formulario 
    await update_(q)
    await update_price_textbox(q)
    await q.page.save()
    
async def update_price_textbox(q: Q):
    global comboboxHorarios, comboboxPaquetePlan, comboboxAnchoBanda
    global name_client, lastname_client, phone_client, address_client, refaddress_client, location_client, colonia_client, datepicker_client
    global localidad_client, municipio_client, estado_client, precio_client, paqueteprecio, anchoprecio, formatoPago
    global tiposervicio, paqueteplan, anchoBanda, factura
    global today, today_day, ultimo_dia, ndays, month

    if today_day < 26:
        ndays = ultimo_dia - today_day 
        abpxDay = anchoprecio / ultimo_dia
        precio_client = ndays * abpxDay
        precio_client += paqueteprecio
        precio_client = round(precio_client)
    else:
        # Calcular el precio total
        precio_client = paqueteprecio + anchoprecio

    precioMensual = anchoprecio

    # Renderizar el formulario con los valores actuales
    q.page['combotextboxes1'] = ui.form_card(
        box=ui.box('der1_12', order=1),
        items=[
            ui.textbox(name='textrefaddress_client', label='Referencia', trigger=True, value=str(refaddress_client)),
            ui.textbox(name='textlocaddress_client', label='Ubicación', trigger=True, value=str(location_client)),
            ui.date_picker(name='date_picker', label='Dia Propuesto', trigger=True, value=str(today), disabled=True),
            ui.combobox(name='comboboxHorario', label='Horario', value=str(tiposervicio), choices=comboboxHorarios, trigger=True),
            ui.combobox(name='comboboxPaqueteEquipo', label='Paquete Plan', value=str(paqueteplan), choices=comboboxPaquetePlan, trigger=True),
            ui.combobox(name='comboboxPaqueteMB', label='Ancho de Banda Plan', value=str(anchoBanda), choices=comboboxAnchoBanda, trigger=True),
            ui.combobox(name='comboboxFormaPago', label='Formato de Pago', value=str(formatoPago), choices=comboboxFormaPago, trigger=True),
            ui.checkbox(name='checkFactura', label='Factura', value=factura, trigger=True),
            ui.textbox(name='textcost_client', label='Costo de Instalación', trigger=True, value=str(precio_client), disabled=True),
            ui.textbox(name='textprecioMensual', label='Costo Mensual', trigger=True, value=str(precioMensual), disabled=True),
            ui.button(name='btnAdd', label='Add Ticket', disabled=False, primary=True)
        ]
    )

    await q.page.save()

async def update_(q: Q):
    global comboboxHorarios, comboboxPaquetePlan, comboboxAnchoBanda
    global name_client, lastname_client, phone_client, address_client, refaddress_client, location_client, colonia_client, datepicker_client
    global localidad_client, municipio_client, estado_client, precio_client, paqueteprecio, anchoprecio, email_client
    global tiposervicio, paqueteplan, anchoBanda
    global today, today_day, ultimo_dia, ndays, month
    global identificacion, comprobante

    # Renderizar el formulario con los valores actuales
    q.page['combotextboxes0'] = ui.form_card(
        box=ui.box('der1_11', order=1),
        items=[
            ui.textbox(name='textname_client', label='Nombre completo', trigger=True, value=str(name_client)),
            ui.textbox(name='textlastname_client', label='Apellidos', trigger=True, value=str(lastname_client)),
            ui.textbox(name='textphone_client', label='Telefono', trigger=True, value=str(phone_client)),
            ui.textbox(name='textemail_client', label='Email', trigger=True, value=str(email_client)),
            ui.textbox(name='textaddress_client', label='Domicilio', trigger=True, value=str(address_client)),
            ui.textbox(name='textcolonia_client', label='Colonia', trigger=True, value=str(colonia_client)),
            ui.textbox(name='textlocalidad_client', label='Localidad', trigger=True, value=str(localidad_client)),
            ui.textbox(name='textmunicipio_client', label='Municipio', trigger=True, value=str(municipio_client)),
            ui.textbox(name='textestado_client', label='Estado', trigger=True, value=str(estado_client)),
            ui.checkbox(name='checkidentificacion_client', label='Identificacion oficial', value=identificacion, trigger=True),
            ui.checkbox(name='checkcomprobante_client', label='Comprobante de domicilio', value=comprobante, trigger=True)
        ]
    )

    await q.page.save()
    
async def iis_create(q: Q):
    print(str("starting iis_create..."))
    global ipGlobal,session,username
    global comboboxTS, comboboxTP
    global name_client, lastname_client, datepicker_client, tiposervicio, paqueteplan, anchoBanda, formatoPago
    global comboboxHorarios, comboboxPaquetePlan, comboboxAnchoBanda
    global phone_client, address_client, refaddress_client, location_client, localidad_client, colonia_client, municipio_client, estado_client, precio_client, paqueteprecio, anchoprecio
    global today, today_day, anchoBanda, ultimo_paquete, ultimo_banda, ultima_location, email_client, precioMensual
    global identificacion, comprobante, factura

    session_data = load_session()

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

    if q.args.textname_client:
        name_client = session_data['name_client'] = q.args.textname_client
        await q.page.save()

    if q.args.textlastname_client:
        lastname_client = session_data['lastname_client'] = q.args.textlastname_client
        await q.page.save()

    if q.args.textphone_client:
        phone_client = session_data['phone_client'] = q.args.textphone_client
        await q.page.save()

    if q.args.textemail_client:
        email_client = session_data['email_client'] = q.args.textemail_client
        await q.page.save()

    if q.args.textaddress_client:
        address_client = session_data['address_client'] = q.args.textaddress_client
        await q.page.save()

    if q.args.textcolonia_client:
        colonia_client = session_data['colonia_client'] = q.args.textcolonia_client
        await q.page.save()

    if q.args.textlocalidad_client:
        localidad_client = session_data['localidad_client'] = q.args.localidad_client
        await q.page.save()

    if q.args.textmunicipio_client:
        municipio_client = session_data['municipio_client'] = q.args.textmunicipio_client
        await q.page.save()
    
    if q.args.textestado_client:
        estado_client = session_data['estado_client'] = q.args.textestado_client
        await q.page.save()

    if 'checkidentificacion_client' in q.args:
        if q.args.checkidentificacion_client:
            identificacion = session_data['identificacion'] = q.args.checkidentificacion_client
            await q.page.save()
        else:
            identificacion = session_data['identificacion'] = False
            await q.page.save()

    if 'checkcomprobante_client' in q.args:
        if q.args.checkcomprobante_client:
            comprobante = session_data['comprobante'] = q.args.checkcomprobante_client
            await q.page.save()
        else:
            comprobante = session_data['comprobante'] = False
            await q.page.save()
    
    if q.args.textrefaddress_client:
        refaddress_client = session_data['refaddress_client'] = q.args.textrefaddress_client
        await q.page.save()
    
    if q.args.textlocaddress_client:
        latitude, longitude = extract_lat_long_from_url(q.args.textlocaddress_client)
        # Actualiza `location_client` con las coordenadas extraídas
        if latitude and longitude:
            location_client = f"{latitude}, {longitude}"
            session_data['location_client'] = location_client  # Guarda en la sesión
            ultima_location = location_client
            await update_price_textbox(q)
        await q.page.save()

    if q.args.date_picker:
        # Convierte la cadena a un objeto datetime usando dateutil
        date_object = parser.parse(q.args.date_picker)
        # Formatea el objeto datetime para que solo muestre la fecha
        datepicker_client = session_data['datepicker_client'] = date_object.strftime('%Y-%m-%d')
        await q.page.save()

    if 'checkFactura' in q.args:
        if q.args.checkFactura:
            factura = session_data['factura'] = q.args.checkFactura
            await q.page.save()
        else:
            factura = session_data['factura'] = False
            await q.page.save()

    ##### GUARDAR LOS COMBOBOX DE ESTA MANERA ######
    if q.args.comboboxHorario and q.args.propietarioAddPoste!=str(q.args.comboboxHorario):
        if q.args.comboboxHorario != 'Seleccionar':
            tiposervicio = session_data['tiposervicio'] = str(q.args.comboboxHorario)
        await q.page.save()

    if 'comboboxPaqueteEquipo' in q.args:
        # Verifica que el valor de la combobox sea distinto del valor guardado previamente
        if q.args.comboboxPaqueteEquipo and q.args.paqueteplan != str(q.args.comboboxPaqueteEquipo):
            if q.args.comboboxPaqueteEquipo != 'Seleccionar':
                paqueteplan = session_data['paqueteplan'] = str(q.args.comboboxPaqueteEquipo)

                # Actualiza el precio en función del paquete seleccionado
                if paqueteplan == 'Comprado':
                    paqueteprecio = 1200
                elif paqueteplan == 'Comodato':
                    paqueteprecio = 600

                if paqueteplan != ultimo_paquete:  
                    # Actualiza el textbox del precio
                    await update_price_textbox(q)
                    await q.page.save()
                    ultimo_paquete = paqueteplan
                else:
                    await q.page.save()

    # Manejo de la combobox de ancho de banda
    if 'comboboxPaqueteMB' in q.args:
        # Verifica que el valor de la combobox sea distinto del valor guardado previamente
        if q.args.comboboxPaqueteMB and q.args.anchoBanda != str(q.args.comboboxPaqueteMB):
            if q.args.comboboxPaqueteMB != 'Seleccionar':
                anchoBanda = session_data['anchoBanda'] = str(q.args.comboboxPaqueteMB)

                # Actualiza el precio en función del ancho de banda seleccionado
                if anchoBanda == '30MB':
                    anchoprecio = 350
                elif anchoBanda == '50MB':
                    anchoprecio = 350
                elif anchoBanda == '100MB':
                    anchoprecio = 450
                elif anchoBanda == '200MB':
                    anchoprecio = 550

            if anchoBanda != ultimo_banda:
                # Actualiza el textbox del precio
                await update_price_textbox(q)
                await q.page.save()
                ultimo_banda = anchoBanda
            else:
                await q.page.save()

        if q.args.comboboxFormaPago:
            if q.args.comboboxFormaPago != 'Seleccionar':
                formatoPago = session_data['formatoPago'] = str(q.args.comboboxFormaPago)
            await q.page.save()

    save_session(session_data)

    if q.args.btnAdd:
        if  name_client != '':
            if lastname_client != '':
                if tiposervicio != "Seleccionar":
                    if paqueteplan != "Seleccionar":
                        if anchoBanda != "Seleccionar":
                            if formatoPago != "Seleccionar":
                                if phone_client != '':
                                    if address_client != '':
                                        if localidad_client != '':
                                            if municipio_client != '':
                                                if estado_client != '':
                                                    if refaddress_client != '':
                                                        if location_client != '':
                                                            if datepicker_client != '':
                                                                if colonia_client != '':
                                                                    if email_client != '':
                                                                        now = datetime.datetime.now()
                                                                        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                                                                        id_ticket = now.strftime("%Y%m%d%H%M%S")
                                                                        ### %Y%m%d%H%M%S
                                                                        json_datos = json.dumps({
                                                                            "id_ticket":str(id_ticket),
                                                                            "date_ticket":str(dt_string),
                                                                            "status":"Active",
                                                                            "date_status":str(dt_string),
                                                                            "name_client":str(name_client) + " " + str(lastname_client),
                                                                            "phone_client":str(phone_client),
                                                                            "email_client":str(email_client),
                                                                            "address_client":str(address_client),
                                                                            "localidad_client":str(localidad_client),
                                                                            "municipio_client":str(municipio_client),
                                                                            "estado_client":str(estado_client),
                                                                            "refaddress_client":str(refaddress_client),
                                                                            "colonia_client":str(colonia_client),
                                                                            "location_client":str(location_client),
                                                                            "datepicker_client":str(datepicker_client),
                                                                            "hora_propuesta":str(tiposervicio),
                                                                            "paqueteplan":str(paqueteplan),
                                                                            "anchoBanda":str(anchoBanda),
                                                                            "formatoPago":str(formatoPago),
                                                                            "precio_client":str(precio_client),
                                                                            "precioMensual":str(precioMensual),
                                                                            "identificacion":str(identificacion),
                                                                            "comprobante":str(comprobante),
                                                                            "factura":str(factura),
                                                                            "username":str("Admin"),
                                                                        })
                                                                        try:
                                                                            key_count=r.get('tickets_iis_key')
                                                                            if key_count == None:
                                                                                key_count = 0
                                                                            else:
                                                                                key_count=key_count.decode("utf-8")
                                                                                key_count=int(key_count)+1
                                                                            r.publish("tickets_iis",json_datos)
                                                                            createNewTicket(r, int(key_count), id_ticket, name_client, lastname_client, dt_string, phone_client, email_client, address_client, colonia_client, localidad_client, municipio_client, estado_client, refaddress_client, location_client, datepicker_client, tiposervicio, paqueteplan, anchoBanda, formatoPago, precio_client, precioMensual, identificacion, comprobante, factura);
                                                                            time.sleep(0.3)
                                                                        except Exception as e:
                                                                            print(e)
                                                                            pass
                                                                        # Reiniciar los valores de los campos
                                                                        name_client = ''
                                                                        lastname_client = ''
                                                                        phone_client = ''
                                                                        email_client = ''
                                                                        address_client = ''
                                                                        refaddress_client = ''
                                                                        colonia_client = ''
                                                                        location_client = ''
                                                                        localidad_client = ''
                                                                        municipio_client = ''
                                                                        estado_client = ''
                                                                        tiposervicio = 'Seleccionar'
                                                                        paqueteplan = 'Seleccionar'
                                                                        anchoBanda = 'Seleccionar'
                                                                        formatoPago = 'Seleccionar'

                                                                        # Borrar los datos de la sesion
                                                                        save_session({})

                                                                        print(datepicker_client)
                                                                        # Recargar el formulario
                                                                        await formu_ticket(q)                                                                                                     
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
                        ui.zone('body',size='93', direction=ui.ZoneDirection.COLUMN, zones=[
                            ui.zone('der1_1', size='100%', align='center', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('der1_11', size='50%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_12', size='50%', align='center', direction=ui.ZoneDirection.ROW),
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

        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='', icon='Back')])
        
        await q.run(formu_ticket,q)
        await q.page.save()


@app('/iis_create', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await iis_create(q)