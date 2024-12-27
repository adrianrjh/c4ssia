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
            print(username)
        except Exception as e:
            print(e)

    def work2(self, item):
        global refreshDownloadRecep, rutaDoc
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            rutaDoc = data['rutaDoc']
            refreshDownloadRecep = 1
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
                    if (message['channel'].decode("utf-8")=="downloadFileRecep"):
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
                        self.pubsub.subscribe(['last_session', 'downloadFileRecep'])
                        break
            time.sleep(0.001)  # be nice to the system :)

client = Listener1(r, ['last_session'])
client.start()

########### P   A   S   O   1111111111111111111111 ###########
async def paso1(q: Q):
    global comboboxProyectos, data_rows, proyecto

    del q.page['lista']
    del q.page['menuBtns0']
    del q.page['menuBtns1']
    del q.page['menuBtns2']
    del q.page['btnAtras']
    del q.page['statDev1']
    del q.page['statDev2']
    del q.page['statDev3']
    del q.page['statDev4']
    del q.page['statDev5']
    del q.page['statDev6']
    del q.page['btnAtras1']
    del q.page['textboxNoSerie']
    del q.page['btnReport']

    proyecto = ''
    data_rows, comboboxProyectos = [], []
    data_rows = getAllPrsxStatus(r, 'Arrived')
    for x in range(0,len(data_rows)):
        comboboxProyectos.append(data_rows[x][0]+'/'+data_rows[x][1]+'/'+data_rows[x][3])

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_1', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    q.page['comboboxproyectos'] = ui.section_card(
        box=ui.box('izq1_3', order=1),
        title='',
        subtitle='',
        items=[ui.combobox(name='comboboxproyecto', label='Proyecto', value='Seleccionar', choices=comboboxProyectos,trigger=True)],
    )

    q.page['btnRecibir'] = ui.section_card(box=ui.box('izq1_4', order=1),title='',subtitle='',items=[ui.button(name='btnRecep', label='Recibir', disabled = False, primary=True)])

    await q.page.save()
########### P   A   S   O   2222222222222222222 ###########
async def paso2(q: Q):
    global proyecto, data_rowsPR, comboboxGaran, proyecto1, sumaIteDevs
    global dataaaa, counter
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4

    sumaIteDevs = 0
    del q.page['comboboxproyectos']
    del q.page['btnRecibir']
    del q.page['statDev1']
    del q.page['statDev2']
    del q.page['statDev3']
    del q.page['statDev4']
    del q.page['statDev5']
    del q.page['statDev6']
    del q.page['btnAtras1']
    del q.page['textboxNoSerie']
    del q.page['btnReport']
    del q.page['btnAtrasH']

    q.page['btnAtras'] = ui.section_card(box=ui.box('izq1_1', order=1),title='',subtitle='',items=[ui.button(name='btnAtras', label='Atrás', disabled = False, primary=True)])  

    proyecto1 = proyecto.split("/")
    data_rowsPR = getSinglePr(r, str(proyecto1[0]))
    dataaaa = getSinglePrAll2(r, str(proyecto1[0]))
    q.page['lista'] = ui.form_card(box=ui.box('mid1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columns,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rowsPR],
            #values = ['0'],
            groupable=False,
            downloadable=True,
            resettable=False,
        )
    ])

    #updAct(dataaaa, 'arrived')
    q.page['menuBtns0'] = ui.section_card(box=ui.box('izq1_4', order=1),title='',subtitle='',items=[ui.combobox(name='combogarantia', label='Garantia', value='Seleccionar', choices=comboboxGaran,trigger=True)])
    q.page['menuBtns1'] = ui.section_card(box=ui.box('mid1_12', order=1),title='',subtitle='',items=[ui.button(name='btnRegister', label='Dar de Alta en Almacen', disabled = False, primary=False)])
    q.page['menuBtns2'] = ui.section_card(box=ui.box('der1_14', order=1),title='',subtitle='',items=[ui.button(name='btnGaran', label='Aplicar Garantía', disabled = False, primary=True)])

    data_rows_lista = getSinglePrAll(r, proyecto1[0])
    counter = 0
    for x in range(0, len(data_rows_lista)):
        if str(data_rows_lista[x][9]) == str(data_rows_lista[x][5]):
            print('holaaaaa')
            counter += 1
            if len(data_rows_lista) == counter:
                paso1P = 0
                paso2P = 0
                paso3P = 0
                paso4P = 1
                bandPaso4 = 0

    await q.page.save()
