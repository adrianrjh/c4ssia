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
from PIL import Image
import base64
from io import BytesIO
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
        global data_rows, refreshTable, data_rows_save, r
        global noticketPaP, tiempoPaP, proyectoPaP, postePaP, asignadoPaP, prioridadPaP, problemaPaP, statusPaP
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            noticketPaP = str(data['noticket'])
            tiempoPaP = str(data['time'])
            proyectoPaP = str(data['proyecto'])
            postePaP = str(data['poste'])
            asignadoPaP = str(data['asignado'])
            prioridadPaP = str(data['prioridad'])
            problemaPaP = str(data['problema'])
            statusPaP = str(data['status'])
            data_rows.append([noticketPaP, tiempoPaP, proyectoPaP, postePaP, asignadoPaP, prioridadPaP, problemaPaP, statusPaP])
            #updAct(data, 0)
            refreshTable = 1
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
                    if (message['channel'].decode("utf-8")=="pap_tickets"):
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
                        self.pubsub.subscribe(['last_session'],['pap_tickets'])
                        break
            time.sleep(0.001)  # be nice to the system :)

client = Listener1(r, ['last_session','pap_tickets'])
client.start()

async def showList(q: Q):
    global data_rows, columnsTicketsPaP, trabajadorAsignado

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='', disabled = False, primary=True, icon='ChromeBack')])

    trabajadorAsignado = ''
    users = getAllUsers(r, 'user_key', 'user_')
    comboboxUsers = []
    for x in range(0,len(users)):
        comboboxUsers.append(users[x][2]+' '+users[x][3]+'/'+users[x][7])
    q.page['comboboxproyectos']=ui.section_card(box=ui.box('der1_10',order=1),title='',subtitle='',items=[ui.combobox(name='comboboxusers',label='Trabajador',value='Seleccionar',choices=comboboxUsers,trigger=True)])
    q.page['btnAsignar']=ui.section_card(box=ui.box('der1_11',order=1),title='',subtitle='',items=[ui.button(name='btnAsignar',label='Asignar',disabled=False,primary=True)])
    q.page['table']=ui.form_card(box=ui.box('mid1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columnsTicketsPaP,
            rows=[ui.table_row(name=str(dato[0]),cells=dato,)for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        )
    ])

    await q.page.save()

async def refresh(q: Q):
    global refreshTable
    try:
        while 1:
            if refreshTable == 1:
                refreshTable = 0
                await q.run(showList,q)
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global refreshTable
    refreshTable = 1
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

async def pap_manage(q: Q):
    print(str("starting pap_manage app..."))
    global ipGlobal,session, r
    global data_rows
    global noticketPaP, tiempoPaP, proyectoPaP, postePaP, prioridadPaP, problemaPaP, statusPaP, trabajadorAsignado, textSolucionTicket, solutionTicket
    global refreshTable

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
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_pap'
        await q.page.save()
    
    if 'comboboxusers' in q.args:
        if q.args.comboboxusers and trabajadorAsignado!=str(q.args.comboboxusers):
            trabajadorAsignado = str(q.args.comboboxusers)
        await q.page.save()

######### A   S   I   G   N   A   R ############
    if q.args.btnAsignar:
        eliminados = q.args.issues
        if eliminados == None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona primero al trabajador y posteriormente el ticket a asignar.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if eliminados != None:
            if len(eliminados) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in eliminados:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            data_rows_send.append(y)
                    if found==0:
                        pass
                        # si quieres quitar los que no seleccionaste
                        #data_rows_temp.append(y)
                    found=0
                if trabajadorAsignado != 'None' and trabajadorAsignado != '' and trabajadorAsignado != 'Seleccionar':
                    if data_rows_send[0][7] == "Active" or data_rows_send[0][7] == "Asigned":
                        noticketSearch = str(data_rows_send[0][0])
                        proyectoSearch = str(data_rows_send[0][2])
                        posteSearch = str(data_rows_send[0][3])
                        updActPaP(r, noticketSearch, proyectoSearch, posteSearch, trabajadorAsignado, 'asigned', '', '')
                else:
                    q.page["meta"].side_panel = ui.side_panel(
                        title="",
                        items=[ui.text("Selecciona al trabajador para asignar el ticket.")],
                        name="side_panel",
                        events=["dismissed"],
                        closable=True,
                        width = '400px',
                    )
                data_rows = getAllTickets(r, 'key_tickets_obra', 'tickets_obra', 'yi_obra')
                refreshTable = 1
        await q.page.save()

