from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common8 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import csv
import pyshorteners
import webbrowser
import asyncio

#class Listener1(threading.Thread):
#    def __init__(self, r, channels):
#        threading.Thread.__init__(self)
#
#        self.redis,self.init = r,0
#        self.pubsub = self.redis.pubsub()
#        print('Listener1...')
#
#        try:
#            self.pubsub.subscribe(channels)
#        except Exception as e:
#            print(e)
#
#    def work(self, item):
#        global session, puesto, username
#        data=0
#        try:
#            data = json.loads(item.decode('utf8'))
#            session = data['session']
#            puesto = data['puesto']
#            username = data['username']
#        except Exception as e:
#            print(e)
#
#    def run(self):
#        while True:
#            try:
#                message = self.pubsub.get_message()
#                if message:
#                    if (message['channel'].decode("utf-8")=="last_session"):
#                        self.work(message['data'])
#                    else:
#                        pass
#            except ConnectionError:
#                print('[lost connection]')
#                while True:
#                    print('trying to reconnect...')
#                    try:
#                        self.redis.ping()
#                    except ConnectionError:
#                        time.sleep(10)
#                    else:
#                        self.pubsub.subscribe(['last_session'])
#                        break
#            time.sleep(0.001)  # be nice to the system :)
#
#client = Listener1(r, ['last_session'])
#client.start()

########### P   A   S   O   1111111111111111111111 ###########
async def paso1(q: Q):
    global comboboxTrabajadores

    del q.page['lista']
    del q.page['combotextboxes']
    del q.page['total']
    del q.page['boton2']
    del q.page['btnReport']

    q.page['menuBtns'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.textbox(name='textproyecto', label='Proyecto', value='',trigger=True),
            ui.combobox(name='comboboxencargado', label='Dirigido por', value='Seleccionar', choices=comboboxTrabajadores,trigger=True),
            ui.button(name='btnRegis', label='Registro', disabled = False, primary=True)
        ],
    )

    await q.page.save()
########### P   A   S   O   33333333333333 ###########
async def paso2(q: Q):
    global comboboxGaran, comboboxMarca, comboboxModelo, comboboxDescripcion, totalPR, matsdevs, data_rows
    global marcaPRs, modeloPRs, descripcionPRs, unidadPRs, cantidadPRs, costoPRs, garantiaPRs, linkCompraPRs

    del q.page['menuBtns']
    del q.page['menuBtns1']
    del q.page['menuBtns1Btn']
    del q.page['combotextboxes']
    del q.page['lista']
    del q.page['boton2']
    del q.page['total']

    q.page['combotextboxes'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.combobox(name='comboboxmatdevs', label='Tipo de material', value=str(matsdevs), choices=comboboxMatDevs,trigger=True),
            ui.combobox(name='combomarca', label='Marca', value=str(marcaPRs), choices=comboboxMarca,trigger=True, disabled=False),
            ui.combobox(name='combomodelo', label='Modelo', value=str(modeloPRs), choices=comboboxModelo,trigger=True, disabled=False),
            ui.combobox(name='combodescripcion', label='Descripción', value=str(descripcionPRs), choices=comboboxDescripcion,trigger=True, disabled=False),
            ui.textbox(name='textunidad', label='Unidad', value=str(unidadPRs), trigger=True, disabled=True),
            ui.spinbox(name='cantidad', label='Cantidad', value=int(cantidadPRs), trigger=False, disabled=False),
            ui.textbox(name='textcosto', label='Costo', value=str(costoPRs), trigger=True, disabled=False),
            ui.combobox(name='combogarantia', label='Garantia', value=str(garantiaPRs), choices=comboboxGaran,trigger=True, disabled=False),
            ui.textbox(name='textlink', label='Link de compra', value=str(linkCompraPRs), trigger=True, disabled=False),
            ui.button(name='addMod', label='Agregar', disabled = False, primary=True,)
        ],
    )

    q.page['lista'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.text_xl(content='Lista de artículos'),
        ui.table(
            name='issues',
            multiple = True,
            columns=columns,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            # Add pagination attribute to make your table paginated.
            pagination=ui.table_pagination(total_rows=20, rows_per_page=10),
            # Register events to listen, all of these have to be handled by developer.
            events=['page_change'],
            values = ['0'],
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
            ui.button(name='btnCreate', label='Create PR', disabled = False, primary=True,)
        ],
    )
    q.page['total'] = ui.small_stat_card(box=ui.box('der1_13', order=1), title='Total $ PR', value=f'${totalPR}')
    await q.page.save()

