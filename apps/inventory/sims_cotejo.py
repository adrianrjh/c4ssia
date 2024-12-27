from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys, os
import random, webbrowser
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from common8 import *
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from funcApp import *


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

async def showList(q: Q):
    global data_rows, columnsPRs

    q.page['table'] = ui.form_card(box=ui.box('mid1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columnsPRs,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        )
    ])

    await q.page.save()

async def refresh(q: Q):
    global fig, refreshDownload, data_rows
    while 1:

        await q.sleep(1)

async def sims_cotejo(q: Q):
    print(str("starting sims_cotejo app..."))
    global ipGlobal,session, r
    global data_rows, data_rows2, proyecto, descripcion, cantidad, costo, total, linkcompra, encargado, totalPR, username

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

    if q.args.btnAtras:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_sims'
        await q.page.save()
#########   U   P   D   A   T   E     T   A   B   L   E   ############
    if q.args.btnUpd:
        data_rows = getAllPrsxStatus(r, 'Purchased')
        if data_rows == 'NO':
            data_rows = []
        elif len(data_rows) > 0:
            q.page['boton2'].items[0].button.disabled = False
            q.page['boton2'].items[1].button.disabled = False
            q.page['boton2'].items[2].button.disabled = False
            q.page['boton2'].items[3].button.disabled = False
        await q.run(showList, q)
        await q.page.save()
#########    A   R   R   I   V   E   D      P   R   ############
    if q.args.btnArrivedPR:
        selectioned = q.args.issues
        if selectioned == None:
            pass
        if selectioned != None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            data_rows_send.append(y)
                    if found==0:
                        #pass
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                for i in range(0,len(data_rows_send)):
                    if data_rows_send[i][5] == 'Purchased':
                        updAct(data_rows_send, 'arrived')
                        data_rows = getAllPrsxUser(r, username)
                await q.run(showList, q)
        await q.page.save()
#########   D   O   W   N   L   O   A   D       P    D   F       P   R   ############
    if q.args.btnDownload:
        import base64
        selectioned = q.args.issues
        if selectioned == None:
            pass
        if selectioned != None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            data_rows_send.append(y)
                    if found==0:
                        #pass
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                # Recuperar el PDF codificado en base64 desde Redis
                pdf_base64 = r.get(data_rows_send[0][0])
                # Decodificar el PDF desde base64
                pdf_data = base64.b64decode(pdf_base64)
                # Escribir el PDF decodificado a un nuevo archivo
                rootHost = '/home/adrian/ws/wave/cassia/apps/pdfs/prs/docs/'
                with open(rootHost+data_rows_send[0][0]+'.pdf', 'wb') as file:
                    file.write(pdf_data)
                annotations_path, = await q.site.upload([rootHost+data_rows_send[0][0]+'.pdf'])
                webbrowser.open_new_tab(ipGlobal+':10101'+annotations_path)
                await q.run(showList, q)
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
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq',size='15%', zones=[
                                ui.zone('izq1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('izq1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('izq1_11', size='90%', align='start', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                            ui.zone('mid',size='70%', zones=[
                                ui.zone('mid1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('mid1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('mid1_11', size='90%', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('mid1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                            ui.zone('der',size='15%', zones=[
                                ui.zone('der1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='90%', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
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
        #########   Cassia Home   #########
        q.page['boton2'] = ui.section_card(
            box=ui.box('mid1_12', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnUpd', label='Update Table', disabled = False, primary=True,),
                ui.button(name='btnArrivedPR', label='Arrived PR', disabled = False, primary=False),
                ui.button(name='btnDownload', label='Descargar archivo', disabled = False, primary=True,)
            ],
        )

        q.page['btnAtras'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtras', label='Atrás', disabled = False, primary=True)])

        await q.page.save()
        data_rows = getAllPrsxStatus(r, 'Purchased')
        await q.run(showList,q)
        await q.run(refresh,q)

@app('/sims_cotejo', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await sims_cotejo(q)
