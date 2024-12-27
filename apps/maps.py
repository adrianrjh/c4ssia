import sys
import threading,json,time,math
from plotly import graph_objects as go
from plotly import io as pio
from h2o_wave import ui, main, app, Q
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common2 import *
from common0 import *
sys.path.insert(0, '/home/adrian/ws/wave/cassia/data')
from municipios_est import *
import webbrowser
import numpy as np
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

#############    F    U    N    C    T    I    O    N   --   P    I    N    G    #############
async def ping_test(q: Q, hostIP: str, hostAfiliacion: str):
    del q.page['networkActive']
    del q.page['networkError']
    del q.page['ftpRight']
    del q.page['ftpError']

    q.page['actions'] = ui.form_card(
        box=ui.box('izq1_5', order=1),
        items=[
            ui.text_xl(content='Soluciones rapidas'),
            ui.buttons(justify='center', items=[
                ui.button(name=btnPing, label='PING',primary=True),
                ui.button(name=btnFtp, label='FTP'),
            ]),
            ui.buttons(justify='center', items=[
                ui.button(name=btnIP, label='User page'),
                ui.button(name=btnLoc, label='Device location')
            ]),
    ])

    q.page['progressPing'] = ui.form_card(
        box=ui.box(zone='izq1_6', order=1),
        items=[
            ui.progress('Pinging to '+hostAfiliacion),
        ]
    )
    await q.page.save()
    await q.sleep(0.5)
    pingstatus = check_ping(hostIP)
    if pingstatus == "Network Active":
        del q.page['progressPing']
        ###### Markdown to display check image and button to show the conected devices in the table
        checkRight = 'https://upload.wikimedia.org/wikipedia/commons/c/c6/Sign-check-icon.png'
        q.page['networkActive'] = ui.form_card(
            box=ui.box(zone='izq1_6', order=1),
            items=[
                ui.persona(title='Ping', subtitle='Test correct', caption=hostAfiliacion, size='m', image=checkRight),
        ])

    if pingstatus == "Network Error":
        del q.page['progressPing']
        ###### Markdown to display check image and button to show the disconected devices in the table
        checkWrong = 'https://freepngimg.com/thumb/red_cross_mark/5-2-red-cross-mark-download-png.png'
        q.page['networkError'] = ui.form_card(
            box=ui.box(zone='izq1_6', order=1),
            items=[
                ui.persona(title='Ping', subtitle='Test incorrect', caption=hostAfiliacion, size='m', image=checkWrong),
        ])
    
    q.page['actions'] = ui.form_card(
        box=ui.box('izq1_5', order=1),
        items=[
            ui.text_xl(content='Soluciones rapidas'),
            ui.buttons(justify='center', items=[
                ui.button(name=btnPing, label='PING',primary=False),
                ui.button(name=btnFtp, label='FTP'),
            ]),
            ui.buttons(justify='center', items=[
                ui.button(name=btnIP, label='User page'),
                ui.button(name=btnLoc, label='Device location')
            ]),
    ])

    await q.page.save()

