from h2o_wave import main, app, ui, data, Q, AsyncSite
import time
import random
import redis,datetime
import asyncio
from redis import StrictRedis, ConnectionError
import json, threading
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common6 import *

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

async def addList(q: Q, data_olt1: data_rows, cell_olt1: columnsDev, data_olt2: data_rows2, cells_olt2: columnsDev2):
    global columnsDev, columnsT, columnsDev2, columnsT2
    
    del q.page['states1']
    del q.page['states2']
    del q.page['states3']
    del q.page['states4']
    await q.page.save()
    
    columnsT = []
    for x in range(0,int(len(columnsDev))):
        if columnsDev[x] == 'STATUS':
            columnsT.append(ui.table_column(name='tag', label=str(columnsDev[x]), max_width='90', cell_type=ui.tag_table_cell_type(name='tags', tags=[ui.tag(label='DISABLED', color='$red'), ui.tag(label='ENABLED', color='$mint')])))
        else:
            columnsT.append(ui.table_column(name='text'+str(x), label=str(columnsDev[x]), align='center', searchable=True, max_width='118'))

    columnsT2 = []
    for y in range(0,int(len(columnsDev2))):
        if columnsDev2[y] == 'ONLINE STATUS':
            columnsT2.append(ui.table_column(name='tag', label=str(columnsDev2[y]), max_width='110', cell_type=ui.tag_table_cell_type(name='tags', tags=[ui.tag(label='OFFLINE', color='$red'), ui.tag(label='ONLINE', color='$mint')])))
        else:
            columnsT2.append(ui.table_column(name='text'+str(y), label=str(columnsDev2[y]), align='center', searchable=True, max_width='125'))

    q.page['lista-table'] = ui.form_card(box=ui.box('mid1_11', order=1), items=[
        ui.table(
            name='issues',
            #multiple = True,
            checkbox_visibility='hidden',
            columns=columnsT,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            values = ['0'],
            groupable=True,
            downloadable=True
        )
    ])

    q.page['lista-table2'] = ui.form_card(box=ui.box('mid1_12', order=1), items=[
        ui.table(
            name='issues2',
            #multiple = True,
            checkbox_visibility='hidden',
            columns=columnsT2,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows2],
            values = ['0'],
            groupable=True,
            downloadable=True
        )
    ])

    await q.page.save()