########### P   A   S   O   33333333333333 ###########
async def paso3(q: Q):
    global deviceRecep, sumaIteDevs, noserie, comboboxMisc, r
    global data_rows_temp, proyecto1, paso1P, paso2P, paso3P, paso4P, bandPaso4, bandPaso2

    noserie = ''
    del q.page['btnAtras']
    del q.page['lista']
    del q.page['menuBtns0']
    del q.page['menuBtns1']
    del q.page['menuBtns2']
    del q.page['btnAtrasH']

    q.page['btnAtras1'] = ui.section_card(box=ui.box('izq1_1',order=1),title='',subtitle='',items=[ui.button(name='btnAtras1', label='Atrás', disabled = False, primary=True)])
    q.page['statDev1'] = ui.small_stat_card(box=ui.box('mid1_11', order=1),title='MARCA',value=f'{deviceRecep[0][2]}')
    q.page['statDev2'] = ui.small_stat_card(box=ui.box('mid1_11', order=2),title='MODELO',value=f'{deviceRecep[0][3]}')
    q.page['statDev3'] = ui.small_stat_card(box=ui.box('mid1_11', order=3),title='DESCRIPCION',value=f'{deviceRecep[0][4]}')
    q.page['statDev4'] = ui.small_stat_card(box=ui.box('mid1_11', order=4),title='CANTIDAD A RECIBIR',value=f'{deviceRecep[0][5]}')
    q.page['statDev5'] = ui.small_stat_card(box=ui.box('mid1_11', order=5),title='GARANTIA',value=f'{deviceRecep[0][6]}')
    q.page['textboxNoSerie'] = ui.section_card(
        box=ui.box('mid1_11', order=6),
        title='',subtitle='',
        items=[
            ui.textbox(name='textnoserie', label='N° de Serie',trigger=True),
            ui.combobox(name='combomisc',label='Tipo',value='Seleccionar',choices=comboboxMisc,trigger=True),
            ui.button(name='btnGenQR', label='Imprimir QR Label', disabled = False, primary=True),
        ]
    )

    q.page['statDev6'] = ui.small_stat_card(box=ui.box('mid1_11', order=7),title='Registrados',value=f'{sumaIteDevs}')

    if sumaIteDevs == int(deviceRecep[0][5]):
        proyecto1 = proyecto.split("/")
        data_rows_lista = getSinglePrAll(r, proyecto1[0])
        data_rows_temp1, data_rows_send1, found = [], [], 0
        for y in data_rows_lista:
            for x in data_rows_temp:
                if str(y[0][0])==str(x[0][0]):
                    # si quieres quitar los que seleccionaste
                    found=1
                    data_rows_send1.append(y)
            if found==0:
                # si quieres quitar los que no seleccionaste
                data_rows_temp1.append(y)
            found=0
        proyecto1 = proyecto1[0].split('-')
        #changeFieldTable(r,  data_rows_send1, proyecto1[1])
        if len(data_rows_send1) == 0:
            paso1P = 0
            paso2P = 0
            paso3P = 0
            paso4P = 1
            bandPaso4 = 0
        if len(data_rows_send1) != 0:
            paso1P = 0
            paso2P = 1
            paso3P = 0
            paso4P = 0
            bandPaso2 = 0
    await q.page.save()

########### P   A   S   O   44444444444444444 ###########
async def paso4(q: Q):
    global deviceRecep, sumaIteDevs, noserie, comboboxMisc, r
    global data_rows_temp, proyecto1, paso1P, paso2P, paso3P, bandPaso2

    del q.page['comboboxproyectos']
    del q.page['btnRecibir']
    del q.page['statDev1']
    del q.page['statDev2']
    del q.page['statDev3']
    del q.page['statDev4']
    del q.page['statDev5']
    del q.page['statDev6']
    del q.page['btnAtras1']
    del q.page['textboxNoSerie']
    del q.page['btnReport']
    del q.page['btnAtrasH']
    del q.page['btnAtras']
    del q.page['lista']
    del q.page['menuBtns0']
    del q.page['menuBtns1']
    del q.page['menuBtns2']

    q.page['btnReport'] = ui.section_card(box=ui.box('mid1_11', order=1),title='',subtitle='',items=[ui.button(name='btnEndRecep',label='Finalizar - Reporte', disabled=False, primary=True)])
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