#############    F    U    N    C    T    I    O    N   --   F    T    P    #############
async def ftp_test(q: Q, hostIP: str, hostAfiliacion: str):
    del q.page['ftpRight']
    del q.page['ftpError']
    del q.page['networkActive']
    del q.page['networkError']

    q.page['actions'] = ui.form_card(
        box=ui.box('izq1_5', order=1),
        items=[
            ui.text_xl(content='Soluciones rapidas'),
            ui.buttons(justify='center', items=[
                ui.button(name=btnPing, label='PING'),
                ui.button(name=btnFtp, label='FTP', primary=True),
            ]),
            ui.buttons(justify='center', items=[
                ui.button(name=btnIP, label='User page'),
                ui.button(name=btnLoc, label='Device location')
            ]),
    ])

    q.page['progressFTP'] = ui.form_card(
        box=ui.box(zone='izq1_6', order=1),
        items=[
            ui.progress('FTPing to '+hostAfiliacion),
        ]
    )

    await q.page.save()
    await q.sleep(0.5)
    
    ftpstatus = check_ftp(hostIP)
    if ftpstatus == "Network Active":
        del q.page['progressFTP']
        ###### Markdown to display check image and button to show the conected devices in the table
        checkWrong = 'https://freepngimg.com/thumb/red_cross_mark/5-2-red-cross-mark-download-png.png'
        q.page['ftpError'] = ui.form_card(
            box=ui.box(zone='izq1_6', order=1),
            items=[
                ui.persona(title='FTP', subtitle='Test incorrect', caption=hostAfiliacion, size='m', image=checkWrong),
        ])

    if ftpstatus == "Network Error":
        del q.page['progressFTP']
        ###### Markdown to display check image and button to show the disconected devices in the table
        checkRight = 'https://upload.wikimedia.org/wikipedia/commons/c/c6/Sign-check-icon.png'
        q.page['ftpRight'] = ui.form_card(
            box=ui.box(zone='izq1_6', order=1),
            items=[
                ui.persona(title='FTP', subtitle='Test correct', caption=hostAfiliacion, size='m', image=checkRight),
        ])

    q.page['actions'] = ui.form_card(
        box=ui.box('izq1_5', order=1),
        items=[
            ui.text_xl(content='Soluciones rapidas'),
            ui.buttons(justify='center', items=[
                ui.button(name=btnPing, label='PING'),
                ui.button(name=btnFtp, label='FTP', primary=False),
            ]),
            ui.buttons(justify='center', items=[
                ui.button(name=btnIP, label='User page'),
                ui.button(name=btnLoc, label='Device location')
            ]),
    ])

    await q.page.save()

#############    F    U    N    C    T    I    O    N   --   T    A    B    L    A    S    #############
async def showList(q: Q, table, description: str, tech:str, muni:str):
    global btnIP, btnLoc, btnPing, btnFtp
    global dispositivo, localidad

    dispositivo = tech
    localidad = muni

    del q.page['details']
    del q.page['networkActive']
    del q.page['networkError']
    del q.page['ftpRight']
    del q.page['ftpError']
    del q.page['lista-show']
    del q.page['actions']

    dato = []

    if description == 'conectados':
        btnIP = 'btnIP1'
        btnLoc = 'btnLoc1'
        btnPing = 'btnPing1'
        btnFtp = 'btnFtp1'
        q.page['stableDevices'].items[1].button.disabled = True
        q.page['problemDevices'].items[1].button.disabled = False
    if description == 'desconectados':
        btnIP = 'btnIP2'
        btnLoc = 'btnLoc2'
        btnPing = 'btnPing2'
        btnFtp = 'btnFtp2'
        q.page['stableDevices'].items[1].button.disabled = False
        q.page['problemDevices'].items[1].button.disabled = True

    q.page['lista-show'] = ui.form_card(
        box=ui.box('der1_12', order=1), 
        items=[
            ui.text_xl(content='Descripción de los dispositivos '+str(description)),
            ui.table(
                name='issues', 
                height='320px', 
                columns = columns,
                rows=[ui.table_row(
                    name=str(dato[0]),
                    cells=dato
                    )for dato in table],
                #values = ['0'],
                multiple = True,
                downloadable=True,
            ),
        ]
    )
    
    ###### Box to make actions.
    q.page['actions'] = ui.form_card(
        box=ui.box('izq1_5', order=1),
        items=[
            ui.text_xl(content='Soluciones rapidas'),
            ui.buttons(justify='center', items=[
                ui.button(name=btnPing, label='PING'),
                ui.button(name=btnFtp, label='FTP'),
            ]),
            ui.buttons(justify='center', items=[
                ui.button(name=btnIP, label='User page'),
                ui.button(name=btnLoc, label='Device location')
            ])
    ])

    await q.page.save()

