from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common7 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

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
    global data_rows, columns
    
    q.page['table'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columns,
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

async def mytickets(q: Q):
    print(str("starting mytickets app..."))
    global ipGlobal, session, r
    global data_rows

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
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/settings'
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
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq',size='5%', zones=[
                                ui.zone('izq1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('izq1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('izq1_11', size='10%', align='start', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_12', size='20%', align='start', direction=ui.ZoneDirection.ROW),
                                        ui.zone('izq1_13', size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_14', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_15', size='30%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                            ui.zone('der',size='95%', zones=[
                                ui.zone('der1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='100%', direction=ui.ZoneDirection.COLUMN),
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
        
        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='', icon='Back')])
        
        await q.page.save()
        await q.run(showList,q)

@app('/mytickets', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await mytickets(q)