from plotly import graph_objects as go
from connections import tracesTP, tracesTT
import pymysql
from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import os
from ftplib import FTP
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
import time, json
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
r = ''

# Variable global para mantener la referencia de la tarea refresh
current_refresh_task = None

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

def decode_redis(src):
    if isinstance(src, list):
        rv = list()
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = dict()
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " +type(src))

subscribersHostG = []
subscribersLatG = []
subscribersLonG = []
subscribersIPG = []
subscribersHostR = []
subscribersLatR = []
subscribersLonR = []
subscribersIPR = []
data_table_stable_keycount = 0
data_table_stable = []
data_table_problem_keycount = 0
data_table_problem = []
subscribers = 0
data = {}
data1 = {}
updtd = 0
lat_media = 19.1
lon_media = -103.6
zoom_media = 11.8
stableDevices = 0
problemDevices = 0
btnPing = ''
botonShow1 = 0
botonShow2 = 0
dispositivo, locacipio = '', ''
refreshTecno, refreshMuni = '', ''

#comboboxTecno = ['ALL','AP', 'OLT', 'ONU', 'PTP', 'ROUTER', 'SWITCH']
comboboxTecno = ['ALL', 'APS PUBLICOS','OLT', 'ONU', 'ROUTER', 'SWITCH', 'RADIOGRAFIA FIBRA']
comboboxMuni = ['ALL', 'ARMERIA', 'COLIMA', 'COMALA', 'COQUIMATLAN', 'CUAUHTEMOC', 'IXTLAHUACAN', 'MANZANILLO', 'MINATITLAN', 'TECOMAN', 'VILLA DE ALVAREZ']
comboboxAll = ['ALL']
comboboxVars = ['RSSI','LSNR']

ciudad, localidad = '', ''
dataFD = ''