#############    F    U    N    C    T    I    O    N    --    R    E    N    D    E    R     I    N    G    #############
async def rendering(q: Q):
    global fig, dispositivo, ciudad, localidad, comboboxEstM,comboboxLocaColM
    global botonShow1, botonShow2
    global refreshTecno, refreshEstado, refreshLoca
    global btnIP, btnLoc, btnPing, btnFtp,enterToMonitor

    rendered = 0
    del q.page['lista-show']
    q.page['details'] = ui.markdown_card(box=ui.box('der1_12', order=1),title='Información y acciones',content='Nothing selected.')
    del q.page['actions']
    del q.page['networkActive']
    del q.page['networkError']
    del q.page['ftpRight']
    del q.page['ftpError']

    refreshTecno = dispositivo
    refreshCiudad = ciudad
    refreshLoca = localidad
    ########## PUNTOS DE EQUIPOS ##########
    if refreshTecno != 'RADIOGRAFIA FIBRA' and refreshTecno != '':
        rendered = 1
        radiografia = 'NO'
        html = 0
        enterToMonitor = 0
        fig = connectionsPoints(refreshTecno, refreshCiudad, refreshLoca)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html
    ######### RADIOGRAFIA DE FIBRA ##########
    if refreshTecno == 'RADIOGRAFIA FIBRA' and refreshTecno != '':
        rendered = 1
        radiografia = 'SI'
        html = 0
        enterToMonitor = 0
        fig = connectionsTraces(refreshCiudad, refreshLoca)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html
    ######### N O   A C T I O N S #########
    if refreshTecno == 'Seleccionar'and refreshCiudad == 'Seleccionar' and refreshLoca == 'Seleccionar':
        pass

    if rendered == 1:
        q.page['comboboxes'] = ui.form_card(
            box=ui.box('izq1_2', order=1),
            items=[
                ui.combobox(name='comboboxtecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.combobox(name='combociudad', label='Estado', value='Seleccionar', choices=comboboxEstM,trigger=True),
                ui.combobox(name='comboboxloca', label='Localidad', value='Seleccionar', choices=comboboxLoca,trigger=True),
                ui.button(name='show_inputs', label='Consultar', primary=True),
            ],
        )
        if botonShow1 == 1:
            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshLoca)
        if botonShow2 == 1:
            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshLoca)
        del q.page['stableDevices']
        del q.page['problemDevices']
        ###### Markdown to display check image and button to show the conected devices in the table
        if len(fig[3])>0:
            checkRight = 'https://upload.wikimedia.org/wikipedia/commons/c/c6/Sign-check-icon.png'
            q.page['stableDevices'] = ui.form_card(
                box=ui.box(zone='izq1_3', order=1),
                items=[
                    ui.persona(title=f'{fig[1]} DEVICES', subtitle='WITH CONNECTION', caption='', size='xs', image=checkRight),
                    ui.button(name='btnShow1', width= '80px',label='Show', disabled = False, primary = True)
            ])
        if len(fig[4])>0:
            checkWrong = 'https://freepngimg.com/thumb/red_cross_mark/5-2-red-cross-mark-download-png.png'
            q.page['problemDevices'] = ui.form_card(
                box=ui.box(zone='izq1_4', order=1),
                items=[
                    ui.persona(title=f'{fig[2]} DEVICES', subtitle='WITHOUT CONNECTION', caption='', size='xs', image=checkWrong),
                    ui.button(name='btnShow2', width= '80px',label='Show', disabled = False, primary = True)
                ]
            )
        await q.page.save()
        await q.run(start_or_restart_refresh,q,fig[3],fig[4],refreshTecno, refreshCiudad, refreshLoca)
    else:
        pass
    dispositivo, ciudad, localidad = '','',''
    await q.page.save()

