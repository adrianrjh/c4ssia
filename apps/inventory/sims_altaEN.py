from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from common8 import *
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import csv
import pyshorteners
import webbrowser
import asyncio

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

client = Listener1(r, ['last_session'])
client.start()

########### P   A   S   O   1111111111111111111111 ###########
async def paso1(q: Q):
    global comboboxGaran, comboboxMarca, comboboxModelo, comboboxDescripcion, comboboxMotivos, data_rows
    global marcaEN, modeloEN, descripcionEN, garantiaEN, noserieEN, motivoEN
    
    del q.page['btnReport']
    del q.page['btnAtras1']
    del q.page['btnAtras2']
    del q.page['btnAtrasH']

    res = getAllMatsDevs(r, 'Equipos de Red')
    marcaBefore = ''
    comboboxMarca = []
    for x in range(0, len(res)):
        if marcaBefore != str(res[x][0]):
            marcaBefore = res[x][0]
            comboboxMarca.append(res[x][0])

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    q.page['combotextboxes'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.combobox(name='combomarca', label='Marca', value=str(marcaEN), choices=comboboxMarca,trigger=True, disabled=False),
            ui.combobox(name='combomodelo', label='Modelo', value=str(modeloEN), choices=comboboxModelo,trigger=True, disabled=False),
            ui.combobox(name='combodescripcion', label='Descripción', value=str(descripcionEN), choices=comboboxDescripcion,trigger=True, disabled=False),
            ui.combobox(name='combogarantia', label='Garantia', value=str(garantiaEN), choices=comboboxGaran,trigger=True, disabled=False),
            ui.combobox(name='combomotivos', label='Motivo', value=str(motivoEN), choices=comboboxMotivos,trigger=True, disabled=False),
            ui.button(name='btnSig1', label='Siguiente', disabled = False, primary=True,)
        ],
    )

    q.page['lista'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.text_xl(content='Lista de artículos usados'),
        ui.table(
            name='issues',
            multiple = True,
            columns=columnsRegEN,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            # Add pagination attribute to make your table paginated.
            # Register events to listen, all of these have to be handled by developer.
            #values = ['0'],
            groupable=False,
            downloadable=True,
            resettable=False,
        )
    ])

    q.page['boton2'] = ui.section_card(
        box=ui.box('der1_22', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='btnDelete', label='Delete', disabled = False, primary=True,),
            ui.button(name='btnCreateList', label='Create List', disabled = False, primary=True,)
        ],
    )
    await q.page.save()

########### P   A   S   O   222222222222222222 ###########
async def paso2(q: Q):
    del q.page['combotextboxes']
    del q.page['btnAtras1']
    del q.page['btnAtras2']
    del q.page['btnAtrasH']

    q.page['btnAtras1'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtras1', label='Atrás', disabled = False, primary=True)])
    q.page['combotextboxes']=ui.section_card(box=ui.box('der1_11',order=1),title='',subtitle='',
        items=[
            ui.textbox(name='textnoserie',label='N° Serie',value='',trigger=True,disabled=False),
            ui.button(name='btnAddMod', label='Guardar', disabled = False, primary=True,)
        ]
    )
    await q.page.save()

########### P   A   S   O   33333333333333333 ###########
async def paso3(q: Q):
    del q.page['lista']
    del q.page['boton2']
    del q.page['combotextboxes']
    del q.page['btnAtras1']
    del q.page['btnAtras2']
    del q.page['btnAtrasH']

    q.page['btnAtras2'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtras2', label='Atrás', disabled = False, primary=True)])
    q.page['combotextboxes']=ui.section_card(box=ui.box('der1_11',order=1),title='',subtitle='',items=[ui.text_xl('CREAR CODIGOS QR Y REGISTRAR A C4SSIADB')])
    q.page['lista'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.text_xl(content='Lista de artículos usados'),
        ui.table(
            name='issues',
            multiple = True,
            columns=columnsRegEN,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            # Add pagination attribute to make your table paginated.
            pagination=ui.table_pagination(total_rows=20, rows_per_page=10),
            # Register events to listen, all of these have to be handled by developer.
            events=['page_change'],
            #values = ['0'],
            groupable=False,
            downloadable=True,
            resettable=False,
        )
    ])
    q.page['boton2']=ui.section_card(box=ui.box('der1_22',order=1),title='',subtitle='',items=[ui.button(name='btnCreateQR',label='Registrar - Print QR',disabled=False,primary=True)])
    await q.page.save()

########### P   A   S   O   444444444444444444 ###########
async def paso4(q: Q):
    del q.page['combotextboxes']
    del q.page['lista']
    del q.page['boton2']
    del q.page['btnAtras1']
    del q.page['btnAtras2']
    del q.page['btnAtrasH']

    checkRight = 'http://'+ipGlobal+':10101/datasets/checkRight.png'
    q.page['btnReport'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='btnEndRecep',label='Finalizar - Reporte', disabled=False, primary=True),
            ui.image(title='Reporte creado correctamente!', path=checkRight)
        ]
    )
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
                await q.run(paso2,q)
                await q.page.save()
            if paso3P == 1 and bandPaso3 == 0:
                bandPaso3 = 1
                await q.run(paso3,q)
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