async def sims_recepcion(q: Q):
    print(str("starting sims_recepcion..."))
    global username
    global data_rows, r, proyecto, proyecto1, session, data_rowsPR, deviceRecep, noserie, miscellaniuos
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    global garantia, sumaIteDevs, data_rows_temp, errno, data_to_report

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

    if q.args.comboboxproyecto:
        if q.args.comboboxproyecto != 'Seleccionar':
            proyecto = str(q.args.comboboxproyecto)
        await q.page.save()

    if q.args.combomisc:
        if q.args.combomisc != 'Seleccionar':
            miscellaniuos = str(q.args.combomisc)
        await q.page.save()

    if q.args.textnoserie:
        noserie=str(q.args.textnoserie)
        await q.page.save()

    if q.args.btnRecep:
        if proyecto != '':
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        else:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un proyecto.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
            await q.run(paso2,q)
        await q.page.save()

    if q.args.btnRegister:
        selectioned = q.args.issues
        if selectioned == None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un equipo(s) para dar de alta.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if selectioned != None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rowsPR:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            # si quieres quitar los que seleccionaste
                            found=1
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                deviceRecep = data_rows_send
                if int(deviceRecep[0][7]) >= 0:
                    if int(deviceRecep[0][5]) != int(deviceRecep[0][7]):
                        paso1P = 0
                        paso2P = 0
                        paso3P = 1
                        bandPaso3 = 0
                        sumaIteDevs = int(deviceRecep[0][7])
        await q.page.save()

    if q.args.btnAtras:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnAtras1:
        paso1P = 0
        paso2P = 1
        paso3P = 0
        bandPaso2 = 0
        await q.page.save()

#########   G   E   N   E   R   A   R       Q   R   ############
    if q.args.btnGenQR:
        if noserie != '':
            if miscellaniuos != '':
                if sumaIteDevs<int(deviceRecep[0][5]):
                    sumaIteDevs += 1
                    card1 = q.page['statDev6']
                    card1.value = str(sumaIteDevs)
                    key_count=r.get('key_alm')
                    if key_count == {}:
                        key_count = 0
                    else:
                        key_count=key_count.decode("utf-8")
                        key_count=int(key_count)+1
                    now = datetime.datetime.now()
                    dt_string = now.strftime("%Y%m%d")
                    fell = now.strftime("%Y-%m-%d %H:%M:%S")
                    proyecto1 = proyecto.split("/")
                    try:
                        counter_article = rts.get(str(deviceRecep[0][3]))
                    except Exception as e:
                        print(e)
                        errno = str(e)
                    try:
                        if errno == 'TSDB: the key does not exist':
                            rts.add(str(deviceRecep[0][3]), int(time.time()), int(1))
                            errno = ''
                        if int(counter_article[1]) > 0:
                            updtArt = int(counter_article[1])+1
                            rts.add(str(deviceRecep[0][3]), int(time.time()), int(updtArt))
                    except Exception as e:
                        print(e)
                    #########   NOPR             PROYECTO          MARCA                    MODELO                    DESCRIPCION             NOSERIE     FECHA LLEGADA 
                    qr_code = proyecto1[0]+'/'+proyecto1[1]+'/'+deviceRecep[0][2]+'/'+deviceRecep[0][3]+'/'+deviceRecep[0][4]+'/'+noserie+'/'+dt_string
                    devToAlm(r, key_count, fell, proyecto1[0], proyecto1[1], deviceRecep[0][2], deviceRecep[0][3], deviceRecep[0][4], deviceRecep[0][6], noserie, qr_code, miscellaniuos)
                    data_to_report.append([fell, proyecto1[0], proyecto1[1], deviceRecep[0][2], deviceRecep[0][3], deviceRecep[0][4], deviceRecep[0][6], noserie, qr_code, miscellaniuos])
                    ########## P    R   I   N   T        Q  R       C   O   D   E ############
                    import qrcode
                    from PIL import Image
                    import os
                    # Obtener la ruta del directorio de Documentos para macOS y Linux
                    documentos_path = os.path.join(os.path.expanduser('~'))
                    nueva_carpeta_path = os.path.join(documentos_path, 'QR_CODES')
                    documentos_path = os.path.join(os.path.expanduser('~'), 'QR_CODES/')
                    os.makedirs(nueva_carpeta_path, exist_ok=True)
                    # Generar QR
                    input_data = str(qr_code)
                    qr = qrcode.QRCode(
                        version=1,
                        box_size=10,
                        border=5)
                    qr.add_data(input_data)
                    qr.make(fit=True)
                    img = qr.make_image(fill='black', back_color='white')
                    img.save(documentos_path+'qr_code.png')
                    import cups
                    # Conectar con CUPS
                    conn = cups.Connection()
                    # Obtener la lista de impresoras
                    printers = conn.getPrinters()
                    # Nombre de la impresora configurada en CUPS
                    printer_name = '4BARCODE_3B-365B'
                    # Imprimir la imagen
                    conn.printFile(printer_name, documentos_path+'qr_code.png', "QR Code Print", {})
                    conn.printFile(printer_name, documentos_path+'qr_code.png', "QR Code Print", {})
                    paso1P = 0
                    paso2P = 0
                    paso3P = 1
                    bandPaso3 = 0
                    if sumaIteDevs <= int(deviceRecep[0][5]):
                        if len(proyecto1) > 2:
                            data_rows_lista = getSinglePrAll(r, proyecto1[0])
                            data_rowsPR1, data_rows_temp1, data_rows_send1, found = [], [], [], 0
                            for y in data_rows_lista:
                                for x in data_rows_temp:
                                    if str(y[0][0])==str(x[0][0]):
                                        # si quieres quitar los que seleccionaste
                                        found=1
                                        data_rowsPR1.append(y)
                                if found==0:
                                    # si quieres quitar los que no seleccionaste
                                    y[9] = str(sumaIteDevs)
                                    data_rowsPR1.append(y)
                                found=0
                            proyecto1 = proyecto1[0].split('-')
                            changeFieldTable(r,  data_rowsPR1, proyecto1[1])
        else:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Ingresa el número de serie del equipo.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        await q.page.save()

    if q.args.combogarantia:
        if q.args.combogarantia != 'Seleccionar':
            garantia = str(q.args.combogarantia)
        await q.page.save()
