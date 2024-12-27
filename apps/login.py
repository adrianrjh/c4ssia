from h2o_wave import Q, app, main, ui, AsyncSite,site,data
#from pyzabbix import ZabbixAPI
import threading,json,time,math
from datetime import datetime
import sys
from redis import StrictRedis, ConnectionError
from redistimeseries.client import Client
import random
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common0 import *
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

async def login(q: Q):
    global session, usernameL, passwordL
    print("Start aplication login...")

    if q.args.signin:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/signin'
        await q.page.save()

    if q.args.username:
        usernameL=str(q.args.username)
        await q.page.save()

    if q.args.password:
        passwordL=str(q.args.password)
        await q.page.save()

    if q.args.login:
        if usernameL != '' and passwordL != '':
            user = getUser('user_key', 'user_',usernameL,passwordL)
            if user[0] == 'Yes':
                session = True
                json_datos = json.dumps({"session":session, "puesto":user[1], "username": usernameL})
                try:
                    r.publish("last_session",json_datos)
                except Exception as e:
                    print(e)
                yaainternet_logo = 'http://'+ipGlobal+':10101/datasets/yaainternet.png'
                checkRight = 'http://'+ipGlobal+':10101/datasets/checkRight.png'
                q.page['logInYI'] = ui.section_card(
                    box=ui.box(zone='center1_12', order=1),
                    title='',subtitle='',
                    items=[
                        ui.persona(title='LOG IN C4SSIA', subtitle='', caption='', size='l', image=yaainternet_logo),
                        ui.textbox(name='username', label='Username', required=True),
                        ui.textbox(name='password', label='Password', password=True, required=True),
                        ui.button(name='login', label='Log In', primary=True),
                        ui.persona(title='Succesful!', subtitle='', caption='', size='s', image=checkRight),
                    ]
                )
                await q.sleep(2)
                q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
            await q.page.save()
            if user[0] == 'No':
                time.sleep(1)
                yaainternet_logo = 'https://yaainternet.com/wp-content/uploads/2023/07/Logo.png'
                checkWrong = 'https://freepngimg.com/thumb/red_cross_mark/5-2-red-cross-mark-download-png.png'
                q.page['logInYI'] = ui.section_card(
                    box=ui.box(zone='center1_12', order=1),
                    title='',subtitle='',
                    items=[
                        ui.persona(title='LOG IN C4SSIA', subtitle='', caption='', size='l', image=yaainternet_logo),
                        ui.textbox(name='username', label='Username', required=True, error='username or password wrong'),
                        ui.textbox(name='password', label='Password', password=True, required=True, error='username or password wrong'),
                        ui.button(name='login', label='Log In', primary=True),
                        #ui.persona(title='username or password wrong', subtitle='', caption='', size='s', image=checkWrong),
                ])
                await q.page.save()
                await q.sleep(1)
            await q.page.save()
    await q.page.save()
    
    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
            await q.page.save()
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                    ui.zone('header',size='7%'),
                    ui.zone('body',size='93%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq1', size='33%', zones=[
                            ui.zone('izq1_1',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_2',size='14%'),
                        ]),
                        ui.zone('cen1',size='33%', direction=ui.ZoneDirection.COLUMN, zones=[
                            ui.zone('center1_11',size='30%',align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('center1_12',size='40%',align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('center1_13',size='30%',align='center',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der1',size='33%', zones=[
                            ui.zone('der1_11', align='center',size='100%',direction=ui.ZoneDirection.COLUMN),
                        ]),
                    ]),
                ]),
                ],
            ),
        ], theme='winter-is-coming')
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_login'] = ui.header_card(
            box='header',
            title='C 4 S S I A',
            subtitle='YAA Internet',
            items=[],
        )
        yaainternet_logo = 'https://yaainternet.com/wp-content/uploads/2023/07/Logo.png'
        q.page['logInYI'] = ui.section_card(
            box=ui.box(zone='center1_12', order=1),
            title='',subtitle='',
            items=[
                ui.persona(title='LOG IN C4SSIA', subtitle='', caption='', size='l', image=yaainternet_logo),
                ui.textbox(name='username', label='Username', required=True),
                ui.textbox(name='password', label='Password', password=True, required=True),
                ui.button(name='login', label='Log In', primary=True),
        ])
        q.page['signInYI'] = ui.section_card(box=ui.box('der1_11', order=1), title='', subtitle = '', items = [ui.button(name='signin', label='Sign In', primary=True)])

    await q.page.save()

@app('/login', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await login(q)