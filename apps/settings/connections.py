from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common5 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import csv

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

async def showList(q: Q, reg: int):
    global data_rows, data_rows_get, comboboxDev1, comboboxDev2
    del q.page['table-show']
    del q.page['combotextboxes']

    if reg == 0:
        q.page['table-show'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
            ui.table(
                name='issues',
                multiple = True,
                columns=columns,
                rows=[ui.table_row(
                    name=str(dato[0]),
                    cells=dato,
                )for dato in data_rows_get],
                values = ['0'],
                groupable=True,
                downloadable=True,
                resettable=True,
            )
        ])
    if reg == 1:
        q.page['table-show'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
            ui.table(
                name='issues',
                multiple = True,
                columns=columns,
                rows=[ui.table_row(
                    name=str(dato[0]),
                    cells=dato,
                )for dato in data_rows],
                values = ['0'],
                groupable=True,
                downloadable=True,
                resettable=True,
            )
        ])

    q.page['combotextboxes'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='getDevs',label='Get devices',disabled = False, primary=True,),
            ui.separator(label='  '),
            ui.combobox(name='textdev1', label='Dispositivo 1', value='Seleccionar', choices=comboboxDev1,trigger=True,disabled = False),
            ui.combobox(name='textdev2', label='Dispositivo 2', value='Seleccionar', choices=comboboxDev2,trigger=True,disabled = False),
            ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
        ],
    )

    await q.page.save()