columns = [
    ui.table_column(name='delete', label='No.', sortable=True, searchable=True, max_width='40'),
    ui.table_column(name='text',  label='Host', sortable=True, searchable=True, max_width='630'),
    ui.table_column(name='text1', label='Afilición', sortable=True, searchable=True, max_width='200'),
    ui.table_column(name='text2', label='IP', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text3', label='Referencia', sortable=True, searchable=True, max_width='190'),
    ui.table_column(name='text4', label='Ubicación', sortable=True, searchable=True, max_width='190'),
]
###############################    P   I   N   G    ###############################
def check_ping(hostname):
    print(hostname)
    response = os.system("ping -c 2 -W 1 "+hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    return pingstatus

###############################    F    T    P    ###############################
def check_ftp(hostname):
    try:
        ftp = FTP(hostname)
        ftp.login(user='root',passwd='$3gurit3ch')
        wdir = ftp.sendcmd('site reboot')
    except Exception as e:
        print('FTP error:', e)
    time.sleep(7)
    result = check_ping(hostname)
    return result

###############################    Q    U    E    R    Y    ###############################
def doQuerySUBS():
    global r
    subs = []
    json_datos = {}
    band = 0
    #print("Get data subscribers...")
    data = decode_redis(r.hgetall('infraYI'))
    if data == {}:
        data = 'NO'
    else:
        data = json.loads(data['data'])
        pass
    for sub in range(len(data)):
        if data[sub][3] != 'PISCILA':
            if data[sub][0] != '' and data[sub][9] != '' and data[sub][10] != '' and data[sub][11] != '':
                subs.append((data[sub][0], data[sub][1], data[sub][2], data[sub][3], data[sub][4], data[sub][5], data[sub][6], data[sub][7], 
                             data[sub][8], data[sub][9], data[sub][10], data[sub][11], data[sub][12], data[sub][13], data[sub][14], data[sub][15]))
            else:
                pass
    return subs

###############################     P   O   I   N   T   S     ###############################
def pointsToMap(data):
    global fig, lat_media, lon_media, zoom_media
    fig = go.Figure(
        go.Scattermapbox(
            name= "STABLE",
            lat = data["latStable"],
            lon = data["lonStable"],
            mode = "markers",
            marker = go.scattermapbox.Marker(size=10),
            showlegend=True,
            text = [data["hostsStable"][i] + '<br>' + data["IPStable"][i] for i in range(len(data["hostsStable"]))],
            marker_color=data["statusStable"]
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            name= "PROBLEM",
            mode = "markers",
            lat = data["latProb"],
            lon = data["lonProb"],
            marker = go.scattermapbox.Marker(size=10),
            showlegend=True,
            text=[data["hostsProb"][i] + '<br>' + data["IPProb"][i] for i in range(len(data["hostsProb"]))],
            marker_color = data["statusProb"]
        )
    )
    fig.update_layout(
        hovermode='closest',
        clickmode='event+select',
        mapbox=dict(
            zoom=zoom_media,
            style="open-street-map",
            center=go.layout.mapbox.Center(lat=lat_media,lon=lon_media)
        ),
        #l = left   #t = top   #b = bottom   #r = right
        margin ={'l':0,'t':0,'b':0,'r':0}
    )
    return fig

def connectionsPoints(tech, city, loca):
    if tech == 'APS PUBLICOS':
        tech = 'APP'
    global data_table_stable, data_table_stable_keycount, data_table_problem, data_table_problem_keycount
    level = ''
    fig = 0
    data = {}
    subscribersHostG = []
    subscribersLatG = []
    subscribersLonG = []
    subscribersIPG = []
    subscribersHostR = []
    subscribersLatR = []
    subscribersLonR = []
    subscribersIPR = []
    data_table_stable_keycount = 0
    data_table_stable = []
    data_table_problem_keycount = 0
    data_table_problem = []
    subscribers = doQuerySUBS()
    #####    P  O  I  N  T  S    ####
    for x in range(len(subscribers)):
        ##### CONSULTAR TODOS LOS EQUIPOS DEL PROYECTO #####
        if tech == 'ALL' and city == 'ALL' and loca == 'ALL':
            status = rts.get(str(subscribers[x][9]))
            if status[1] > 0:
                subscribersHostG.append(subscribers[x][15])
                subscribersLatG.append(subscribers[x][10])
                subscribersLonG.append(subscribers[x][11])
                subscribersIPG.append(subscribers[x][9])
                data_table_stable_keycount += 1
                data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
            if status[1] == 0:
                subscribersHostR.append(subscribers[x][15])
                subscribersLatR.append(subscribers[x][10])
                subscribersLonR.append(subscribers[x][11])
                subscribersIPR.append(subscribers[x][9])
                data_table_problem_keycount += 1
                data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
        ##### CONSULTAR UN GRUPO DE EQUIPOS DE UN ESTADO Y MUNICIPIO DEL PROYECTO #####
        if tech == subscribers[x][6]:
            if city == subscribers[x][1]:
                if loca == subscribers[x][3]:
                    status = rts.get(str(subscribers[x][9]))
                    if status[1] > 0:
                        subscribersHostG.append(subscribers[x][15])
                        subscribersLatG.append(subscribers[x][10])
                        subscribersLonG.append(subscribers[x][11])
                        subscribersIPG.append(subscribers[x][9])
                        data_table_stable_keycount += 1
                        data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
                    if status[1] == 0:
                        subscribersHostR.append(subscribers[x][15])
                        subscribersLatR.append(subscribers[x][10])
                        subscribersLonR.append(subscribers[x][11])
                        subscribersIPR.append(subscribers[x][9])
                        data_table_problem_keycount += 1
                        data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
                ##### CONSULTAR UN GRUPO DE EQUIPOS DE UN ESTADO DEL PROYECTO #####
                elif loca == 'ALL':
                    status = rts.get(str(subscribers[x][9]))
                    if status[1] > 0:
                        subscribersHostG.append(subscribers[x][15])
                        subscribersLatG.append(subscribers[x][10])
                        subscribersLonG.append(subscribers[x][11])
                        subscribersIPG.append(subscribers[x][9])
                        data_table_stable_keycount += 1
                        data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
                    if status[1] == 0:
                        subscribersHostR.append(subscribers[x][15])
                        subscribersLatR.append(subscribers[x][10])
                        subscribersLonR.append(subscribers[x][11])
                        subscribersIPR.append(subscribers[x][9])
                        data_table_problem_keycount += 1
                        data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
            ##### CONSULTAR UN GRUPO DE EQUIPOS DE TODOS LOS ESTADOS DEL PROYECTO #####
            if city == 'ALL' and loca == 'ALL':
                status = rts.get(str(subscribers[x][9]))
                if status[1] > 0:
                    subscribersHostG.append(subscribers[x][15])
                    subscribersLatG.append(subscribers[x][10])
                    subscribersLonG.append(subscribers[x][11])
                    subscribersIPG.append(subscribers[x][9])
                    data_table_stable_keycount += 1
                    data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
                if status[1] == 0:
                    subscribersHostR.append(subscribers[x][15])
                    subscribersLatR.append(subscribers[x][10])
                    subscribersLonR.append(subscribers[x][11])
                    subscribersIPR.append(subscribers[x][9])
                    data_table_problem_keycount += 1
                    data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
        ##### CONSULTAR TODOS LOS EQUIPOS DE UN ESTADO DEL PROYECTO #####
        if tech == 'ALL' and city == subscribers[x][1] and loca == 'ALL':
            status = rts.get(str(subscribers[x][9]))
            if status[1] > 0:
                subscribersHostG.append(subscribers[x][15])
                subscribersLatG.append(subscribers[x][10])
                subscribersLonG.append(subscribers[x][11])
                subscribersIPG.append(subscribers[x][9])
                data_table_stable_keycount += 1
                data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
            if status[1] == 0:
                subscribersHostR.append(subscribers[x][15])
                subscribersLatR.append(subscribers[x][10])
                subscribersLonR.append(subscribers[x][11])
                subscribersIPR.append(subscribers[x][9])
                data_table_problem_keycount += 1
                data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
        ##### CONSULTAR TODOS LOS EQUIPOS DE UN ESTADO Y UN MUNICIPIO DEL PROYECTO #####
        if tech == 'ALL' and city == subscribers[x][1] and loca == subscribers[x][3]:
            status = rts.get(str(subscribers[x][9]))
            if status[1] > 0:
                subscribersHostG.append(subscribers[x][15])
                subscribersLatG.append(subscribers[x][10])
                subscribersLonG.append(subscribers[x][11])
                subscribersIPG.append(subscribers[x][9])
                data_table_stable_keycount += 1
                data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
            if status[1] == 0:
                subscribersHostR.append(subscribers[x][15])
                subscribersLatR.append(subscribers[x][10])
                subscribersLonR.append(subscribers[x][11])
                subscribersIPR.append(subscribers[x][9])
                data_table_problem_keycount += 1
                data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
   
    data['hostsStable'] = subscribersHostG
    data['latStable'] = subscribersLatG
    data['lonStable'] = subscribersLonG
    data['IPStable'] = subscribersIPG
    data['statusStable'] = 'green'
    data['hostsProb'] = subscribersHostR
    data['latProb'] = subscribersLatR
    data['lonProb'] = subscribersLonR
    data['IPProb'] = subscribersIPR
    data['statusProb'] = 'red'
    fig = pointsToMap(data)
    
    return fig, len(data['hostsStable']), len(data['hostsProb']), data_table_stable, data_table_problem

###############################    R A D I O G R A F I A   T O R R E S - P O S T E S     ###############################
def tracesToMap(data):
    global fig, lat_media, lon_media, zoom_media
    for x in range(len(data["latStable"])):
        if x == 0:
            fig = go.Figure(go.Scattermapbox(
                name= "Active",
                mode = "markers+lines",
                lat = [data["latStable"][x][1],data["latStable"][x][0]],
                lon = [data["lonStable"][x][1],data["lonStable"][x][0]],
                marker = {'size': 10},
                text=[data["hostsStable"][x][1]+ '<br>' + data["IPStable"][x][1]],
                marker_color='green')
            )
        if x != 0:
            fig.add_trace(go.Scattermapbox(
                name= "Active",
                mode = "markers+lines",
                lat = [data["latStable"][x][1],data["latStable"][x][0]],
                lon = [data["lonStable"][x][1],data["lonStable"][x][0]],
                marker = {'size': 10},
                text=[data["hostsStable"][x][1]+ '<br>' + data["IPStable"][x][1]],
                marker_color='green')
            )
    for z in range(len(data["latProb"])):
        fig.add_trace(go.Scattermapbox(
            name= "Offline",
            mode = "markers+lines",
            lat = [data["latProb"][z][1],data["latProb"][z][0]],
            lon = [data["lonProb"][z][1],data["lonProb"][z][0]],
            marker = {'size': 10},
            text=[data["hostsProb"][z][1]+ '<br>' + data["IPProb"][z][1]],
            marker_color='red')
        )
    fig.update_layout(
        hovermode='closest',
        clickmode='event+select',
        mapbox=dict(
            zoom=zoom_media,
            style="open-street-map",
            center=go.layout.mapbox.Center(lat=lat_media,lon=lon_media)
        ),
        #l = left   #t = top   #b = bottom   #r = right
        margin ={'l':0,'t':0,'b':0,'r':0}
    )
    return fig

def connectionsTraces(city,loca):
    global data_table_stable_keycount, data_table_stable, data_table_problem_keycount, data_table_problem
    fig = 0
    data = {}
    subscribersHostG = []
    subscribersLatG = []
    subscribersLonG = []
    subscribersIPG = []
    subscribersHostR = []
    subscribersLatR = []
    subscribersLonR = []
    subscribersIPR = []
    ipsSubs = []
    subscribers = doQuerySUBS()
    ####    T  R  A  C  E  S    ####
    bandFor = 0
    bandSubs = 0
    bandTwrs = 0
    count = 0
    for x in range(len(subscribers)):
        if city == subscribers[x][1]:
            if loca == subscribers[x][3]:
                ipSecondary = subscribers[x][9]
                latSecondary = subscribers[x][10]
                lonSecondary = subscribers[x][11]
                lvlSecondary = subscribers[x][14].split('-')
                hostSecondary = subscribers[x][15]
                for z in range(len(subscribers)):
                    if lvlSecondary[0]==subscribers[z][13] and lvlSecondary[1]==subscribers[z][12]:
                        status = rts.get(str(ipSecondary))
                        if status[1] > 0:
                            subscribersIPG.append([str("subsIP"),ipSecondary])
                            subscribersLatG.append([float(subscribers[z][10]),float(latSecondary)])
                            subscribersLonG.append([float(subscribers[z][11]),float(lonSecondary)])
                            subscribersHostG.append([str(subscribers[z][15]),hostSecondary])
                            data_table_stable_keycount += 1    
                            data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
                        if status[1] == 0:
                            subscribersIPR.append([str("subsIP"),ipSecondary])
                            subscribersLatR.append([float(subscribers[z][10]),float(latSecondary)])
                            subscribersLonR.append([float(subscribers[z][11]),float(lonSecondary)])
                            subscribersHostR.append([str(subscribers[z][15]),hostSecondary])
                            data_table_problem_keycount += 1
                            data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
            if loca == 'ALL':
                ipSecondary = subscribers[x][9]
                latSecondary = subscribers[x][10]
                lonSecondary = subscribers[x][11]
                lvlSecondary = subscribers[x][14].split('-')
                hostSecondary = subscribers[x][15]
                for z in range(len(subscribers)):
                    if lvlSecondary[0]==subscribers[z][13] and lvlSecondary[1]==subscribers[z][12]:
                        status = rts.get(str(ipSecondary))
                        if status[1] > 0:
                            subscribersIPG.append([str("subsIP"),ipSecondary])
                            subscribersLatG.append([float(subscribers[z][10]),float(latSecondary)])
                            subscribersLonG.append([float(subscribers[z][11]),float(lonSecondary)])
                            subscribersHostG.append([str(subscribers[z][15]),hostSecondary])
                            data_table_stable_keycount += 1
                            data_table_stable.append([str(data_table_stable_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
                        if status[1] == 0:
                            subscribersIPR.append([str("subsIP"),ipSecondary])
                            subscribersLatR.append([float(subscribers[z][10]),float(latSecondary)])
                            subscribersLonR.append([float(subscribers[z][11]),float(lonSecondary)])
                            subscribersHostR.append([str(subscribers[z][15]),hostSecondary])
                            data_table_problem_keycount += 1
                            data_table_problem.append([str(data_table_problem_keycount),str(subscribers[x][15]),str(subscribers[x][0]),str(subscribers[x][9]), str(subscribers[x][4]), str(subscribers[x][10]+','+subscribers[x][11])])
    
    data['hostsStable'] = subscribersHostG
    data['latStable'] = subscribersLatG
    data['lonStable'] = subscribersLonG
    data['IPStable'] = subscribersIPG
    data['statusStable'] = 'green'
    ####### OFFLINE DEVICES #########
    data['hostsProb'] = subscribersHostR
    data['latProb'] = subscribersLatR
    data['lonProb'] = subscribersLonR
    data['IPProb'] = subscribersIPR
    data['statusProb'] = 'red'
    fig = tracesToMap(data)
    return fig, len(data['hostsStable']), len(data['hostsProb']), data_table_stable, data_table_problem