from h2o_wave import Q, app, main, ui, AsyncSite,site,data
from pyzabbix import ZabbixAPI
import threading,json,time,math
from datetime import datetime
import sys
import random
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common1 import *

from plotly import io as pio

class Listener1(threading.Thread):
    def __init__(self,zapi):
        threading.Thread.__init__(self)
        self.zapiCon = zapi

    def comparator(self, groupComp, clockComp, hostComp, ipComp, problemComp, enabledComp):
        global groupCompBef, clockCompBef, hostCompBef, ipCompBef, problemCompBef, enabledCompBef,msg,data_rows, data_rows_keycount
        if groupComp != groupCompBef:
            if clockComp!= clockCompBef:
                if hostComp != hostCompBef:
                    if ipComp != ipCompBef:
                        print("Group: "+groupComp)
                        print("Time: "+clockComp)
                        print("Host: "+hostComp)
                        print("IP: "+ipComp)
                        print("Problem: "+problemComp)
                        print("Status Host: "+enabledComp)
                        print(" ")
                        data_rows_keycount += 1 
                        data_rows.append([str(data_rows_keycount),str(groupComp),str(clockComp), str(hostComp),str(ipComp),str(problemComp), str(enabledComp)])
        else:
            pass
        groupCompBef = groupComp
        clockCompBef = clockComp
        hostCompBef = hostComp 
        ipCompBef = ipComp
        problemCompBef = problemComp
        enabledCompBef = enabledComp

    def work(self):
        global groupCompAft, clockCompAft, hostCompAft, ipCompAft, problemCompAft, enabledCompAft
        problems = self.zapiCon.problem.get()
        lenProblem = len(problems)
        trigger = self.zapiCon.trigger.get(triggerids=problems[lenProblem-1]['objectid'], selectHosts='extend')
        interface = self.zapiCon.hostinterface.get(hostids=trigger[0]['hosts'][0]['hostid'])
        group = self.zapiCon.hostgroup.get(hostids=trigger[0]['hosts'][0]['hostid'])

        enabled = "Enabled"
        if (trigger[0]['hosts'][0]['status'] == "1"):
          enabled = "Disabled"
    
        dt_object = datetime.fromtimestamp(int(problems[lenProblem-1]['clock']))

        clockCompAft = str(dt_object)
        groupCompAft = group[0]['name']
        hostCompAft = trigger[0]['hosts'][0]['host']
        ipCompAft = interface[0]['ip']
        problemCompAft = trigger[0]['description']
        enabledCompAft = enabled
        
        self.comparator(groupCompAft, clockCompAft, hostCompAft, ipCompAft, problemCompAft, enabledCompAft)

    def run(self):
        while 1:
            try:
                self.work()
            except Exception as e:
                # Logout from Zabbix
                #self.zapiCon.user.logout()
                print(e)
            time.sleep(1)  # be nice to the system :)

try:
    # Create ZabbixAPI class instance
    zapi = ZabbixAPI(url='http://10.21.211.136/zabbix/', user='provider', password='Pr0v1d3r')
except Exception as e:
    # Logout from Zabbix
    print(e)
    #zapi.user.logout()

client1 = Listener1(zapi)
client1.start()

async def showList(q: Q):
    global data_rows, data_rows_keycount
    lenData_rows = 0
    while 1:
        #if bandShow == 0:
        #    bandShow = 1
        #    q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
        #        ui.table(
        #            name='issues',
        #            columns=columns1,
        #            rows=[ui.table_row(
        #                name=str(dato[0]),
        #                cells=dato,
        #            )for dato in data_rows],
        #            #values = ['0'],
        #            groupable=True,
        #            downloadable=True,
        #        )
        #    ])
        if len(data_rows) > lenData_rows:
            lenData_rows += 1
            q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
                ui.table(
                    name='issues',
                    columns=columns1,
                    rows=[ui.table_row(
                        name=str(dato[0]),
                        cells=dato,
                    )for dato in data_rows],
                    #values = ['0'],
                    groupable=True,
                    downloadable=True,
                )
            ])
            await q.page.save()
        await q.sleep(1)

async def problems(q: Q):
    print(str("starting aplication..."))
    
    global data_rows, data_rows_keycount

    q.page['meta'] = ui.meta_card(box='')         

    if not q.client.initialized:
        q.client.initialized = True
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                    ui.zone('header',size='0%'),
                    ui.zone('body',size='100%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq1', size='14%', zones=[
                            ui.zone('izq1_1',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_2',size='14%'),
                            ui.zone('izq1_3',size='14%'),
                            ui.zone('izq1_4',size= '14%'),
                            ui.zone('izq1_5',size= '14%'),
                            ui.zone('izq1_6',size= '14%'),
                            ui.zone('footer1',size= '15%')
                        ]),
                        ui.zone('der1',size='86%', zones=[
                            ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('der1_1',size='90%', zones=[
                                    ui.zone('der1_11', size='5%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_12', size='50%', direction=ui.ZoneDirection.ROW),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
                ],
            ),
        ], theme='default')
        q.page['section1'] = ui.section_card(
            box='der1_11', 
            title='PROBLEMS',
            subtitle=''
        )

        q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_12', order=1), items=[
            ui.table(
                name='issues',
                columns=columns1,
                rows=[ui.table_row(
                    name=str(dato[0]),
                    cells=dato,
                )for dato in data_rows],
                #values = ['0'],
                groupable=True,
                downloadable=True,
            )
        ])

        content = '![Adrian](http://'+ipGlobal+':10101/datasets/SeguriTech.png)'
        #content = '![Joel](http://'+ipGlobal+':10101/data/ShannonWeaver.png)'
        q.page['shannonImg'] = ui.markdown_card(
            box='izq1_1',
            title='Version 1.0 (c) 2022 Development by ',
            content= content,
        )

        await q.page.save()
        await q.run(showList,q)

@app('/problems', mode = 'broadcast')
async def team1(q: Q):
    route = q.args['#']
    await problems(q)