from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common4 import *
sys.path.insert(0, '/home/adrian/ws/wave/cassia/data')
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
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
                        #self.work(message['data'])
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

client = Listener1(r, ['last_session','LT01TP0LT'])
client.start()

async def paso1(q: Q):
    global comboboxProjPaP, proyecto
    
    del q.page['table']
    del q.page['upldCSV']
    del q.page['plot']
    del q.page['boton2']

    proyecto = ''
    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    comboboxProjPaP = getAllprojectPaP(r)
    if comboboxProjPaP == 'NO':
        comboboxProjPaP = []
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnSearch',label='Buscar',disabled = False,primary=True,),
                ui.button(name='btnCSV',label='Subir Proyecto',disabled = False,primary=False,)
        ]
    )

    await q.page.save()

async def paso2(q: Q):
    global data_rows, data_rows_density
    del q.page['comboboxBtns']
    del q.page['plot']

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    q.page['upldCSV'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='btnConsultar', label='Consultar', disabled = False, primary=False,),
            ui.file_upload(name='file_upload',label='Upload!',multiple=True,file_extensions=['csv'],max_file_size=10,max_size=15, compact=True),
            ui.button(name='btnUpload', label='Upload', disabled = False, primary=True,),
        ]
    )

    q.page['table'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columnsProjects,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=True,
        )
    ])

    q.page['boton2'] = ui.section_card(
        box=ui.box('der1_22', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name = 'btnSave', label = 'Save', disabled = False, primary = True)
        ],
    )

    await q.page.save()

async def paso3(q: Q):
    global proyecto, paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    try:
        while 1:
            if proyecto != '' and proyecto != 'Seleccionar':
                from plotly import graph_objects as go
                from plotly import io as pio
                del q.page['plot']
                del q.page['boton2']
                del q.page['comboboxBtns'] 
                q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
                comboboxProjPaP = getAllprojectPaP(r)
                q.page['comboboxBtns'] = ui.section_card(
                    box=ui.box('der1_11', order=1),
                    title='',
                    subtitle='',
                    items=[
                        ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                        ui.button(name='btnSearch',label='Buscar',disabled = False,primary=True,),
                        ui.button(name='btnCSV',label='Subir Proyecto',disabled = False,primary=False,)
                    ]
                )
                ######### RADIOGRAFIA DE FIBRA ##########
                q.page['plot'] = ui.section_card(box=ui.box('der1_21', order=1), title='', subtitle='',items=[ui.frame(content='', width='1750px', height='1000px')])
                html = 0
                fig = connectionsTraces(proyecto)
                html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
                q.page['plot'].items[0].frame.content = html
                await q.page.save()
            else:
                paso1P = 1
                paso2P = 0
                paso3P = 0
                paso4P = 0
                bandPaso1 = 0
                await q.page.save()
            await q.sleep(60)
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
    global paso1P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    paso1P, bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 1, 0, 0, 0, 0
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

async def pap_projects(q: Q):
    print(str("starting pap_projects..."))
    global ipGlobal,session
    global data_rows, data_rows_keycount, data_rows_density
    global comboboxMuniCol, comboboxMuniMich, comboboxMuniJal, comboboxEst, comboboxMuni, comboboxDisp, comboboxEquipo
    global afiliciacion, ciudad, municipio, localidad, referencia, dependencia, equipo, tecnologia
    global dispositivo, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo, host, proyecto
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4

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

    if q.args.textproyecto:
        proyecto = str(q.args.textproyecto)
        await q.page.save()

    if q.args.btnConsultar:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        paso4P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnCSV:
        data_rows = []
        paso1P = 0
        paso2P = 1
        paso3P = 0
        paso4P = 0
        bandPaso2 = 0
        await q.page.save()

    if q.args.btnSearch:
        if proyecto != '' and proyecto != 'Seleccionar':
            paso1P = 0
            paso2P = 0
            paso3P = 1
            paso4P = 0
            bandPaso3 = 0
        await q.page.save()

    if q.args.btnUpload:
        if q.args.file_upload:
            count = 0
            data_rows = []
            # Since multiple file uploads are allowed, the file_upload argument is a list.
            for path in q.args.file_upload:
                # To use the file uploaded from the browser to the wave server, download it into the app.
                local_path = await q.site.download(path, '../../data/')
                with open(local_path) as csvfile:
                    reader = csv.reader(csvfile) # change contents to floats
                    for row in reader: # each row is a list
                        count += 1
                        if count > 1:
                            if row[22] != 'N/A' and row[22] != '':
                                if float(row[22]) >= 0 and float(row[22]) < 6:
                                    quality = 'Excelente'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= -6  and float(row[22]) < 0:
                                    quality = 'Excelente'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= 6 and float(row[22]) < 11:
                                    quality = 'Muy bueno'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= -11  and float(row[22]) < -6:
                                    quality = 'Muy bueno'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= 11 and float(row[22]) < 16:
                                    quality = 'Bueno'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= -16 and float(row[22]) < -11:
                                    quality = 'Bueno'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= 16 and float(row[22]) < 21:
                                    quality = 'Regular'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= -21 and float(row[22]) < -16:
                                    quality = 'Regular'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= 21 and float(row[22]) <= 25:
                                    quality = 'Malo'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                if float(row[22]) >= -25 and float(row[22]) <= -21:
                                    quality = 'Malo'
                                    data_rows_density.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                                data_rows.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23]+'%', quality])
                            if row[23] == 'N/A':
                                data_rows.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[21], row[22], row[23], 'N/A'])
            paso1P = 0
            paso2P = 1
            paso3P = 0
            paso4P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.btnSave:
        guardados = q.args.issues
        if guardados != [] and guardados != None:
            data_rows_density_table, data_rows_temp, data_rows_send, found, counter = [], [], [], 0, 0
            if len(guardados) == len(data_rows):
                for y in data_rows:
                    for x in guardados:
                        if str(y[0])==str(x):
                            found=1
                            data_rows_send.append(y)
                    if found==0:
                        data_rows_temp.append(y)
                    found=0
                for z in data_rows_density:
                    for counterBox in range(1, int(z[8])+1):
                        counter += 1
                        data_rows_density_table.append([str(counter), z[1], z[2], z[3], z[4], z[5], z[7], 'PUERTO '+str(counterBox), z[12], z[13],'', '', '', '', '', '', '', '', ''])
                regProjPaP(r, data_rows_send)
                regProjDensityPaP(r, data_rows_density_table)
                data_rows = []
                paso1P = 1
                paso2P = 0
                paso3P = 0
                paso4P = 0
                bandPaso1 = 0
            else:
                pass
                ####aquí van notificaciones#####
        else:
            pass
            ####aquí van notificaciones#####
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
                                    ui.zone('der1_1', size='15%', direction=ui.ZoneDirection.COLUMN, zones=[
                                            ui.zone('der1_11', size='100%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='85%', zones=[
                                        ui.zone('der1_21', size='90%', align='center', direction=ui.ZoneDirection.ROW),
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
        q.page['header2_pap_projects'] = ui.header_card(
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
        await q.run(start_or_restart_refresh,q)
        await q.page.save()

@app('/pap_projects', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_projects(q)