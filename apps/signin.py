from h2o_wave import Q, app, main, ui, AsyncSite,site,data
#from pyzabbix import ZabbixAPI
import threading,json,time,math
from datetime import datetime
import sys
from redis import StrictRedis, ConnectionError
from redistimeseries.client import Client
import random, json, time, datetime
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common0 import *

async def createAccount(q: Q):
    global var_ca
    if var_ca == 1:
        var_ca = 0
        del q.page['createYI1']
        del q.page['logInYI']
        yaainternet_logo = 'http://'+ipGlobal+':10101/datasets/yaainternet.png'
        q.page['createYI'] = ui.form_card(
            box=ui.box(zone='center1_12', order=1),
            items=[
                ui.persona(title='CREATE ACCOUNT C4SSIA', subtitle='', caption='', size='l', image=yaainternet_logo),
                ui.textbox(name='name', label='Name', required=True),
                ui.textbox(name='lastname', label='Last Name', required=True),
                ui.combobox(name='textpuesto', label='Puesto', value='Seleccionar', choices=['Soporte Técnico', 'Administrador', 'Desarrollador', 'Monitorista', 'Almacenista', 'Arquitecto', 'Tecnico Instalador'],trigger=True),
                ui.textbox(name='email', label='Email', required=True),
                ui.textbox(name='username', label='Username', required=True),
                ui.textbox(name='password', label='Password', password=True, required=True),
                ui.textbox(name='password1', label='Confirm Password', password=True, required=True),
                ui.button(name='signin', label='Create', primary=True),
        ])
        q.page['logInYI'] = ui.section_card(box=ui.box('der1_11', order=1), title='', subtitle = '', items = [ui.button(name='login', label='Log In', primary=True)])

    await q.page.save()

async def signin(q: Q):
    global session, name, lastname, puesto, email, username, password, password1, var_ca
    print("Start aplication signin...")

    if q.args.name:
        name=str(q.args.name)
        await q.page.save()

    if q.args.lastname:
        lastname=str(q.args.lastname)
        await q.page.save()

    if q.args.textpuesto:
        if q.args.textpuesto != 'Seleccionar':
            puesto = str(q.args.textpuesto)
        await q.page.save()

    if q.args.email:
        email=str(q.args.email)
        await q.page.save()

    if q.args.username:
        username=str(q.args.username)
        await q.page.save()

    if q.args.password:
        password=str(q.args.password)
        await q.page.save()

    if q.args.password1:
        password1=str(q.args.password1)
        await q.page.save()

    if q.args.login:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.caacount:
        var_ca = 1
        await q.run(createAccount,q)
        await q.page.save()

    if q.args.signin:
        if name != '':
            if lastname != '':
                if puesto != 'Seleccionar':
                    if email != '':
                        if username != '':
                            if password != '':
                                if password == password1:
                                    key_count=r.get('user_key')
                                    if key_count == {}:
                                        key_count = 0
                                    else:
                                        key_count=key_count.decode("utf-8")
                                        key_count=int(key_count)+1
                                    now = datetime.datetime.now()
                                    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                                    pp={"time":str(dt_string),"user_key":str(key_count),"name":str(name),"lastname":str(lastname),"puesto":str(puesto),"email":str(email),'status':'Waiting',"username":str(username),"password":str(password)}
                                    try:
                                        regAct(key_count,pp)
                                        time.sleep(2)
                                        del q.page['createYI']
                                        yaainternet_logo = 'http://'+ipGlobal+':10101/datasets/yaainternet.png'
                                        checkRight = 'http://'+ipGlobal+':10101/datasets/checkRight.png'
                                        q.page['createYI1'] = ui.form_card(
                                            box=ui.box(zone='center1_12', order=1),
                                            items=[
                                                ui.persona(title='CREATE ACCOUNT C4SSIA', subtitle='', caption='', size='l', image=yaainternet_logo),
                                                ui.button(name='caacount', label='Create another account', primary=True),
                                                ui.persona(title='Account Created!', subtitle='', caption='', size='s', image=checkRight),
                                        ])
                                    except Exception as e:
                                        print(e)
        await q.page.save()

    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
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
                        ui.zone('cen1',size='33%', zones=[
                            ui.zone('center1_11',size='15%',align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('center1_12',size='70%',align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('center1_13',size='15%',align='center',direction=ui.ZoneDirection.COLUMN),
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
        var_ca = 1
    await q.run(createAccount, q)
    await q.page.save()

@app('/signin', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await signin(q)