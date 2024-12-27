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

async def paso1(q: Q):
    del q.page['upldCSV']
    del q.page['combotextboxes']
    del q.page['btnCSV2']
    del q.page['textdeinicio']

    q.page['textdeinicio'] = ui.section_card(box=ui.box('der1_10', order=1),title='',subtitle='',items=[ui.text_xl('Registro de Materiales de Construcción')],)
    q.page['menuBtns'] = ui.section_card(box=ui.box('der1_11', order=1),title='',subtitle='',
        items=[
            ui.button(name='btnRegis', label='Registro', disabled = False, primary=True),
            ui.button(name='btnCSV', label='CSV File', disabled = False, primary=True)
        ],
    )
    await q.page.save()

async def paso2(q: Q):
    global comboboxUnidadAdd
    
    del q.page['combotextboxes']
    del q.page['menuBtns']
    del q.page['upldCSV']
    del q.page['lista-ing-show']
    del q.page['textdeinicio']
    
    q.page['combotextboxes'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.textbox(name='textdescripcion', label='Descripción', value='', trigger=True),
            ui.textbox(name='textmodelo', label='Modelo', value='', trigger=True),
            ui.textbox(name='textmarca', label='Marca', value='', trigger=True),
            ui.combobox(name='combounidad', label='Unidad', value='Seleccionar', choices=comboboxUnidadAdd,trigger=True),
            ui.button(name='addMod', label='Agregar', disabled = False, primary=True,)
        ]
    )
    q.page['btnCSV2'] = ui.section_card(box=ui.box('der1_12',order=1),title='',subtitle='',items=[ui.button(name='btnCSV',label='CSV File',disabled=False,primary=False)])

    await q.page.save()
    await q.run(showList,q)

async def paso3(q: Q):
    del q.page['combotextboxes']
    del q.page['btnCSV2']
    del q.page['menuBtns']
    del q.page['lista-ing-show']
    del q.page['textdeinicio']

    q.page['upldCSV'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
            ui.button(name='btnRegis', label='Registro', disabled = False, primary=False,),
            ui.file_upload(name='file_upload',label='Upload!',multiple=False,compact=True,file_extensions=['csv'],max_file_size=10,max_size=15),
            ui.button(name='btnAddDevs', label='Agregar', disabled = False, primary=True,),
        ]
    )

    await q.page.save()
    await q.run(showList,q)

async def showList(q: Q):
    global data_rows

    q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.text_xl(content='Lista de artículos'),
        ui.table(
            name='issues',
            multiple = True,
            columns=columns3,
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

    q.page['boton2']=ui.section_card(box=ui.box('der1_22',order=1),title='',subtitle='',items=[ui.button(name='btnRegistrar',label='Registrar Material(es)',disabled=False,primary=True)])
    q.page['boton3']=ui.section_card(box=ui.box('der1_22',order=2),title='',subtitle='',items=[ui.button(name='btnDelete',label='Delete',disabled=False,primary=True)])

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
                await q.page.save()
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

async def addMats(q: Q):
    print(str("starting addMats..."))
    global ipGlobal, session, username
    global data_rows
    global marca, modelo, descripcion, unidad, data_rows_keycountMat
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

    if q.args.btnRegis:
        paso1P = 0
        paso2P = 1
        paso3P = 0
        bandPaso2 = 0
        await q.page.save()

    if q.args.btnCSV:
        paso1P = 0
        paso2P = 0
        paso3P = 1
        bandPaso3 = 0
        await q.page.save()

    if q.args.textmarca:
        marca = str(q.args.textmarca)
        await q.page.save()

    if q.args.textmodelo:
        modelo=str(q.args.textmodelo)
        await q.page.save()

    if q.args.textdescripcion:
        descripcion=str(q.args.textdescripcion)
        await q.page.save()

    if q.args.combounidad and str(q.args.combounidad) != 'Seleccionar':
        unidad = str(q.args.combounidad)
        await q.page.save()

    if q.args.addMod:
        if marca != '':
            if modelo != '':
                if descripcion != '':
                    if unidad != '':
                    	data_rows_keycountMat += 1
                    	data_rows.append([str(data_rows_keycountMat), marca, modelo, descripcion, unidad])
                    	marca, modelo, descripcion, unidad = '', '', '', ''
                    	await q.run(start_or_restart_paso1,q)
                    else:
                        q.page["meta"].side_panel = ui.side_panel(title="",name="side_panel",events=["dismissed"],closable=True,width = '400px',
                            items=[
                            	ui.text("Necesitas ingresar todos los datos correctamente.")
                            ],
                        )
        await q.page.save()

    if q.args.btnRegistrar:
        msg = []
        data_rows_temp, materialesMarca, materialesModelo, materialesDescripcion, materialesUnidad = [], '', '', '', ''
        seleccionated = q.args.issues
        if seleccionated == None or seleccionated == []:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un equipo(s) para registrarlo.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if seleccionated != None and seleccionated != []:
            if len(seleccionated) > 0:
                for y in data_rows:
                    for x in seleccionated:
                        if str(y[0])==str(x):
                            found=1
                            #si quieres quitar los que seleccionaste
                            materialesMarca = str(y[1])
                            materialesModelo = str(y[2])
                            materialesDescripcion = str(y[3])
                            materialesUnidad = str(y[4])
                            try:
                            	key_count=r.get('key_materiales')
                            	if key_count == None:
                            		key_count = 0
                            		r.set("key_materiales",str(key_count))
                            	else:
                            		key_count=key_count.decode("utf-8")
                            except Exception as e:
                            	print(e)
                            res = getAllMaterialesxMarca(r, materialesMarca, materialesModelo)
                            if res == 'NO':
                            	if key_count == None:
                            		key_count=1
                            	else:
                            		key_count=int(key_count)+1
                            	r.set("key_materiales",str(key_count))
                            	pp={"marca":str(materialesMarca),"modelo":str(materialesModelo),"descripcion":str(materialesDescripcion),"unidad":str(materialesUnidad)}
                            	r.hmset('materiales'+str(key_count), pp)
                    if found==0:
                        #si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found = 0
                data_rows = data_rows_temp
                if len(data_rows) == 0:
                	data_rows_keycountMat = 0
                paso1P = 1
                paso2P = 0
                paso3P = 0
                bandPaso1 = 0
        await q.run(showList, q)
        await q.page.save()

    if q.args.btnDelete:
        print(str("delete..."))
        eliminados = q.args.issues
        data_rows_temp, data_rows_send, found = [], [], 0
        if eliminados == None or eliminados == []:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un equipo(s) para eliminarlo de la lista de registro.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if eliminados != None and eliminados != []:
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
            bandPaso1 = 0
        await q.run(showList, q)
        await q.page.save()

    if q.args.btnAddDevs:
        file = q.args.file_upload
        if file:
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
                            data_rows_keycountMat += 1
                            data_rows.append([str(data_rows_keycountMat), row[1], row[2], row[3], row[4]])
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        await q.run(showList, q)
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
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
                            ui.zone('der1',size='100%', zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='25%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_10', size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_11', size='40%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', size='40%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='75%', direction=ui.ZoneDirection.ROW, zones=[
                                        ui.zone('der1_21', size='90%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_22', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
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
        await q.page.save()
        await q.run(start_or_restart_refresh,q)

@app('/addMats', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await addMats(q)