#########   G   A   R   A   N   T   I   A       U   P   D   A   T   E   ############
    if q.args.btnGaran:
        selectioned = q.args.issues
        data_rowsPR = []
        if selectioned == None:
            pass
        if selectioned != None:
            if len(selectioned) == 1:
                if garantia != '':
                    proyecto1 = proyecto.split("/")
                    data_rowsPRFor = getSinglePrAll(r, str(proyecto1[0]))
                    data_rows_temp, data_rows_send, found = [], [], 0
                    for y in data_rowsPRFor:
                        for x in selectioned:
                            if str(y[0])==str(x):
                                # si quieres quitar los que seleccionaste
                                found=1
                                y[7] = garantia
                                data_rowsPR.append(y)
                                data_rows_send.append(y)
                        if found==0:
                            # si quieres quitar los que no seleccionaste
                            data_rowsPR.append(y)
                            data_rows_temp.append(y)
                        found=0
                    proyecto1 = proyecto1[0].split('-')
                    changeFieldTable(r,  data_rowsPR, proyecto1[1])
                    paso1P = 0
                    paso2P = 1
                    paso3P = 0
                    bandPaso2 = 0
                else:
                    q.page["meta"].side_panel = ui.side_panel(
                        title="",
                        items=[ui.text("Ingresa la garantia se le aplicará al equipo.")],
                        name="side_panel",
                        events=["dismissed"],
                        closable=True,
                        width = '400px',
                    )
        await q.page.save()

    if q.args.btnEndRecep:
        res = getSinglePrAll2(r, proyecto1[0])
        data_user = getUser('user_key', 'user_',username)
        json_datos={
            "proyecto": str(res['proyecto']),
            'encargado':str(res['encargado']),
            'noPR':str(res['noPR']),
            'fecha':str(res['fecha']),
            'totalPR':str(res['totalPR']),
            'fullname':str(data_user[0]),
            'puesto':str(data_user[1]),
            'lista':data_to_report
        }
        try:
            r.publish("yi_pdfs_recepcion",json.dumps(json_datos))
            time.sleep(0.3)
        except Exception as e:
            print(e)
        paso1P = 1
        paso2P = 0
        paso3P = 0
        bandPaso1 = 0
        data_to_report = []
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
            await q.run(paso2,q)
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
                    ui.zone('body',size='93%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq', size='12%', zones=[
                            ui.zone('izq1_1', align='start', size='12%', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_2', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_3', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_4', align='start', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_5', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_6', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_7', align='center', size='12%', direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_8', align='center', size='16%', direction=ui.ZoneDirection.ROW)
                        ]),
                        ui.zone('mid',size='76%',direction=ui.ZoneDirection.COLUMN, zones=[
                            ui.zone('mid1_11', align='center', size='80%', direction=ui.ZoneDirection.ROW),
                            ui.zone('mid1_12', align='center', size='20%', direction=ui.ZoneDirection.COLUMN),
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

@app('/sims_recepcion', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await sims_recepcion(q)