async def rtm(q: Q):
    print("starting rtm app...")
    global username
    global session, equipo, device, columnsDev, columnsOLT, data_rows, columnsT, columnsDev2, columnsT2
    global inicio_val, dateStart, dateEnd, r
    global AV080, AV081, AV082, PP001, HW001, FAN001, CW001, Recir, Pasteur, CALM
    global niveluht,flujouht,sostenimiento_in,enfriamiento
    global niveluht_rows,flujouht_rows,sostenimiento_in_rows,enfriamiento_rows
    global aguacaliente,salidaproducto,sostenimiento_out, entrada_glicol
    global aguacaliente_rows,salidaproducto_rows,sostenimiento_out_rows, entrada_glicol_rows
    global brixlinea, gas, phEspera, tempEspera
    global tanque1, tanque2, tanque3, tanque4
    global brixlinea_rows, gas_rows, phEspera_rows, tempEspera_rows
    global tanque1_rows, tanque2_rows, tanque3_rows, tanque4_rows
    global temp_min_past, temp_max_past, flujo_min_past, flujo_max_past, tanques_dest, combotanque, noTanque
    global ipGlobal, comboboxTanques, recover, dateStart,dataInfo,dataInfoTanque,data_to_run,dataInfoPasteur

    recover = getAll(r,"conf_past")

    q.page['meta'] = ui.meta_card(box='')
    if q.args.issues:
        print(q.args.issues)
    await q.page.save()
    
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

    if q.args.textequipo and equipo != str(q.args.textequipo):
        equipo = str(q.args.textequipo)
        await q.page.save()

    if q.args.textdevices and device != str(q.args.textdevices):
        device = str(q.args.textdevices)
        await q.page.save()

    if q.args.btnGetDev:
        if equipo != 'Seleccionar':
            devices = []
            comboboxDev1 = []
            devices = getAll(r, 'infraYI')
            devices = devices['data'].replace("'","[")
            devices = json.loads(devices)
            for x in range(0,len(devices)):
                if equipo == devices[x][6]:
                    comboboxDev1.append(devices[x][0]+'_'+devices[x][13]+'_'+devices[x][12])
            q.page['comboboxDevices'] = ui.section_card(
                box=ui.box('izq1_12', order=1),
                title='',
                subtitle='',
                items=[
                    ui.combobox(name='textdevices', label='Devices', value='Seleccionar', choices=comboboxDev1,trigger=True),
                ],
            )
            q.page['btnMonitor'] = ui.section_card(
                box=ui.box('izq1_12', order=2),
                title='',
                subtitle='',
                items=[
                    ui.button(name='btnMonitor', label='Monitor', disabled = False, primary=True),
                ],
            )
        await q.page.save()

    if q.args.btnMonitor:
        del q.page['combotextboxes']
        del q.page['comboboxDevices']
        devices = []
        comboboxDev1 = []
        devices = getAll(r, 'infraYI')
        devices = devices['data'].replace("'","[")
        devices = json.loads(devices)
        for x in range(0,len(devices)):
            split_device = device.split("_")
            afidev = split_device[0]
            if afidev == devices[x][0]:
                print(devices[x])
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('izq1_11', order=1),
            title='',
            subtitle='',
            items=[ui.combobox(name='textequipo', label='Equipo', value='Seleccionar', choices=comboboxDisp,trigger=True),
            ],
        )
        q.page['comboboxDevices'] = ui.section_card(
            box=ui.box('izq1_12', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='textdevices', label='Devices', value='Seleccionar', choices=comboboxDev1,trigger=True),
            ],
        )
        if equipo == 'OLT':
            columnsDev = columnsOLT
            columnsDev2 = columnsOLT2
            await q.run(addList, q, data_rows, columnsDev, data_rows2, columnsDev2)
        await q.page.save()
    
    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        if session != True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
            await q.page.save()
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xl',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93%',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='10%', zones=[
                                ui.zone('izq1_11',size='20%', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_12',size='20%', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_13',size='20%', direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_14', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_15', align="center",size='20%', direction=ui.ZoneDirection.ROW)
                            ]),
                            ui.zone('mid1',size='90%', zones=[
                                ui.zone('mid1_3',size='100%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                                        ui.zone('mid1_1',size='50%', direction=ui.ZoneDirection.ROW, zones=[
                                            ui.zone('mid1_11', size='50%', align = 'center', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_12', size='50%', align = 'center', direction=ui.ZoneDirection.ROW),
                                        ]),
                                        ui.zone('mid1_2',size='50%', direction=ui.ZoneDirection.ROW, zones=[
                                            ui.zone('mid1_21',size='50%', align = 'center', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_22',size='50%', align = 'center', direction=ui.ZoneDirection.ROW),
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')
###############    T   O  P     H  E  A  D  E  R    #################
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_rtm'] = ui.header_card(
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

###############   L  E  F  T   S  I  D  E     A    #################
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('izq1_11', order=1),
            title='',
            subtitle='',
            items=[ui.combobox(name='textequipo', label='Equipo', value='Seleccionar', choices=comboboxDisp,trigger=True),
            ],
        )
        q.page['btnGetDev'] = ui.section_card(
            box=ui.box('izq1_11',order=2),
            title=' ',
            subtitle=' ',
            items=[  
                ui.button(
                    name='btnGetDev',
                    label='Get Devices',
                    #caption=' ',
                    #width= '100px',
                    disabled = False,
                    primary=True,
                ),
            ],
        )
###############   1ER   E  S  C  A  L  O  N    ################
        q.page['states1'] = ui.tall_stats_card(
            box=ui.box('mid1_11', order=1),
            items=[
                ui.stat(label='Data not found', value=str("")),
            ]
        )
###############   2DO   E  S  C  A  L  O  N    #################
        q.page['states2'] = ui.tall_stats_card(
            box=ui.box('mid1_12', order=1),
            items=[
                ui.stat(label='Data not found', value=str("")),
            ]
        )
###############   3ER   E  S  C  A  L  O  N    #################
        q.page['states3'] = ui.tall_stats_card(
            box=ui.box('mid1_21', order=1),
            items=[
                ui.stat(label='Data not found', value=str("")),
            ]
        )
###############   4TO   E  S  C  A  L  O  N    #################
        q.page['states4'] = ui.tall_stats_card(
            box=ui.box('mid1_22', order=1),
            items=[
                ui.stat(label='Data not found', value=str("")),
            ]
        )

        await q.page.save()

@app('/rtm', mode = 'unicast')
async def serve4(q: Q):
    route = q.args['#']
    await rtm(q)