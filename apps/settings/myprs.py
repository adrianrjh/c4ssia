from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys, os
import random, webbrowser
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common8 import *
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

    def work2(self, item):
        global refreshDownload, rutaDoc
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            rutaDoc = data['rutaDoc']
            refreshDownload= 1
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
                    if (message['channel'].decode("utf-8")=="downloadFile"):
                        self.work2(message['data'])
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
                        self.pubsub.subscribe(['last_session'],['downloadFile'])
                        break
            time.sleep(0.001)  # be nice to the system :)

client = Listener1(r, ['last_session','downloadFile'])
client.start()

async def paso1(q: Q):
    global data_rows, columnsPRs
    
    del q.page['boton3']
    del q.page['table2']

    q.page['table'] = ui.form_card(box=ui.box('cen1_11', order=1), items=[
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

async def paso2(q: Q):
    global data_rows2, columns2
    del q.page['states1']
    q.page['table2'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
        ui.table(
            name='issues2',
            multiple = True,
            columns=columns2,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows2],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        )
    ])

    q.page['boton3'] = ui.section_card(
        box=ui.box('der1_12', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='btnLinkCompra', label='Link de Compra', disabled = False, primary=True,)
        ],
    )

    await q.page.save()

async def downloadFile(q: Q):
    global rutaDoc

    del q.page['boton2']
    q.page['boton2'] = ui.section_card(
        box=ui.box('izq1_12', order=1),
        title='',
        subtitle='',
        items=[
            ui.button(name='btnUpd', label='Update Table', disabled = False, primary=True,),
            ui.button(name='btnSeePR', label='See PR', disabled = False, primary=False),
            ui.button(name='btnSignPR', label='Sign PR', disabled = False, primary=False),
            ui.button(name='btnPDF', label='PDF', disabled = False, primary=True,),
            ui.button(name='btnDownload', label='Descargar archivo', disabled = False, primary=True,),
            ui.button(name='btnCancel', label='Cancel', disabled = False, primary=False),
        ],
    )

    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, bandPaso1, bandPaso2, bandPaso3, refreshDownload
    try:
        while 1:
            if refreshDownload == 1:
                refreshDownload = 0
                await q.run(downloadFile,q)
            if paso1P == 1 and bandPaso1 == 0:
                bandPaso1 = 1
                await q.run(paso1,q)
            if paso2P == 1 and bandPaso2 == 0:
                bandPaso2 = 1
                await q.run(paso2,q)
            if paso3P == 1 and bandPaso3 == 0:
                bandPaso3 = 1
                await q.run(paso3,q)
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
async def myprs(q: Q):
    print(str("starting myprs app..."))
    global ipGlobal,session, r
    global data_rows, data_rows2, proyecto, descripcion, cantidad, costo, garantia, total, linkcompra, encargado, totalPR, username
    global rutaDoc

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

#########   U   P   D   A   T   E     T   A   B   L   E   ############
    if q.args.btnUpd:
        data_rows = getAllPrsxUser(r, username)
        if data_rows == 'NO':
            data_rows = []
        elif len(data_rows) > 0:
            q.page['boton2'].items[0].button.disabled = False
            q.page['boton2'].items[1].button.disabled = False
            q.page['boton2'].items[2].button.disabled = False
            q.page['boton2'].items[3].button.disabled = False

        await q.run(paso1, q)
        await q.page.save()
#########   S   E   E       P   R   ############
    if q.args.btnSeePR:
        selectioned = q.args.issues
        data_rows_temp, data_rows_send, found = [], [], 0
        if selectioned == None:
            pass
        if selectioned != None:
            if len(selectioned) == 1:
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                idpr = data_rows_send[0][0]
                data_rows2 = getSinglePr(r, username, idpr)
                data_rows2 = json.loads(data_rows2["lista"])
                await q.run(paso2, q)
        await q.page.save()