async def refresh(q: Q, conectados, desconectados, tech, ciudad, localidad):
    global fig, refreshLoca
    global current_refresh_task, enterToMonitor
    try:
        while 1:
            if tech != "RADIOGRAFIA FIBRA":
                if enterToMonitor == 1:
                    fig = connectionsPoints(tech, ciudad, localidad)
                    if fig[3] != []:
                        if (np.array_equal(conectados, fig[3])) == False:
                            #se ha desconectado un dispositivo
                            conectados = fig[3]
                            await q.run(rendering,q)
                else:
                    enterToMonitor = 1
            if tech == "RADIOGRAFIA FIBRA":
                fig = connectionsTraces(ciudad, localidad)
                if fig[3] != []:
                    if (np.array_equal(conectados, fig[3])) == False:
                        #se ha desconectado un dispositivo
                        conectados = fig[3]
                        await q.run(rendering,q)
            await q.sleep(30)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q, conectados, desconectados, tech, ciudad, localidad):
    global current_refresh_task
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
    current_refresh_task = asyncio.create_task(refresh(q, conectados, desconectados, tech, ciudad, localidad))

async def maps(q: Q):
    global updtd, comboboxAll,comboboxMuni, comboboxTecno, comboboxLoca, fig, data_table_stable, data_table_problem, selectioned
    global btnPing, btnFtp, btnIP, btnLoc
    global dispositivo, ciudad, localidad, refreshTecno, dataFD,refreshLoca
    global botonShow1, botonShow2, session, comboboxEstM

    print("Start aplication maps...")
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

