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
from common0 import session
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
        global session, user
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            session = data['session']
            user = data['user']
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
                        #self.work(message['data'])
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

client = Listener1(r, ['last_session','LT01TP0LT'])
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
    global dispositivo, municipio

    dispositivo = tech
    municipio = muni

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
    
    if dispositivo == 'LPR':
        ###### Box to make actions.
        q.page['actions'] = ui.form_card(
            box=ui.box('izq1_5', order=1),
            items=[
                ui.text_xl(content='Soluciones rapidas'),
                ui.buttons(justify='center', items=[
                    ui.button(name=btnPing, label='PING'),
                ]),
                ui.buttons(justify='center', items=[
                    ui.button(name=btnIP, label='User page'),
                    ui.button(name=btnLoc, label='Device location')
                ])
        ])

    if dispositivo == 'PTZ':
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
    global fig, dispositivo, municipio, comboboxEstM
    global botonShow1, botonShow2
    global refreshTecno, refreshMuni
    global btnIP, btnLoc, btnPing, btnFtp

    rendered = 0

    del q.page['lista-show']
    q.page['details'] = ui.markdown_card(box=ui.box('der1_12', order=1),title='Información y acciones',content='Nothing selected.')
    del q.page['actions']
    del q.page['networkActive']
    del q.page['networkError']
    del q.page['ftpRight']
    del q.page['ftpError']

    refreshTecno = dispositivo
    refreshMuni = municipio
    level = ''

    if dispositivo == 'RADIOGRAFIA TT':
        radiografia = 'SI'
        rendered = 1
        fig = connectionsTracesTT(tracesTT,refreshMuni)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'RADIOGRAFIA TP':
        radiografia = 'SI'
        rendered = 1
        html = 0
        fig = connectionsTraces(tracesTP, refreshMuni)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'SUSCRIPTORES':
        level = 'LS'
        radiografia = 'NO'
        rendered = 1
        html = 0
        fig = connectionsPoints(refreshMuni,level)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'LPR':
        level = 'LL'
        radiografia = 'NO'
        rendered = 1
        html = 0
        fig = connectionsPoints(refreshMuni,level)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'PTZ':
        level = 'LP'
        radiografia = 'NO'
        rendered = 1
        html = 0
        fig = connectionsPoints(refreshMuni,level)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'FIJAS':
        level = 'LF'
        radiografia = 'NO'
        rendered = 1
        fig = connectionsTraces(traces,level)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'INTERCOM':
        level = '10'
        radiografia = 'NO'
        rendered = 1
        fig = connectionsTraces(traces,level)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'SWITCH':
        level = 'LSW'
        radiografia = 'NO'
        rendered = 1
        fig = connectionsTraces(traces,level)
        html = pio.to_html(fig[0], validate=False, include_plotlyjs='cdn',config = {'displayModeBar': False})
        q.page['plot'].content = html

    if dispositivo == 'Seleccionar'and ciudad == 'Seleccionar' and municipio == 'Seleccionar':
        pass

    if rendered == 1:
        del q.page['stableDevices']
        del q.page['problemDevices']

        ###### Markdown to display check image and button to show the conected devices in the table
        checkRight = 'https://upload.wikimedia.org/wikipedia/commons/c/c6/Sign-check-icon.png'
        q.page['stableDevices'] = ui.form_card(
            box=ui.box(zone='izq1_3', order=1),
            items=[
                ui.persona(title=f'{fig[1]} DEVICES', subtitle='- WITH CONNECTION', caption='', size='xs', image=checkRight),
                ui.button(name='btnShow1', width= '80px',label='Show', disabled = False, primary = True)
        ]) 
        if radiografia != 'SI':
            checkWrong = 'https://freepngimg.com/thumb/red_cross_mark/5-2-red-cross-mark-download-png.png'
            q.page['problemDevices'] = ui.form_card(
                box=ui.box(zone='izq1_4', order=1),
                items=[
                    ui.persona(title=f'{fig[2]} DEVICES', subtitle='- WITHOUT CONNECTION', caption='', size='xs', image=checkWrong),
                    ui.button(name='btnShow2', width= '80px',label='Show', disabled = False, primary = True)
            ])
        await q.page.save()
        #await q.run(refresh,q,fig[5],fig[6],level)

    else:
        pass

    if botonShow1 == 1:
        del q.page['details']
        await q.run(showList, q, fig[3], 'conectados', dispositivo, refreshMuni)
        await q.page.save()
    if botonShow2 == 1:
        del q.page['details']
        await q.run(showList, q, fig[4], 'desconectados', dispositivo, refreshMuni)
        await q.page.save()

    q.page['comboboxes'] = ui.form_card(
        box=ui.box('izq1_2', order=1),
        items=[
            ui.combobox(name='comboboxtecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
            ui.combobox(name='textciudad', label='Ciudad', value='Seleccionar', choices=comboboxEstM,trigger=True),
            ui.combobox(name='comboboxmuni', label='Municipio', value='Seleccionar', choices=comboboxMuni,trigger=True),
            ui.combobox(name='comboboxmuni1', label='Host', value='Seleccionar', choices=comboboxVars,trigger=True),
            ui.button(name='show_inputs', label='Consultar', primary=True),
        ],
    )

    await q.page.save()

async def refresh(q: Q, conectados, desconectados, level):
    global fig, refreshMuni
    while 1:
        print('Get metrics...')
        fig = connectionsPoints(refreshMuni,level)
        if fig[5] != []:
            if (np.array_equal(conectados, fig[5])):
                pass
            else:
                print("se ha desconectado un dispositivo")
                await q.run(rendering,q)
        if fig[6] != []:
            if (np.array_equal(desconectados, fig[6])):
                pass
            else:
                print("se ha conectado un dispositivo")
                await q.run(rendering,q)
        await q.sleep(5)

async def maps(q: Q):
    global updtd, comboboxAll,comboboxMuni, comboboxTecno, fig, data_table_stable, data_table_problem, selectioned
    global btnPing, btnFtp, btnIP, btnLoc
    global dispositivo, municipio, refreshTecno, refreshMuni
    global botonShow1, botonShow2, session, comboboxEstM, ciudad

    print("Start aplication maps...")
    #updtd = 0
    if q.args.home:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()
        
    if q.args.settings:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/settings'
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

#############    S    E    L    E    C    T   --   T    E    C    H    #############
    if q.args.comboboxtecno and dispositivo != str(q.args.comboboxtecno):
        if str(q.args.comboboxtecno) != '':
            dispositivo = str(q.args.comboboxtecno)

            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='textciudad', label='Ciudad', value=str(q.args.textciudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxmuni', label='Municipio', value=municipio, choices=comboboxMuni,trigger=True),
                    ui.combobox(name='comboboxmuni1', label='Host', value='Seleccionar', choices=comboboxVars,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
            await q.page.save()
        if str(q.args.comboboxtecno) == 'RADIOGRAFIA TT':
            dispositivo = str(q.args.comboboxtecno)

            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='textciudad', label='Ciudad', value=str(q.args.textciudad), choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxmuni', label='Municipio', value=municipio, choices=comboboxAll,trigger=True),
                    ui.combobox(name='comboboxmuni1', label='Host', value='Seleccionar', choices=comboboxVars,trigger=True),
                    ui.button(name='show_inputs', label='Consultar', primary=True),
                ],
            )
            await q.page.save()

#############    S    E    L    E    C    T   --   C    I    T    Y    #############
    if q.args.textciudad and ciudad != str(q.args.textciudad):
        val = ' '
        if str(q.args.textciudad) == 'ALL':
            comboboxMuni = ['ALL']
            val = 'ALL'
        if str(q.args.textciudad) == 'COLIMA':
            comboboxMuni = comboboxMuniColM
            val = 'ARMERÍA'
        if str(q.args.textciudad) == 'MICHOACAN':
            comboboxMuni = comboboxMuniMichM
            val = 'ACATIC'
        if str(q.args.textciudad) == 'JALISCO':
            comboboxMuni = comboboxMuniJalM
            val = 'ACUITZIO'

        municipio = val
        ciudad = str(q.args.textciudad)
        q.page['comboboxes'] = ui.form_card(
            box=ui.box('izq1_2', order=1),
            items=[
                ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                ui.combobox(name='textciudad', label='Ciudad', value=str(q.args.textciudad), choices=comboboxEstM,trigger=True),
                ui.combobox(name='comboboxmuni', label='Municipio', value=municipio, choices=comboboxMuni,trigger=True),
                ui.combobox(name='comboboxmuni1', label='Host', value='Seleccionar', choices=comboboxVars,trigger=True),
                ui.button(name='show_inputs', label='Consultar', primary=True),
            ],
        )
        await q.page.save()
#############    S    E    L    E    C    T   --   M    U   N   I   C   I   P   I   O    #############
    if q.args.comboboxmuni and municipio != str(q.args.comboboxmuni):
        if str(q.args.comboboxmuni) != '':
            municipio = str(q.args.comboboxmuni)

            q.page['comboboxes'] = ui.form_card(
                box=ui.box('izq1_2', order=1),
                items=[
                    ui.combobox(name='comboboxtecno', label='Tecnología', value=dispositivo, choices=comboboxTecno,trigger=True),
                    ui.combobox(name='textciudad', label='Ciudad', value=ciudad, choices=comboboxEstM,trigger=True),
                    ui.combobox(name='comboboxmuni', label='Municipio', value=municipio, choices=comboboxMuni,trigger=True),
                    ui.combobox(name='comboboxmuni1', label='Host', value='Seleccionar', choices=comboboxVars,trigger=True),
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
            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshMuni)
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
            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshMuni)
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

            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshMuni)
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

            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshMuni)
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

            await q.run(showList, q, fig[3], 'conectados', refreshTecno, refreshMuni)
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

            await q.run(showList, q, fig[4], 'desconectados', refreshTecno, refreshMuni)
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

    q.page['meta'] = ui.meta_card(box='', icon='![Adrian](http://'+ipGlobal+':10101/datasets/cassia-logo.png)')
    if not q.client.initialized:  # First visit
        q.client.initialized = True
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93%',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='12%', direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('izq1_1',size='14%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_2',size='33%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_3',size='10%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_4',size='11%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_5',size='22%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_6',size='12%',align='center',direction=ui.ZoneDirection.ROW),
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
        content = '![Adrian](http://'+ipGlobal+':10101/datasets/cassia-logo.png)'
        q.page['STPImg'] = ui.markdown_card(
            box=ui.box('izq1_1', order=1),
            title='',
            content= content,
        )
        ###### Combobox to select any options, technology first and after city.
        q.page['comboboxes'] = ui.form_card(
            box=ui.box('izq1_2', order=1),
            items=[
                ui.combobox(name='comboboxtecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.combobox(name='textciudad', label='Ciudad', value='Seleccionar', choices=comboboxEstM,trigger=True),
                ui.combobox(name='comboboxmuni', label='Municipio', value='Seleccionar', choices=comboboxMuni,trigger=True),
                ui.combobox(name='comboboxmuni1', label='Data from Device', value='Seleccionar', choices=comboboxVars,trigger=True),
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