########### P   A   S   O   44444444444444444 ###########
async def paso3(q: Q):
    
    del q.page['menuBtns1']
    del q.page['menuBtns1Btn']
    del q.page['combotextboxes']
    del q.page['lista']
    del q.page['boton2']
    del q.page['total']

    checkRight = 'http://'+ipGlobal+':10101/datasets/checkRight.png'
    q.page['btnReport'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='btnEndRecep',label='Finalizar - Reporte', disabled=False, primary=True),
            ui.image(title='PR creado correctamente!', path=checkRight)
        ]
    )
    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, bandPaso1, bandPaso2, bandPaso3
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
                await q.page.save()
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global bandPaso1, bandPaso2, bandPaso3
    
    bandPaso1, bandPaso2, bandPaso3 = 0, 0, 0
    
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

async def prs(q: Q):
    print(str("starting prs..."))
    global ipGlobal, session, username
    global data_rows, data_rows_keycount
    global proyecto, marca, modelo, descripcion, cantidad, costo, garantia, total, linkcompra, encargado, totalPR, recibidos, matsdevs, unidad
    global paso1P, paso2P, paso3P, bandPaso1, bandPaso2, bandPaso3
    global comboboxMarca, comboboxModelo, comboboxDescripcion, comboboxGaran
    global marcaPRs, modeloPRs, descripcionPRs, unidadPRs, cantidadPRs, costoPRs, garantiaPRs, linkCompraPRs

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
        user = ''
        json_datos = json.dumps({"session":session, "user":user})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAtrasH:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_prs'
        await q.page.save()

    if q.args.textproyecto:
        proyecto = str(q.args.textproyecto)
        await q.page.save()

    if q.args.comboboxencargado and str(q.args.comboboxencargado) != 'Seleccionar':
        encargado = str(q.args.comboboxencargado)
        await q.page.save()

    if q.args.btnRegis:
        if proyecto != '':
            if encargado != 'Seleccionar' or encargado != '':
                paso1P = 0
                paso2P = 1
                paso3P = 0
                bandPaso2 = 0
        await q.page.save()

    if q.args.comboboxmatdevs and str(q.args.comboboxmatdevs) != 'Seleccionar':
        if matsdevs != str(q.args.comboboxmatdevs):
            matsdevs = str(q.args.comboboxmatdevs)
            res = getAllMatsDevs(r, matsdevs)
            comboboxMarca = list(set([str(x[0]) for x in res]))  # Obtener marcas únicas
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.combomarca and str(q.args.combomarca) != 'Seleccionar':
        if marcaPRs!=str(q.args.combomarca):
            marcaPRs = str(q.args.combomarca)
            if matsdevs == 'Materiales de construccion':
                res = getAllMatsMarca(r, marcaPRs)
            if matsdevs == 'Equipos de Red':
                res = getAllDevsMarca(r, marcaPRs)
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
        if modeloPRs!=str(q.args.combomodelo):
            modeloPRs = str(q.args.combomodelo)
            if matsdevs == 'Materiales de construccion':
                res = getAllMatsModelo(r, modeloPRs)
            if matsdevs == 'Equipos de Red':
                res = getAllDevsModelo(r, modeloPRs)
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
        if descripcionPRs!=str(q.args.combodescripcion):
            descripcionPRs = str(q.args.combodescripcion)
            if matsdevs == 'Materiales de construccion':
                res = getAllMatsDescripcion(r, descripcionPRs)
            if matsdevs == 'Equipos de Red':
                res = getAllDevsDescripcion(r, descripcionPRs)
            unidadPRs = res
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.cantidad:
        cantidadPRs=str(q.args.cantidad)
        await q.page.save()

    if q.args.textcosto:
        costoPRs=str(q.args.textcosto)
        await q.page.save()

    if q.args.combogarantia and str(q.args.combogarantia) != 'Seleccionar':
        if garantiaPRs!=str(q.args.combogarantia):
            garantiaPRs = str(q.args.combogarantia)
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.textlink:
        linkCompraPRs=str(q.args.textlink)
        await q.page.save()

    if q.args.addMod:
        if proyecto != '':
            if marcaPRs != '':
                if modeloPRs != '':
                    if descripcionPRs != '':
                        if unidadPRs != '':
                            if cantidadPRs != '':
                                if costoPRs != '':
                                    if garantiaPRs != 'Seleccionar':
                                        if linkCompraPRs != '':
                                            if linkCompraPRs.find('https://') != -1:
                                                total = float(cantidadPRs)*float(costoPRs)
                                                totalPR = totalPR+total
                                                total = '$'+str(total)
                                                costoPRs = '$'+str(float(costoPRs))
                                                # Crear un objeto Shortener
                                                s = pyshorteners.Shortener()
                                                # Acortar la URL utilizando TinyURL
                                                linkCompraPRs = s.tinyurl.short(linkCompraPRs)
                                                data_rows_keycount += 1
                                                data_rows.append([str(data_rows_keycount), proyecto, marcaPRs, modeloPRs, descripcionPRs, unidadPRs, cantidadPRs, costoPRs, str(total), str(garantiaPRs), linkCompraPRs, str(recibidos)])
                                                q.page['total'].value = str(totalPR)
                                                marcaPRs, modeloPRs, descripcionPRs, unidadPRs, cantidadPRs, costoPRs, garantiaPRs, linkCompraPRs = 'Seleccionar', 'Seleccionar', 'Seleccionar', '', 1, '', 'Seleccionar', ''
                                                bandRefresh = 0
                                                q.page['boton2'].items[0].button.disabled = False
                                                q.page['boton2'].items[1].button.disabled = False
                                                q.page['boton2'].items[2].button.disabled = False
                                                q.page['boton3'].items[0].button.disabled = False
                                                await q.sleep(1)
                                                paso1P = 0
                                                paso2P = 1
                                                paso3P = 0
                                                bandPaso2 = 0
                                            else:
                                                q.page["meta"].side_panel = ui.side_panel(
                                                    title="",
                                                    items=[ui.text("Necesitas ingresar un link valido")],
                                                    name="side_panel",
                                                    events=["dismissed"],
                                                    closable=True,
                                                    width = '400px',
                                                )
        await q.page.save()

    if q.args.btnCreate:
        key_count=r.get('key_prs')
        if key_count == {}:
            key_count = 0
        else:
            key_count=key_count.decode("utf-8")
            key_count=int(key_count)+1
        regList(r, key_count, proyecto, encargado, username, data_rows, totalPR)
        data_rows, data_rows_keycount, descripcion, cantidad, costo, total, linkcompra, totalPR = [], 0, '', '', '', '', '', 0.0
        await q.sleep(1)
        paso1P = 0
        paso2P = 0
        paso3P = 1
        bandPaso3 = 0
        await q.page.save()

    if q.args.btnDelete:
        print(str("delete..."))
        eliminados = q.args.issues
        data_rows_temp, data_rows_send, found = [], [], 0
        if len(eliminados) > 0 and len(eliminados) < 2:
            for y in data_rows:
                for x in eliminados:
                    if str(y[0])==str(x):
                        found=1
                        # si quieres quitar los que seleccionaste
                        data_rows_send.append(y)
                        totalEquipo = data_rows_send[0][5].split("$")
                if found==0:
                    # si quieres quitar los que no seleccionaste
                    data_rows_temp.append(y)
                found = 0
        totalPR = (float(totalPR)-float(totalEquipo[1]))
        q.page['total'].value = str(totalPR)
        data_rows = data_rows_temp
        await q.page.save()

    if q.args.btnEndRecep:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
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
                                    ui.zone('der1_1', size='40%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='40%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', size='30%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_13', size='30%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='60%', zones=[
                                        ui.zone('der1_21', size='80%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_22', size='20%', align='center', direction=ui.ZoneDirection.ROW),
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
        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
        await q.run(paso1,q)
        await q.page.save()
        await q.run(start_or_restart_refresh,q)

@app('/prs', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await prs(q)