async def sims_altaEN(q: Q):
    print(str("starting sims_altaEN..."))
    global ipGlobal, session, username
    global data_rows, data_rows_keycount
    global marcaEN, modeloEN, descripcionEN, garantiaEN, noserieEN, motivoEN
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    global comboboxMarca, comboboxModelo, comboboxDescripcion, comboboxGaran
    global data_to_report

    q.page['meta'] = ui.meta_card(box='')

    if q.args.home:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.logout:
        session = False
        user = ''
        json_datos = json.dumps({"session":session, "user":user})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAtrasH:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_sims'
        await q.page.save()

    if q.args.btnAtras1:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        paso4P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnAtras2:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        paso4P = 0
        bandPaso1 = 0
        await q.page.save()

    if 'combomarca' in q.args:
        if q.args.combomarca and str(q.args.combomarca) != 'Seleccionar':
            marcaEN = str(q.args.combomarca)
            res = getAllDevsMarca(r, marcaEN)
            modeloBefore = ''
            comboboxModelo = []
            for x in range(0, len(res)):
                if modeloBefore != str(res[x][1]):
                    modeloBefore = res[x][1]
                    comboboxModelo.append(res[x][1])
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
            await q.page.save()

    if 'combomodelo' in q.args:
        if q.args.combomodelo and str(q.args.combomodelo) != 'Seleccionar':
            modeloEN = str(q.args.combomodelo)
            res = getAllDevsModelo(r, modeloEN)
            descripcionBefore = ''
            comboboxDescripcion = []
            for x in range(0, len(res)):
                if descripcionBefore != str(res[x][2]):
                    descripcionBefore = res[x][2]
                    comboboxDescripcion.append(res[x][2])
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
            await q.page.save()

    if 'combodescripcion' in q.args:
        if q.args.combodescripcion and str(q.args.combodescripcion) != 'Seleccionar':
            descripcionEN = str(q.args.combodescripcion)
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
            await q.page.save()

    if 'combogarantia' in q.args:
        if q.args.combogarantia and str(q.args.combogarantia) != 'Seleccionar':
            garantiaEN = str(q.args.combogarantia)
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
            await q.page.save()

    if 'combomotivos' in q.args:
        if q.args.combomotivos and str(q.args.combomotivos) != 'Seleccionar':
            motivoEN = str(q.args.combomotivos)
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
            await q.page.save()

    if q.args.btnSig1:
        paso1P = 0
        paso2P = 1
        paso3P = 0
        paso4P = 0
        bandPaso2 = 0
        await q.page.save()

    if 'textnoserie' in q.args:
        if q.args.textnoserie:
            noserieEN = str(q.args.textnoserie)
            await q.page.save()

    if q.args.btnAddMod:
        if marcaEN != 'Seleccionar' and marcaEN != '':
            if modeloEN != 'Seleccionar' and modeloEN != '':
                if descripcionEN != 'Seleccionar' and descripcionEN != '':
                    if garantiaEN != 'Seleccionar' and garantiaEN != '':
                        if motivoEN != 'Seleccionar' and motivoEN != '':
                            if noserieEN != '':
                                descripcionEN1 = descripcionEN.replace("(", " ")
                                descripcionEN2 = descripcionEN1.replace(")", " ")
                                data_rows_keycount += 1
                                data_rows.append([str(data_rows_keycount), str(noserieEN), 'N/A', str(marcaEN), str(modeloEN), str(descripcionEN2), str(garantiaEN), str(motivoEN), 'Almacen', 'Nuevo'])
                                marcaEN, modeloEN, descripcionEN, descripcionEN1, descripcionEN2, garantiaEN, noserieEN, motivoEN = 'Seleccionar', 'Seleccionar', 'Seleccionar', "", "", 'Seleccionar', '', 'Seleccionar'
                                paso1P = 1
                                paso2P = 0
                                paso3P = 0
                                paso4P = 0
                                bandPaso2 = 0
                            else:
                                q.page["meta"].side_panel = ui.side_panel(
                                    title="",
                                    items=[ui.text("Registro incompleto, por favor completa todos los campos.")],
                                    name="side_panel",
                                    events=["dismissed"],
                                    closable=True,
                                    width = '400px',
                                )
        await q.page.save()

    if q.args.btnCreateList:
        registrados = q.args.issues
        if registrados and len(registrados) == len(data_rows):
            paso1P = 0
            paso2P = 0
            paso3P = 1
            paso4P = 0
            bandPaso3 = 0
        else:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona todos los equipos, sino elimina el que no quieras registrar.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        await q.page.save()

    if q.args.btnDelete:
        print("delete...")
        eliminados = q.args.issues
        data_rows_temp, data_rows_send, found = [], [], 0
        if eliminados == None:
            pass
        if eliminados and eliminados != None:
            if len(eliminados) > 0:
                for y in data_rows:
                    for x in eliminados:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found = 0
            data_rows = data_rows_temp
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
        else:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un equipo para eliminarlo.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        await q.page.save()

    if q.args.btnCreateQR:
        selectionated = q.args.issues
        data_rows_temp, data_rows_send, found, counter_article, errno = [], [], 0, 0, ''
        if selectionated == None:
            pass
        if selectionated != None:
            if len(selectionated) == 1:
                for y in data_rows:
                    for x in selectionated:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found = 0
                marcareg = data_rows_send[0][3].replace("/", "-")
                modeloreg = data_rows_send[0][4].replace("/", "-")
                descripcionreg = data_rows_send[0][5].replace("/", "-")
                descripcionreg = data_rows_send[0][5].replace("(", "")
                descripcionreg = data_rows_send[0][5].replace(")", "")
                key_count=r.get('key_alm_new')
                if key_count == {} or key_count == None:
                    key_count = 0
                else:
                    key_count=key_count.decode("utf-8")
                    key_count=int(key_count)+1
                now = datetime.datetime.now()
                dt_string = now.strftime("%Y%m%d")
                fell = now.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    counter_article = rts.get(str(modeloreg))
                except Exception as e:
                    print(e)
                    errno = str(e)
                try:
                    if errno == 'TSDB: the key does not exist':
                        rts.add(str(modeloreg), int(time.time()), int(1))
                        errno = ''
                    if int(counter_article[1]) > 0:
                        updtArt = int(counter_article[1])+1
                        rts.add(str(modeloreg), int(time.time()), int(updtArt))
                except Exception as e:
                    print(e)
                ########## NOPR   PROYECTO     MARCA              MODELO            DESCRIPCION              NOSERIE              FECHA LLEGADA 
                qr_code = 'NA'+'/'+'NA'+'/'+str(marcareg)+'/'+str(modeloreg)+'/'+str(descripcionreg)+'/'+data_rows_send[0][1]+'/'+dt_string
                devNewToAlm(r, key_count, fell, 'NA', 'NA', str(marcareg), str(modeloreg), str(descripcionreg), data_rows_send[0][6], data_rows_send[0][1], qr_code, 'No Misc', data_rows_send[0][7])
                data_to_report.append([fell, 'NA', 'NA', str(marcareg), str(modeloreg), str(descripcionreg), data_rows_send[0][6], data_rows_send[0][1], qr_code, 'No Misc', data_rows_send[0][7]])
                ########### P    R   I   N   T        Q  R       C   O   D   E ############
                import qrcode
                from PIL import Image
                import os
                ## Obtener la ruta del directorio de Documentos para macOS y Linux
                documentos_path = os.path.join(os.path.expanduser('~'))
                nueva_carpeta_path = os.path.join(documentos_path, 'QR_CODES')
                documentos_path = os.path.join(os.path.expanduser('~'), 'QR_CODES/')
                os.makedirs(nueva_carpeta_path, exist_ok=True)
                ## Generar QR
                input_data = str(qr_code)
                qr = qrcode.QRCode(
                    version=1,
                    box_size=10,
                    border=5)
                qr.add_data(input_data)
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                img.save(documentos_path+'qr_code.png')
                import cups
                ## Conectar con CUPS
                conn = cups.Connection()
                ## Obtener la lista de impresoras
                printers = conn.getPrinters()
                ## Nombre de la impresora configurada en CUPS
                printer_name = '4BARCODE_3B-365B'
                ## Imprimir la imagen
                conn.printFile(printer_name, documentos_path+'qr_code.png', "QR Code Print", {})
                conn.printFile(printer_name, documentos_path+'qr_code.png', "QR Code Print", {})
                data_rows = data_rows_temp
                if len(data_rows) > 0:
                    paso1P = 0
                    paso2P = 0
                    paso3P = 1
                    paso4P = 0
                    bandPaso3 = 0
                else:
                    paso1P = 0
                    paso2P = 0
                    paso3P = 0
                    paso4P = 1
                    bandPaso4 = 0
        else:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Ingresa el número de serie del equipo.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        await q.page.save()

    if q.args.btnEndRecep:
        data_rows_keycount = 0
        data_user = getUser('user_key', 'user_','adrianfime')
        now = datetime.datetime.now()
        fell = now.strftime("%Y-%m-%d %H:%M:%S")
        json_datos={'fecha':str(fell),'fullname':str(data_user[0]),'puesto':str(data_user[1]),'lista':data_to_report}
        try:
            r.publish("yi_pdfs_recepcion_usados",json.dumps(json_datos))
            time.sleep(0.3)
        except Exception as e:
            print(e)
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        data_to_report = []
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
        await q.page.save()

    #icon_path, = site.upload(['/home/adrian/ws/h2o-wave/home/data/cassia-logo1.png'])
    #q.page['meta'] = ui.meta_card(box='', icon=icon_path, title='C4SSIA')
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
                            ui.zone('izq1', size='10%', zones=[
                                ui.zone('izq1_11',size='15%',align='center',direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('der1',size='90%', zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='25%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='40%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', size='30%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_13', size='30%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='75%', zones=[
                                        ui.zone('der1_21', size='90%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_22', size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ]),
                                ]),
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
        await q.run(paso1,q)
        await q.page.save()
        await q.run(start_or_restart_refresh,q)

@app('/sims_altaEN', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await sims_altaEN(q)