#############    S    E    L    E    C    T   --   T    E    C    H    #############
    if q.args.comboboxtecno and dispositivo != str(q.args.comboboxtecno):
        if str(q.args.comboboxtecno) != '' and str(q.args.comboboxtecno) != 'RADIOGRAFIA FIBRA' and str(q.args.comboboxtecno) != 'Seleccionar':
            dispositivo = str(q.args.comboboxtecno)
            del q.page['comboboxes']
            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='combociudad', label='Estado', value=str(q.args.combociudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxloca', label='Localidad', value='Seleccionar', choices=comboboxLoca,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
            await q.page.save()
        if str(q.args.comboboxtecno) == 'RADIOGRAFIA FIBRA':
            del q.page['comboboxes']
            dispositivo = str(q.args.comboboxtecno)
            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='combociudad', label='Estado', value=str(q.args.combociudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxloca', label='Localidad', value='Seleccionar', choices=comboboxLoca,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
        await q.page.save()

#############    S    E    L    E    C    T   --   C    I    T    Y    #############
    if q.args.combociudad and ciudad != str(q.args.combociudad):
        val = ' '
        if str(q.args.combociudad) == 'ALL':
            comboboxLoca = ['ALL']
            val = 'ALL'
        if str(q.args.combociudad) == 'COLIMA':
            comboboxLoca = comboboxLocaColM
            val = 'ARMERÍA'
        if str(q.args.combociudad) == 'MICHOACAN':
            comboboxLoca = comboboxMuniMichM
            val = 'ACATIC'
        if str(q.args.combociudad) == 'JALISCO':
            comboboxLoca = comboboxMuniJalM
            val = 'ACUITZIO'
        localidad = val
        ciudad = str(q.args.combociudad)
        if ciudad != 'Seleccionar' and dispositivo != 'RADIOGRAFIA FIBRA':
            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='combociudad', label='Estado', value=str(q.args.combociudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxloca', label='Localidad', value='Seleccionar', choices=comboboxLoca,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
        elif ciudad != 'Seleccionar' and dispositivo == 'RADIOGRAFIA FIBRA':
            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='combociudad', label='Estado', value=str(q.args.combociudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxloca', label='Localidad', value='Seleccionar', choices=comboboxLoca,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
        await q.page.save()
#############    S    E    L    E    C    T   --   L    O   C   A   L   I   D   A   D   #############
    if q.args.comboboxloca and localidad != str(q.args.comboboxloca):
        localidad = str(q.args.comboboxloca)
        if localidad != 'Seleccionar':
            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='combociudad', label='Estado', value=str(q.args.combociudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxloca', label='Localidad', value=localidad, choices=comboboxLoca,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
        await q.page.save()
#############    B    T    N   --   R    E    N    D    E    R    I    N    G    #############
    if q.args.show_inputs:
        await q.run(rendering, q)
        await q.page.save()

#############    B    T    N    S   --   T    A    B    L    A    S    #############
    if q.args.btnShow1:
        ##### Display 'conected table', if fig's have info show table, else pass.
        if fig[3] != []:
            botonShow1 = 1
            botonShow2 = 0
            del q.page['lista-show']
            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshLoca)
        else:
            del q.page['lista-show']
            q.page['details'] = ui.markdown_card(box=ui.box('der1_12', order=1),title='Información y acciones',content='Nothing selected.')
        await q.page.save()

    if q.args.btnShow2:
        ##### Display 'disconected table', if fig's have info show table, else pass.
        if fig[4] != []:
            botonShow1 = 0
            botonShow2 = 1
            del q.page['lista-show']
            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshLoca)
        else:
            del q.page['lista-show']
            q.page['details'] = ui.markdown_card(box=ui.box('der1_12', order=1),title='Información y acciones',content='Nothing selected.')
        await q.page.save()

#############    B    T    N    S   --   U    S    E    R    P    A    G    E    #############
    if q.args.btnIP1:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues
        if selectioned != []:
            found = 0
            for y in fig[3]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0

            a_website = selectioned[3]
            # Open url in a new page (“tab”) of the default browser, if possible
            webbrowser.open_new_tab(a_website)

            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshLoca)
            await q.page.save()
        else:
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
            await q.page.save()

    if q.args.btnIP2:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues
        if selectioned != []:
            found = 0
            for y in fig[4]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0

            a_website = selectioned[3]
            # Open url in a new page (“tab”) of the default browser, if possible
            webbrowser.open_new_tab(a_website)

            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshLoca)
            await q.page.save()
        else:
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
            await q.page.save()

#############    B    T    N    S   --   L    O    C    A    T    I    O    N    #############
    if q.args.btnLoc1:
        ##### Search the Location attr to administrate the device
        selectioned = q.args.issues
        if selectioned != []:
            found = 0
            for y in fig[3]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0

            location = selectioned[4]
            # Open url in a new page (“tab”) of the default browser, if possible
            webbrowser.open('https://www.google.com/maps/place/'+location)

            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshLoca)
            await q.page.save()
        else:
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
            await q.page.save()

    if q.args.btnLoc2:
        ##### Search the Location attr to administrate the device
        selectioned = q.args.issues
        if selectioned != []:
            found = 0
            for y in fig[4]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0

            location = selectioned[4]
            # Open url in a new page (“tab”) of the default browser, if possible
            webbrowser.open('https://www.google.com/maps/place/'+location)

            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshLoca)
            await q.page.save()
        else:
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
            await q.page.save()

#############    B    T    N    S   --   P    I    N    G    #############
    if q.args.btnPing1:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues
        if (selectioned != []) and (len(selectioned)==1):
            found = 0
            for y in fig[3]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0

            ip = selectioned[3]
            afiliacion = selectioned[2]
            await q.run(ping_test, q, ip, afiliacion)
            await q.page.save()
        else:
            del q.page['networkActive']
            del q.page['networkError']
            del q.page['ftpRight']
            del q.page['ftpError']
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
            await q.page.save()

    if q.args.btnPing2:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues
        if (selectioned != []) and (len(selectioned)==1):
            found = 0
            for y in fig[4]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0
            ip = selectioned[3]
            afiliacion = selectioned[2]
            await q.run(ping_test, q, ip, afiliacion)
            await q.page.save()
        else:
            del q.page['networkActive']
            del q.page['networkError']
            del q.page['ftpRight']
            del q.page['ftpError']
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])

            await q.run(ping_test, q, ip, afiliacion)
            await q.page.save()