######### W    O   R   K   I   N   G       O   N       I   T ############
    if q.args.btnWOI:
        eliminados = q.args.issues
        if len(eliminados) == 1:
            data_rows_temp, data_rows_send, found = [], [], 0
            for y in data_rows:
                for x in eliminados:
                    if str(y[0])==str(x):
                        found=1
                        # si quieres quitar los que seleccionaste
                        data_rows_send.append(y)
                if found==0:
                    pass
                    # si quieres quitar los que no seleccionaste
                    #data_rows_temp.append(y)
                found=0
            if data_rows_send[0][7] == "Asigned":
                noticketSearch = str(data_rows_send[0][0])
                proyectoSearch = str(data_rows_send[0][2])
                posteSearch = str(data_rows_send[0][3])
                trabajadorAsignado = str(data_rows_send[0][4])
                updActPaP(r, noticketSearch, proyectoSearch, posteSearch, trabajadorAsignado, 'in process', '', '')
            else:
                q.page["meta"].side_panel = ui.side_panel(
                    title="",
                    items=[ui.text("Para poder ejecutar esta accionar, primero tienes que asignar este ticket a un trabajador.")],
                    name="side_panel",
                    events=["dismissed"],
                    closable=True,
                    width = '400px',
                )
            data_rows = getAllTickets(r, 'key_tickets_obra', 'tickets_obra', 'yi_obra')
            refreshTable = 1
        await q.page.save()
######### F    I   N   I   S   H       I   T ############
    if q.args.btnFI:
        eliminados = q.args.issues
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
            found=0
        data_rows = data_rows_temp
        for i in range(0,len(data_rows_send)):
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            json_datos = json.dumps({
                "ticket_key":str(data_rows_send[i][0]),
                "area":"done",
                "time":str(data_rows_send[i][2]),
                "id":"tickets",
                "cliente":str(data_rows_send[i][3]),
                "contacto":str(data_rows_send[i][4]),
                "servicio":str(data_rows_send[i][5]),
                "problema":str(data_rows_send[i][6]),
                "status":"Done",
                "asignado":str(dt_string),
                "descripcion":str(data_rows_send[i][9]),                
            })
            try:
                r.publish("tickets_done",json_datos)
                time.sleep(0.3)
            except Exception as e:
                print(e)
            refreshTable = 1
        await q.page.save()