#########    S    I   G   N       P   R   ############
    if q.args.btnCheckPR:
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
                    if data_rows_send[i][5] == 'Active':
                        updAct(data_rows_send, 'checked')
                        data_rows = getAllPrsxUser(r, username)
                    else:
                        q.page["meta"].side_panel = ui.side_panel(
                            title="",
                            items=[ui.text("La PR ya ha sido checkeda anteriormente.")],
                            name="side_panel",
                            events=["dismissed"],
                            closable=True,
                            width = '400px',
                        )
                await q.run(paso1, q)
        await q.page.save()
#########   G   E   N   E   R   A   T   E       P    D   F        P   R   ############
    if q.args.btnPDF:
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
                if data_rows_send[0][5] != 'Active' and data_rows_send[0][5] != 'Checked':
                    idpr = data_rows_send[0][0]
                    data_pr = getSinglePr(r, username, idpr)
                    now = datetime.datetime.now()
                    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                    json_datos = json.dumps(data_pr)
                    try:
                        r.publish("yi_pdfs_prs",json_datos)
                        time.sleep(0.3)
                    except Exception as e:
                        print(e)
                else:
                    q.page["meta"].side_panel = ui.side_panel(
                        title="",
                        items=[ui.text("Para poder generar el PDF se necesita estar autorizado y firmado por el creador de la PR.")],
                        name="side_panel",
                        events=["dismissed"],
                        closable=True,
                        width = '400px',
                    )
                await q.run(paso1, q)
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
                rutaDoc1 = rutaDoc.split("/")
                rutaDoc2 = rutaDoc1[10].split(".")
                if data_rows_send[0][0] == rutaDoc2[0]:
                    # Recuperar el PDF codificado en base64 desde Redis
                    pdf_base64 = r.get(rutaDoc2[0])
                    # Decodificar el PDF desde base64
                    pdf_data = base64.b64decode(pdf_base64)
                    # Escribir el PDF decodificado a un nuevo archivo
                    with open(rutaDoc, 'wb') as file:
                        file.write(pdf_data)
                    annotations_path, = await q.site.upload([rutaDoc])
                    webbrowser.open_new_tab(ipGlobal+':10101'+annotations_path)
                    #q.page['meta'].redirect = annotations_path
                else:
                    pass
        await q.run(paso1, q)
        await q.page.save()

#########    D   E   L   E   T   E       P   R   ############
    if q.args.btnCancel:
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
                    if data_rows_send[i][5] == 'Active':
                        updAct(data_rows_send, 'cancel')
                        data_rows = getAllPrsxUser(r, username)
                await q.run(paso1, q)
        await q.page.save()

    if q.args.btnLinkCompra:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues2
        if selectioned != [] and str(selectioned) != "['0']":
            found = 0
            for y in data_rows2:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0
            a_website = selectioned[10]
            # Open url in a new page (“tab”) of the default browser, if possible
            webbrowser.open_new_tab(a_website)
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
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq',size='5%', zones=[
                                ui.zone('izq1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('izq1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('izq1_11', size='10%', align='start', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                            ui.zone('cen',size='47%', zones=[
                                ui.zone('cen1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('cen1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('cen1_11', size='90%', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('cen1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                            ui.zone('der',size='48%', zones=[
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
            box=ui.box('cen1_12', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnUpd', label='Update', disabled = False, primary=True,),
                ui.button(name='btnSeePR', label='See', disabled = False, primary=False),
                ui.button(name='btnCheckPR', label='Check', disabled = False, primary=False),
                ui.button(name='btnPDF', label='PDF', disabled = False, primary=True,),
                ui.button(name='btnCancel', label='Cancel', disabled = False, primary=False),
            ],
        )

        q.page['states1'] = ui.tall_stats_card(
            box=ui.box('der1_11', order=1),
            items=[
                ui.stat(label='Data not found', value=str("")),
            ]
        )
        
        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='', icon='Back')])
        
        await q.page.save()
        data_rows = getAllPrsxUser(r, username)
        await q.run(paso1,q)
        await q.run(start_or_restart_refresh,q)

@app('/myprs', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await myprs(q)