#############    B    T    N    S   --   F    T    P    #############
    if q.args.btnFtp1:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues
        if (selectioned != []) and (len(selectioned)==1):
            found = 0
            for y in fig[3]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:
                    pass
                found=0
            ip = selectioned[3]
            afiliacion = selectioned[2]
            await q.run(ftp_test, q, ip, afiliacion)
            await q.page.save()
        else:
            del q.page['networkActive']
            del q.page['networkError']
            del q.page['ftpRight']
            del q.page['ftpError']
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
            await q.page.save()

    if q.args.btnFtp2:
        ##### Search the IP attr to administrate the device
        selectioned = q.args.issues
        if (selectioned != []) and (len(selectioned)==1):
            found = 0
            for y in fig[4]:
                for x in selectioned:
                    if str(y[0])==str(x):
                        found=1
                        selectioned = y
                if found==0:    
                    pass
                found=0
            ip = selectioned[3]
            afiliacion = selectioned[2]
            await q.run(ftp_test, q, ip, afiliacion)
            await q.page.save()
        else:
            del q.page['networkActive']
            del q.page['networkError']
            del q.page['ftpRight']
            del q.page['ftpError']
            ###### Box to make actions.
            q.page['actions'] = ui.form_card(
                box=ui.box('izq1_5', order=1),
                items=[
                    ui.text_xl(content='Soluciones rapidas'),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnPing, label='PING'),
                        ui.button(name=btnFtp, label='FTP'),
                    ]),
                    ui.buttons(justify='center', items=[
                        ui.button(name=btnIP, label='User page'),
                        ui.button(name=btnLoc, label='Device location')
                    ]),
                    ui.text_xl(content='¡ERROR! - Selecciona solo un dispositivo'),
            ])
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
                            ui.zone('izq1', size='12%', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('izq1_1',size='11%',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_2',size='30%',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_3',size='15%',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_4',size='15%',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_5',size='17%',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_6',size='12%',direction=ui.ZoneDirection.ROW),
                            ]),
                            ui.zone('der1',size='88%', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1',size='100%', zones=[
                                        ##### MAPA #####
                                        ui.zone('der1_11', size='100%', direction=ui.ZoneDirection.ROW),
                                        ##### TABLE #####
                                        ui.zone('der1_12', size='40%', align='center', direction=ui.ZoneDirection.ROW),
                                    ]),
                                ]),
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
############ IIIIIIII   ZZZZZZZ     QQQQQQQQ ################
        ###### Image logo of the company
        content = 'http://'+ipGlobal+':10101/datasets/cassia-logo2.png'
        q.page['CassiaImg'] = ui.section_card(
            box=ui.box('izq1_1', order=1),
            title='',
            subtitle = '',
            items = [
                ui.image(title='', path=content)
            ]
        )
        q.page['comboboxes'] = ui.form_card(
            box=ui.box('izq1_2', order=1),
            items=[
                ui.combobox(name='comboboxtecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.combobox(name='combociudad', label='Estado', value='Seleccionar', choices=comboboxEstM,trigger=True),
                ui.combobox(name='comboboxloca', label='Localidad', value='Seleccionar', choices=comboboxLoca,trigger=True),
                ui.button(name='show_inputs', label='Consultar', primary=True),
        ])
############ DDDDDDD   EEEEEEEE     RRRRRRRR ################
        ###### Map, is where show the points and traces queried.
        q.page['plot'] = ui.frame_card(box=ui.box('der1_11', order=1), title='', content='')
        q.page['details'] = ui.markdown_card(box=ui.box('der1_12', order=1),title='Información y acciones',content='Nothing selected.')
        # Save page
        await q.page.save()
        await q.run(rendering, q)

@app('/maps', mode = 'unicast')
async def map(q: Q):
    route = q.args['#']
    await maps(q)