######### S   E   N   D   T O    E  X  C     ############
    if q.args.btnDptoExcptns:
        eliminados = q.args.issues
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
            found=0
        data_rows = data_rows_temp
        for i in range(0,len(data_rows_send)):
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            json_datos = json.dumps({
                "ticket_key":str(data_rows_send[i][0]),
                "area":"exceptions",
                "time":str(data_rows_send[i][2]),
                "id":"tickets",
                "cliente":str(data_rows_send[i][3]),
                "contacto":str(data_rows_send[i][4]),
                "servicio":str(data_rows_send[i][5]),
                "problema":str(data_rows_send[i][6]),
                "status":"Done",
                "asignado":str(dt_string),
                "descripcion":str(data_rows_send[i][9]),                
            })
            try:
                r.publish("tickets_exception",json_datos)
                time.sleep(0.3)
            except Exception as e:
                print(e)
            refreshTable = 1
        await q.page.save()

    if q.args.btnEvidence1:
        del q.page['upldSolu']
        del q.page['form_problema']
        del q.page['Img']
        ticket_info = []
        selectioned = q.args.issues
        if selectioned == None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un ticket.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if selectioned != None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            # si quieres quitar los que seleccionaste
                            found=1
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                noticketSearch = str(data_rows_send[0][0])
                proyectoSearch = str(data_rows_send[0][2])
                posteSearch = str(data_rows_send[0][3])
                ticket_info = getTicketPaP(r, noticketSearch, proyectoSearch, posteSearch)
                if ticket_info and len(ticket_info) > 0 and ticket_info[0][7]:
                    image_data = base64.b64decode(ticket_info[0][7])
                    image = Image.open(BytesIO(image_data))
                    routeEvidencia1 = '/home/adrian/ws/h2o-wave/home/data/'+noticketSearch+'_evidence.png'
                    image.save(routeEvidencia1)  # Asegúrate de especificar la ruta correcta
                    routeEvidencia1 = await q.site.download(routeEvidencia1, '../../data/')
                    routeEvidencia1 = routeEvidencia1.split('/')
                    q.page['form_problema'] = ui.section_card(box=ui.box('mid1_13', order=1),title='',subtitle='',items=[ui.text_l('Descripción del problema: '+str(ticket_info[0][5]))])
                    content = '![Adrian](http://'+ipGlobal+':10101/datasets/'+routeEvidencia1[7]+')'
                    q.page['Img']=ui.markdown_card(box=ui.box('mid1_14',order=1),title='Evidencia:',content=content)
                    await q.page.save()
                else:
                    print("No hay datos de imagen disponibles.")
        refreshTable = 1
        await q.page.save()

    if q.args.btnEvidence2:
        del q.page['upldSolu']
        del q.page['form_problema']
        del q.page['Img']
        del q.page['combotextboxes3']

        ticket_info = []
        selectioned = q.args.issues
        if selectioned == None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un ticket.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if selectioned != None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            # si quieres quitar los que seleccionaste
                            found=1
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                noticketSearch = str(data_rows_send[0][0])
                proyectoSearch = str(data_rows_send[0][2])
                posteSearch = str(data_rows_send[0][3])
                ticket_info = getTicketPaP(r, noticketSearch, proyectoSearch, posteSearch)
                if ticket_info and len(ticket_info) > 0 and ticket_info[0][8]:
                    image_data = base64.b64decode(ticket_info[0][8])
                    image = Image.open(BytesIO(image_data))
                    routeSolution = '/home/adrian/ws/h2o-wave/home/data/'+noticketSearch+'_solution.png'
                    image.save(routeSolution)  # Asegúrate de especificar la ruta correcta
                    routeSolution = await q.site.download(routeSolution, '../../data/')
                    routeSolution = routeSolution.split('/')
                    q.page['form_problema'] = ui.section_card(box=ui.box('mid1_13', order=1),title='',subtitle='',items=[ui.text_l('Descripción de la solución: '+str(ticket_info[0][9]))])
                    content = '![Adrian](http://'+ipGlobal+':10101/datasets/'+routeSolution[7]+')'
                    q.page['Img'] = ui.markdown_card(box=ui.box('mid1_14',order=1),title='Solución:',content='')
                    await q.page.save()
                else:
                    print("No hay datos de imagen disponibles.")
        refreshTable = 1
        await q.page.save()

    if q.args.btnUploadSolution:
        del q.page['form_problema']
        del q.page['Img']
        del q.page['combotextboxes3']

        q.page['combotextboxes3'] = ui.section_card(
            title = '',
            subtitle = '',
            box=ui.box('mid1_13', order=1),
            items=[ui.textbox(name='textSoluTicket', label='Descripción de la solución:', trigger=True, multiline=True, width='800px')]
        )

        q.page['upldSolu'] = ui.form_card(
            box=ui.box('mid1_14', order=1),
            items=[ui.file_upload(name='uploadSoluTicket', label='', multiple=False,file_extensions=['png', 'jpg', 'jpeg'],)]
        )
        await q.page.save()

    if q.args.textSoluTicket:
        textSolucionTicket=str(q.args.textSoluTicket)
        await q.page.save()

    if q.args.uploadSoluTicket:
        selectioned = q.args.issues
        if selectioned == None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un ticket.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if selectioned != None:
            data_rows_temp, data_rows_send, found = [], [], 0
            for y in data_rows:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        # si quieres quitar los que seleccionaste
                        data_rows_send.append(y)
                if found==0:
                    pass
                    # si quieres quitar los que no seleccionaste
                    #data_rows_temp.append(y)
                found=0
            for path in q.args.uploadSoluTicket:
                solucionTicket = await q.site.download(path, '../../data/')
                rootSolucion = str(solucionTicket)
            if data_rows_send[0][7] == "In Process":
                noticketSearch = str(data_rows_send[0][0])
                proyectoSearch = str(data_rows_send[0][2])
                posteSearch = str(data_rows_send[0][3])
                trabajadorAsignado = str(data_rows_send[0][4])
                try:
                    with open(solucionTicket, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                except Exception as e:
                    print(e)
                updActPaP(r, noticketSearch, proyectoSearch, posteSearch, trabajadorAsignado, 'done', textSolucionTicket, encoded_string)
                del q.page['combotextboxes3']
                del q.page['form_problema']
                del q.page['Img']
            else:
                q.page["meta"].side_panel = ui.side_panel(
                    title="",
                    items=[ui.text("Para poder ejecutar esta accionar, primero tienes que asignar este ticket a un trabajador.")],
                    name="side_panel",
                    events=["dismissed"],
                    closable=True,
                    width = '400px',
                )
            data_rows = getAllTickets(r, 'key_tickets_obra', 'tickets_obra', 'yi_obra')
            await q.run(showList, q)
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            await q.run(showList, q)
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
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('left', size='5%', zones=[
                                ui.zone('izq1_11',size='15%',align='start',direction=ui.ZoneDirection.COLUMN),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('mid',size='80%', zones=[
                                ui.zone('mid1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('mid1_1', size='90%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('mid1_11', size='80%', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('mid1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('mid1_13', size='15%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('mid1_14', size='75%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('mid1_2',size='15%', zones=[
                                        ui.zone('mid1_21', size='90%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('mid1_22', size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ]),
                                ]),
                            ]),
                            ui.zone('der1', size='10%', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('der1_10',size='5%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_11',size='5%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_12',size='10%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_13',size='10%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_14',size='10%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_15',size='10%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_16',size='10%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_17',size='10%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_18',size='15%',align='center', direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_19',size='15%',align='center', direction=ui.ZoneDirection.ROW),
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
        #########   BTNS   #########
        q.page['btns2']=ui.section_card(box=ui.box('der1_12',order=1),title='',subtitle='',items=[ui.button(name='btnEvidence1',label='Evidencia',disabled=False,primary=False, icon='RedEye')])
        q.page['btns3']=ui.section_card(box=ui.box('der1_13',order=1),title='',subtitle='',items=[ui.button(name='btnEvidence2',label='Solución',disabled=False,primary=False, icon='RedEye')])
        q.page['btns4']=ui.section_card(box=ui.box('der1_14',order=1),title='',subtitle='',items=[ui.button(name='btnUploadSolution',label='Subir solución', disabled=False, primary=True, icon='PublishContent')])
        #########   Cassia Home   #########
        q.page['boton2'] = ui.section_card(
            box=ui.box('mid1_12', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnWOI', label='Work on it', disabled = False, primary=True, icon='PenWorkspace'),
                ui.button(name='btnFI', label='Finish it', disabled = False, primary=True, icon='DocumentReply'),
                ui.button(name='btnDptoExcptns', label='Exception', disabled = False, primary=True, icon='EventDeclined'),
            ],
        )

        await q.page.save()
        data_rows = getAllTickets(r, 'key_tickets_obra', 'tickets_obra', 'yi_obra')
        await q.run(start_or_restart_refresh,q)

@app('/pap_manage', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_manage(q)