async def connections(q: Q):
    print(str("starting connections app..."))
    global ipGlobal, selectioned, devices, session
    global data_rows, data_rows_get
    global comboboxDev1, comboboxDev2
    global ciudad, municipio, localidad, referencia, dependencia, equipo, tecnologia
    global dispositivo, ipDevice, latitud, longitud, ID_Count, conectedTo
    global devices, device1, device2

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

    if q.args.getDevs:
        devices = []
        comboboxDev1 = []
        comboboxDev2 = []
        devices = getAll(r, 'infraYI')
        devices = devices['data'].replace("'","[")
        devices = json.loads(devices)
        for x in range(0,len(devices)):
            comboboxDev1.append(devices[x][0]+'_'+devices[x][13]+'_'+devices[x][12])
            comboboxDev2.append(devices[x][0]+'_'+devices[x][13]+'_'+devices[x][12])
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='getDevs',label='Get devices',disabled = True,primary=True,),
                ui.separator(label='  '),
                ui.combobox(name='textdev1', label='Dispositivo 1', value='Seleccionar', choices=comboboxDev1,trigger=True,disabled = False),
                ui.combobox(name='textdev2', label='Dispositivo 2', value='Seleccionar', choices=comboboxDev2,trigger=True,disabled = False),
                ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
            ],
        )
        await q.page.save()

    if q.args.textdev1 and device1 != str(q.args.textdev1):
        device1 = str(q.args.textdev1)
        await q.page.save()

    if q.args.textdev2 and device2 != str(q.args.textdev2):
        device2 = str(q.args.textdev2)
        await q.page.save()

    if q.args.btnGetConns:
        devices = []
        data_rows_get = []
        devices = getAll(r, 'connsYI')
        if devices != 'NO':
            if devices['data'] != '[]':
                devices = devices['data'].replace("'","[")
                data_rows_get = json.loads(devices)
                q.page['boton2'].items[0].button.disabled = False
                q.page['boton2'].items[1].button.disabled = False
        await q.run(showList,q, 0)
        await q.page.save()

    if q.args.btnActiConns:
        print(str("Activate..."))
        activate =q.args.issues
        data_rows_temp,found=[],0
        for y in data_rows_get:
            for x in activate:
                if str(y[0])==str(x):
                    found=1
                    data_rows_temp.append([y[1],y[2]])
            if found==0:
                pass
            found=0

        data_rows_act=data_rows_temp
        print(data_rows_act)
        await q.page.save()
    if q.args.addMod:
        if device1 != 'Seleccionar':
            if device2 != 'Seleccionar':
                if device1 != device2:
                    data_rows_get = []
                    split_device1 = device1.split("_")
                    split_device2 = device2.split("_")
                    lvldev1 = split_device1[1]
                    iddev1 = split_device1[2]
                    lvldev2 = split_device2[1]
                    iddev2 = split_device2[2]
                    conndevs = '['+lvldev1+','+iddev1+']'+'['+lvldev2+','+iddev2+']'
                    data_rows.append([conndevs,device1,device2])
                    device1, device2, conndevs = '', '', ''
                    await q.run(showList, q, 1)
        q.page['boton2'].items[0].button.disabled = False
        q.page['boton2'].items[1].button.disabled = False
        await q.page.save()

    if q.args.btnSave:
        msg = []
        devices = getAll(r, 'connsYI')
        if devices != 'NO':
            if devices['data']!='[]':
                msg = devices['data'].replace("'","[")
                data_rows_save = json.loads(msg)
                guardados = q.args.issues
                data_rows_temp, data_rows_save, found = [], [], 0
                for y in data_rows_save:
                    for x in guardados:
                        if str(y[0])==str(x):
                            found=1
                            data_rows.append(y)
                    if found==0:
                        data_rows_save.append(y)
                    found=0
                if len(data_rows_save) > 0:
                    for z in range(0, len(data_rows_temp)):
                        data_rows_save.append([data_rows_temp[z][0], data_rows_temp[z][1]])
                    connsYI(r, 'connsYI', data_rows_save)
                data_rows, device1, device2 = [], '', ''
        if devices == 'NO' or devices['data'] == '[]':
            r.delete('connsYI')
            connsYI(r, 'connsYI', data_rows)
            data_rows = []
            device1, device2 = '',''
        await q.run(showList, q, 1)
        await q.page.save()

    if q.args.btnDelete:
        print(str("delete..."))
        eliminados =q.args.issues
        data_rows_temp,found=[],0
        for y in data_rows_get:
            for x in eliminados:
                if str(y[0])==str(x):
                    found=1
            if found==0:
                data_rows_temp.append(y)
            found=0

        data_rows_get=data_rows_temp
        connsYI(r, 'connsYI', data_rows_get)

        await q.run(showList,q, 0)
        await q.page.save()

    if q.args.settings:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/settings'
        await q.page.save()
    await q.page.save()

    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        if session != True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
            await q.page.save()
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='10%', zones=[
                                ui.zone('izq1_11',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('der1',size='90%', zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='30%', direction=ui.ZoneDirection.COLUMN, zones=[
                                            ui.zone('der1_11', size='90%', align='center', direction=ui.ZoneDirection.COLUMN),
                                            ui.zone('der1_12', size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='70%', zones=[
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
        q.page['header2_connections'] = ui.header_card(
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

        #########   Cassia Home   #########

        q.page['boton3'] = ui.section_card(
            box=ui.box('izq1_15', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnGetConns', label='Get Conn\'s', disabled = False, primary=True,)
            ],
        )

        q.page['activateConn'] = ui.section_card(
            box=ui.box('izq1_15', order=2),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnActiConns', label='Activate Conn\'s', disabled = False, primary=True,)
            ],
        )
        
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='getDevs',label='Get devices',disabled = False,primary=True,),
                ui.separator(label='  '),
                ui.combobox(name='textdev1', label='Dispositivo 1', value='Seleccionar', choices=comboboxDev1,trigger=True,disabled = True),
                ui.combobox(name='textdev2', label='Dispositivo 2', value='Seleccionar', choices=comboboxDev2,trigger=True,disabled = True),
                ui.button(name='addMod',label='Agregar',disabled = True,primary=True,)
            ],
        )

        q.page['boton2'] = ui.section_card(
            box=ui.box('der1_22', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnDelete',label='Delete',disabled = True,primary=True,),
                ui.button(name='btnSave',label='Save',disabled = True,primary=True,)
            ],
        )

        await q.run(showList,q, 1)
        
        if len(data_rows) > 0:
            q.page['boton2'].items[0].button.disabled = False
            q.page['boton2'].items[1].button.disabled = False
        
        await q.page.save()

@app('/connections', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await connections(q)