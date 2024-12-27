from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from funcApp import *
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

########### P   A   S   O   11111111111111111 ###########
async def paso1(q: Q):
    global data_rows

    del q.page['btnAtrasH']
    del q.page['textQrCodeScrap']
    del q.page['btnFinScrap']
    del q.page['btnEliminar']
    del q.page['table']
    del q.page['checkRight']
    del q.page['btnPDF']

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    q.page['textQrCodeScrap'] = ui.section_card(
        box=ui.box('mid1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.textbox(name='textqrcode', label='QR CODE',trigger=True),
            ui.button(name='btnAgregar', label='Agregar', disabled = False, primary=True)
        ],
    )

    q.page['btnFinScrap'] = ui.section_card(box=ui.box('der1_11', order=1),title='',subtitle='',items=[ui.button(name='btnFinScrap', label='Finalizar Scrap', disabled = False, primary=True)])
    q.page['btnEliminar'] = ui.section_card(box=ui.box('mid1_13', order=1),title='',subtitle='',items=[ui.button(name='btnDelete', label='Eliminar Articulo', disabled = False, primary=True)])

    await q.page.save()

########### P   A   S   O   222222222222222222 ###########
async def paso2(q: Q):
    global data_rows
    
    del q.page['btnAtrasH']
    del q.page['comboboxproyectos']
    del q.page['textQrCodeScrap']
    del q.page['btnFinScrap']
    del q.page['btnEliminar']
    del q.page['table']

    #########   a  c  t  i  v  e   #########
    checkRight_logo = 'http://'+ipGlobal+':10101/datasets/checkRight1.png'
    q.page['checkRight'] = ui.section_card(box=ui.box(zone='mid1_12', order=1),title='',subtitle='',items=[ui.persona(name="btnScrapTermi",title='Scrap Terminada', subtitle='', caption='', size='xl', image=checkRight_logo)])
    q.page['btnPDF'] = ui.section_card(box=ui.box('mid1_12', order=2),title='',subtitle='',items=[ui.button(name='btnPDF', label='Descargar PDF', disabled = False, primary=True)])

    await q.page.save()

async def showList(q: Q):
    global data_rows, columnsAsig
    try:
        q.page['table'] = ui.form_card(box=ui.box('mid1_12', order=1), items=[
            ui.table(
                name='issues',
                multiple = True,
                columns=columnsAsig,
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
    except asyncio.CancelledError:
        print("La tarea 'showList' fue cancelada")
        return

async def refresh(q: Q):
    global paso1P, paso2P, bandPaso1, bandPaso2

    try:
        while 1:
            if paso1P == 1 and bandPaso1 == 0:
                bandPaso1 = 1
                await q.run(paso1,q)
                await q.run(start_or_restart_refresh1,q)
                await q.page.save()
            if paso2P == 1 and bandPaso2 == 0:
                bandPaso2 = 1
                await q.run(paso2,q)
                await q.page.save()
            await q.sleep(1)
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

async def start_or_restart_refresh1(q: Q):
    global current_showlist_task
    # Cancela la tarea anterior si existe y aún está corriendo
    if current_showlist_task and not current_showlist_task.done():
        current_showlist_task.cancel()
        try:
            # Espera a que la tarea sea cancelada (opcional)
            await current_showlist_task
        except asyncio.CancelledError:
            # Maneja el caso en que la tarea fue cancelada
            pass
    # Inicia una nueva tarea
    current_showlist_task = asyncio.create_task(showList(q))

async def sims_scrap(q: Q):
    print(str("starting sims_scrap..."))
    global data_rows, data_rows_keycount, r,  session
    global paso1P, paso2P, bandPaso1, bandPaso2
    global trabajador, qr_code, noserie, proyecto, marcaDev, modeloDev, descripcion, garantia, ubicacion, status

    q.page['meta'] = ui.meta_card(box='')

    if q.args.home:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.settings:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/settings'
        await q.page.save()

    if q.args.logout:
        session = False
        puesto = ''
        json_datos = json.dumps({"session":session, "user":puesto})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAtrasH:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_sims'
        await q.page.save()
    
    if q.args.textqrcode:
        qr_code = str(q.args.textqrcode)
        await q.page.save()
    
    if q.args.comboboxusers:
        if q.args.comboboxusers != 'Seleccionar':
            trabajador = str(q.args.comboboxusers)
        await q.page.save()

    if q.args.btnDevolver:
        if trabajador != '':
            paso1P = 1
            paso2P = 0
            bandPaso1 = 0
            await q.run(start_or_restart_refresh1,q)
        await q.page.save()

    if q.args.btnAgregar:
        if qr_code != '':
            data_rows_keycount = 0
            data_rows2 = []
            if len(data_rows)>0:
                for x in range(0,len(data_rows)):
                    data_rows_keycount += 1
                    data_rows[x][0] = data_rows_keycount
                    data_rows2.append([str(data_rows[x][0]), data_rows[x][1], data_rows[x][2], data_rows[x][3], data_rows[x][4], data_rows[x][5], data_rows[x][6], data_rows[x][7], data_rows[x][8]])
            data_rows = data_rows2
            qr_code = qr_code.replace("-", "/")
            qr_code = qr_code.replace("'", "-")
            res = getSingleArticle(r, qr_code)
            try:
                if res != None:
                    data_rows_keycount += 1
                    noserie = res['noserie']
                    proyecto = res['proyecto']
                    marcaDev = res['marca']
                    modeloDev = res['modelo']
                    descripcion = res['descripcion']
                    garantia = res['garantia']
                    ubicacion = res['ubicacion']
                    status = res['status']
                    data_rows.append([str(data_rows_keycount), noserie, proyecto, marcaDev, modeloDev, descripcion, garantia, ubicacion,status])
                else:
                    qr_code = ''
                    q.page["meta"].side_panel = ui.side_panel(
                        title="",
                        items=[ui.text("Articulo inexistente.")],
                        name="side_panel",
                        events=["dismissed"],
                        closable=True,
                        width = '400px',
                    )
            except Exception as e:
                print(e)
        paso1P = 1
        paso2P = 0
        bandPaso1 = 0
        await q.run(start_or_restart_refresh1,q)
        await q.page.save()

    if q.args.btnDelete:
        eliminados = q.args.issues
        if eliminados == None:
            pass
        #if eliminados != []:
        if eliminados != None:
            data_rows_temp, data_rows_send, found = [], [], 0
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
        await q.run(start_or_restart_refresh1,q)
        await q.page.save()

    if q.args.btnFinScrap:
        selectioned = q.args.issues
        if selectioned == None:
            pass
        if selectioned != []:
            if selectioned != None:
                print(selectioned)
                if len(selectioned) == len(data_rows):
                    changeStateArticle(data_rows, trabajador, 'scrap')
                    paso1P = 0
                    paso2P = 1
                    bandPaso2 = 0
                    data_rows = []
        await q.page.save()

    if q.args.btnScrapTermi:
        paso1P = 1
        paso2P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnPDF:
        pass
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
                    ui.zone('body',size='93%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq', size='12%', zones=[
                            ui.zone('izq1_11', align='start', size='12%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_12', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_13', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_14', align='start', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_15', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_16', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_17', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_18', align='center', size='16%', direction=ui.ZoneDirection.ROW)
                        ]),
                        ui.zone('mid',size='76%',direction=ui.ZoneDirection.COLUMN, zones=[
                            ui.zone('mid1_11', align='center', size='20%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('mid1_12', align='center', size='60%', direction=ui.ZoneDirection.ROW),
                            ui.zone('mid1_13', align='center', size='20%', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der', size='12%',direction=ui.ZoneDirection.COLUMN, zones=[
                            ui.zone('der1_11',align='center',size='12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('der1_12',align='center',size='12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('der1_13',align='start',size='12%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_14',align='start',size='12%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_15',align='center',size='12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('der1_16',align='center',size='12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('der1_17',align='center',size='12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('der1_18',align='center',size='16%',direction=ui.ZoneDirection.ROW)
                        ]),
                    ]),
                ]),
                ],
            ),
        ], theme='winter-is-coming')

        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_maps'] = ui.header_card(
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

        await q.page.save()
        await q.run(start_or_restart_refresh,q)

@app('/sims_scrap', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await sims_scrap(q)
