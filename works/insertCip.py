from redis import StrictRedis, ConnectionError
import threading,json,time,datetime
from redistimeseries.client import Client               
from datetime import timedelta
gasGasto=0

def readTSPromed(start,end,sensor,rts):
    global gasGasto
    local_time = (datetime.datetime.strptime(str(start), '%Y-%m-%d %H:%M:%S')).timestamp()
    local_time2 = (datetime.datetime.strptime(str(end), '%Y-%m-%d %H:%M:%S')).timestamp()
    query=[]
    try:
        query=rts.range(str(sensor),int(local_time), int(local_time2))
        if str(sensor)=="BRIX02PURE":
            if len(query)==0:
                query=rts.range("BRIX01LINEA",int(local_time), int(local_time2))
    except Exception as e:
        print(e)  
    for x in range(0,int(len(query))):
        if int(query[x][1])>=0:
            if sensor=="serv_nivelg" and x==0:
                gasGasto=int(query[x][1])
            if sensor=="serv_nivelg" and x==int(len(query))-1:
                gasGasto=gasGasto-int(query[x][1])

def readTS(start,end,sensor,rts):
    local_time = (datetime.datetime.strptime(str(start), '%Y-%m-%d %H:%M:%S')).timestamp()
    local_time2 = (datetime.datetime.strptime(str(end), '%Y-%m-%d %H:%M:%S')).timestamp()
    query=[]
    try:
        query=rts.range(str(sensor),int(local_time), int(local_time2))
        if str(sensor)=="LT01TP0LT":
            if len(query)==0:
                query=rts.range("LT01TP0L",int(local_time), int(local_time2))
        if str(sensor)=="BRIX02PURE":
            if len(query)==0:
                query=rts.range("BRIX01LINEA",int(local_time), int(local_time2))
    except Exception as e:
        print(e)  
    xData=[]
    yData=[]
    for x in range(0,int(len(query))):
        if int(query[x][1])>=0:
            if sensor=="BRIX02PURE" and int(query[x][1])>0.5 and int(query[x][1])<10:
                yData.append(query[x][1])
                xData.append(datetime.datetime.fromtimestamp(query[x][0]).strftime('%Y-%m-%d %H:%M:%S'))
            if sensor!="BRIX02PURE":
                yData.append(query[x][1])
                xData.append(datetime.datetime.fromtimestamp(query[x][0]).strftime('%Y-%m-%d %H:%M:%S'))   
    sens=[]
    sens.append(xData)
    sens.append(yData)
    #print(sens)
    return sens
####################################################FUNCIONES insert_circuitos_cip_start#########################################################################
class Listener1(threading.Thread):
    def __init__(self, r,rts, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        print('Listener1...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)   

    def work2(self, item):
        data =0
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            if data["insert"]=="2":
                print("[BORRAR] cip_start_num->"+str(data["num"]))
                for x in range(0,int(data["num"])):
                    try:
                        all_keys = list(self.redis.hgetall(data["data"][x]["key"]).keys())
                        self.redis.hdel(data["data"][x]["key"], *all_keys)
                    except:
                        print("[ERROR]####################################### hdel1 "+str(data))
            if data["insert"]=="3":
                print("[ENVIAR] cip_start_key")
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    labels = {"key":"cip_start","time":str(data["data"][x]["time"]),"id":str(data["data"][x]["id"]), "area":str(data["data"][x]["area"]),"operador":str(data["data"][x]["operador"]),"key2":str(data["data"][x]["key3"]),"claveCip":str(data["data"][x]["claveCip"]),"seccion":str(data["data"][x]["seccion"])}
                    ERR=0
                    startTime=0
                    try:
                        startTime = datetime.datetime.strptime(str(data["data"][x]["time"]), '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        print(e)
                        startTime = datetime.datetime.strptime(str(data["data"][x]["time"]), '%Y_%m_%d %H:%M:%S')
                    local_time = 0
                    try:
                        local_time = int((datetime.datetime.strptime(str(startTime), '%Y-%m-%d %H:%M:%S')).timestamp())
                    except Exception as e:
                        local_time = int((datetime.datetime.strptime(str(startTime), '%Y_%m_%d %H:%M:%S')).timestamp())
                    try:
                        zkey = 'cip_start_zadd'
                        dict1 = {}
                        dict1[str(labels)] = local_time
                        r.zadd(zkey,dict1)
                        #rts.create(time.time(), labels=labels)
                    except:
                        print("[ERROR]####################################### rts.create "+str(data))
                        ERR=1
                    if ERR==0:
                        try:
                            all_keys = list(r.hgetall(str(data["data"][x]["key"])).keys())
                            r.hdel(str(data["data"][x]["key"]), *all_keys)
                        except:
                            print("[ERROR]####################################### hdel2 "+str(data))
            if data["insert"]=="1":
                print("[EDITAR] cip_start_num->"+str(data["num"]))
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    r.hset(str(data["data"][x]["key"]), "time", str(data["data"][x]["time"]))
                    r.hset(str(data["data"][x]["key"]), "id", str(data["data"][x]["id"]))
                    r.hset(str(data["data"][x]["key"]), "area", str(data["data"][x]["area"]))
                    r.hset(str(data["data"][x]["key"]), "operador", str(data["data"][x]["operador"]))
                    r.hset(str(data["data"][x]["key"]), "key2", str(data["data"][x]["key2"]))
                    r.hset(str(data["data"][x]["key"]), "claveCip", str(data["data"][x]["claveCip"]))
                    r.hset(str(data["data"][x]["key"]), "seccion", str(data["data"][x]["seccion"]))

    def work(self, item):
        data =0
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            key_count=r.get('cip_start_key')
            key_count=key_count.decode("utf-8") 
            key_count=int(key_count)+1
            print("[GUARDAR] cip_start_key->"+str(key_count))
            r.hset("cip_start_"+str(key_count), "time", str(data["time"]))
            r.hset("cip_start_"+str(key_count), "id", str(data["id"]))
            r.hset("cip_start_"+str(key_count), "area", str(data["area"]))
            r.hset("cip_start_"+str(key_count), "operador", str(data["operador"]))
            r.hset("cip_start_"+str(key_count), "key2", str(data["key"]))
            r.hset("cip_start_"+str(key_count), "claveCip", str(data["claveCip"]))
            r.hset("cip_start_"+str(key_count), "seccion", str(data["seccion"]))
            r.set("cip_start_key",key_count) 

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message["channel"].decode("utf-8")=="circuitos_cip_start":
                        self.work(message['data'])
                    if message["channel"].decode("utf-8")=="circuitos_cip_start_dash":
                        self.work2(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['circuitos_cip_start','circuitos_cip_start_dash'])
                        break
            time.sleep(0.001)  # be nice to the system :)
####################################################FUNCIONES insert_circuitos_cip_end#########################################################################
class Listener2(threading.Thread):
    def __init__(self, r,rts, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.redisTS = rts
        self.pubsub = self.redis.pubsub()
        print('Listener2...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)
    def reporte(self, data):
        print("crear reporte...")
        try:
            sens1=readTS(str(data["key2"]).replace("_","-")+" "+str(data["startPaso"]),str(data["key2"]).replace("_","-")+" "+str(data["endPaso"]),"cip_tt01",self.redisTS)
            sens2=readTS(str(data["key2"]).replace("_","-")+" "+str(data["startPaso"]),str(data["key2"]).replace("_","-")+" "+str(data["endPaso"]),"serv_nivelg",self.redisTS)
            json_datos = json.dumps({"data1":data,"sens1":sens1,"sens2":sens2})
            #print(str(json_datos))
            r.publish("CIP_reporte",json_datos)
        except Exception as e:
            print("ERROR...")
            print(e)

    def work2(self, item):
        data =0
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            if data["insert"]=="4":
                print("[PDF] cip_end_key")
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    labels = {"key":"cip_end_temp","time":str(data["data"][x]["time"]),"id":str(data["data"][x]["id"]), "area":str(data["data"][x]["area"]),"operador":str(data["data"][x]["operador"]),"key2":str(data["data"][x]["key3"]),"claveCip":str(data["data"][x]["claveCip"]),"seccion":str(data["data"][x]["seccion"]),"volEnju":str(data["data"][x]["volEnju"]),"paso":str(data["data"][x]["paso"]),"gas":str(data["data"][x]["gas"]),"gotasPq":str(data["data"][x]["gotasPq"]),"porcPq":str(data["data"][x]["porcPq"]),"dosisPq":str(data["data"][x]["dosisPq"]),"dosisUniPq":str(data["data"][x]["dosisUniPq"]),"startPaso":str(data["data"][x]["startPaso"]),"endPaso":str(data["data"][x]["endPaso"])}
                    try:
                        self.reporte(labels)
                    except Exception as e:
                        print(e) 
            if data["insert"]=="2":
                print("[BORRAR] cip_end_num->"+str(data["num"]))
                for x in range(0,int(data["num"])):
                    try:
                        all_keys = list(self.redis.hgetall(data["data"][x]["key"]).keys())
                        self.redis.hdel(data["data"][x]["key"], *all_keys)
                    except:
                        print("[ERROR]####################################### hdel1 "+str(data))
            if data["insert"]=="3":
                print("[ENVIAR] cip_end_key")
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    labels = {"key":"cip_end","time":str(data["data"][x]["time"]),"id":str(data["data"][x]["id"]), "area":str(data["data"][x]["area"]),"operador":str(data["data"][x]["operador"]),"key2":str(data["data"][x]["key3"]),"claveCip":str(data["data"][x]["claveCip"]),"seccion":str(data["data"][x]["seccion"]),"volEnju":str(data["data"][x]["volEnju"]),"paso":str(data["data"][x]["paso"]),"gas":str(data["data"][x]["gas"]),"gotasPq":str(data["data"][x]["gotasPq"]),"porcPq":str(data["data"][x]["porcPq"]),"dosisPq":str(data["data"][x]["dosisPq"]),"dosisUniPq":str(data["data"][x]["dosisUniPq"]),"startPaso":str(data["data"][x]["startPaso"]),"endPaso":str(data["data"][x]["endPaso"])}
                    try:
                        self.reporte(labels)
                    except Exception as e:
                        print(e) 
                        ERR==1
                    ERR=0
                    startTime=0
                    try:
                        startTime = datetime.datetime.strptime(str(data["data"][x]["time"]), '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        print(e)
                        startTime = datetime.datetime.strptime(str(data["data"][x]["time"]), '%Y_%m_%d %H:%M:%S')
                    local_time = 0
                    try:
                        local_time = int((datetime.datetime.strptime(str(startTime), '%Y-%m-%d %H:%M:%S')).timestamp())
                    except Exception as e:
                        local_time = int((datetime.datetime.strptime(str(startTime), '%Y_%m_%d %H:%M:%S')).timestamp())
                    try:
                        zkey = 'cip_end_zadd'
                        dict1 = {}
                        dict1[str(labels)] = local_time
                        r.zadd(zkey,dict1)
                        #rts.create(time.time(), labels=labels)
                    except:
                        print("[ERROR]####################################### rts.create "+str(data))
                        ERR=1
                    if ERR==0:
                        try:
                            all_keys = list(r.hgetall(str(data["data"][x]["key"])).keys())
                            r.hdel(str(data["data"][x]["key"]), *all_keys)
                        except:
                            print("[ERROR]####################################### hdel2 "+str(data))
            if data["insert"]=="1":
                print("[EDITAR] cip_end_num->"+str(data["num"]))
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    r.hset(str(data["data"][x]["key"]), "time", str(data["data"][x]["time"]))
                    r.hset(str(data["data"][x]["key"]), "id", str(data["data"][x]["id"]))
                    r.hset(str(data["data"][x]["key"]), "area", str(data["data"][x]["area"]))
                    r.hset(str(data["data"][x]["key"]), "operador", str(data["data"][x]["operador"]))
                    r.hset(str(data["data"][x]["key"]), "key2", str(data["data"][x]["key2"]))
                    r.hset(str(data["data"][x]["key"]), "claveCip", str(data["data"][x]["claveCip"]))
                    r.hset(str(data["data"][x]["key"]), "seccion", str(data["data"][x]["seccion"]))
                    r.hset(str(data["data"][x]["key"]), "volEnju", str(data["data"][x]["volEnju"]))
                    r.hset(str(data["data"][x]["key"]), "paso", str(data["data"][x]["paso"]))
                    r.hset(str(data["data"][x]["key"]), "gas", str(data["data"][x]["gas"]))
                    r.hset(str(data["data"][x]["key"]), "gotasPq", str(data["data"][x]["gotasPq"]))
                    r.hset(str(data["data"][x]["key"]), "porcPq", str(data["data"][x]["porcPq"]))
                    r.hset(str(data["data"][x]["key"]), "dosisPq", str(data["data"][x]["dosisPq"]))
                    r.hset(str(data["data"][x]["key"]), "dosisUniPq", str(data["data"][x]["dosisUniPq"]))
                    r.hset(str(data["data"][x]["key"]), "startPaso", str(data["data"][x]["startPaso"]))
                    r.hset(str(data["data"][x]["key"]), "endPaso", str(data["data"][x]["endPaso"]))

    def work(self, item):
        data =0
        global gasGasto
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            gasGasto=0
            tm1=str(data["key"]).replace("_","-")+" "+str(data["startPaso"])
            tm2=str(data["key"]).replace("_","-")+" "+str(data["endPaso"])
            date1 = datetime.datetime.strptime(tm1, '%Y-%m-%d %H:%M:%S')
            date2 = datetime.datetime.strptime(tm2, '%Y-%m-%d %H:%M:%S')
            if date1 > date2:
                d2=str(date2 + timedelta(days=1))
                tm2=str(d2)
            print(str(tm1))
            print(str(tm2))
            readTSPromed(str(tm1),str(tm2),"serv_nivelg",self.redisTS)
            print(str(gasGasto))

            key_count=r.get('cip_end_key')
            key_count=key_count.decode("utf-8") 
            key_count=int(key_count)+1
            print("[GUARDAR] cip_end_key->"+str(key_count))
            r.hset("cip_end_"+str(key_count), "time", str(data["time"]))
            r.hset("cip_end_"+str(key_count), "id", str(data["id"]))
            r.hset("cip_end_"+str(key_count), "area", str(data["area"]))
            r.hset("cip_end_"+str(key_count), "operador", str(data["operador"]))
            r.hset("cip_end_"+str(key_count), "key2", str(data["key"]))
            r.hset("cip_end_"+str(key_count), "claveCip", str(data["claveCip"]))
            r.hset("cip_end_"+str(key_count), "seccion", str(data["seccion"]))
            r.hset("cip_end_"+str(key_count), "volEnju", str(data["volEnju"]))
            r.hset("cip_end_"+str(key_count), "paso", str(data["paso"]))
            r.hset("cip_end_"+str(key_count), "gas", str(gasGasto))
            r.hset("cip_end_"+str(key_count), "gotasPq", str(data["gotasPq"]))
            r.hset("cip_end_"+str(key_count), "porcPq", str(data["porcPq"]))
            r.hset("cip_end_"+str(key_count), "dosisPq", str(data["dosisPq"]))
            r.hset("cip_end_"+str(key_count), "dosisUniPq", str(data["dosisUniPq"]))
            r.hset("cip_end_"+str(key_count), "startPaso", str(data["startPaso"]))
            r.hset("cip_end_"+str(key_count), "endPaso", str(data["endPaso"]))
            r.set("cip_end_key",key_count) 

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message["channel"].decode("utf-8")=="circuitos_cip_end":
                        self.work(message['data'])
                    if message["channel"].decode("utf-8")=="circuitos_cip_end_dash":
                        self.work2(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['circuitos_cip_end','circuitos_cip_end_dash'])
                        break
            time.sleep(0.001)  # be nice to the system :)

####################################################FUNCIONES insert_filtros_cip_end#########################################################################
class Listener3(threading.Thread):
    def __init__(self, r,rts, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        print('Listener3...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)   

    def work2(self, item):
        data =0
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            if data["insert"]=="2":
                print("[BORRAR] filtros_end_num->"+str(data["num"]))
                for x in range(0,int(data["num"])):
                    try:
                        all_keys = list(self.redis.hgetall(data["data"][x]["key"]).keys())
                        self.redis.hdel(data["data"][x]["key"], *all_keys)
                    except:
                        print("[ERROR]####################################### hdel1 "+str(data))
            if data["insert"]=="3":
                print("[ENVIAR] filtros_end_key")
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    labels = {"key":"filtros_end","time":str(data["data"][x]["time"]),"id":str(data["data"][x]["id"]), "area":str(data["data"][x]["area"]),"operador":str(data["data"][x]["operador"]),"key2":str(data["data"][x]["key3"]),"sitio":str(data["data"][x]["sitio"]),"nombreFil":str(data["data"][x]["nombreFil"]),"micraje":str(data["data"][x]["micraje"]),"startPaso":str(data["data"][x]["startPaso"]),"endPaso":str(data["data"][x]["endPaso"])}
                    ERR=0
                    startTime=0
                    try:
                        startTime = datetime.datetime.strptime(str(data["data"][x]["time"]), '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        print(e)
                        startTime = datetime.datetime.strptime(str(data["data"][x]["time"]), '%Y_%m_%d %H:%M:%S')
                    local_time = 0
                    try:
                        local_time = int((datetime.datetime.strptime(str(startTime), '%Y-%m-%d %H:%M:%S')).timestamp())
                    except Exception as e:
                        local_time = int((datetime.datetime.strptime(str(startTime), '%Y_%m_%d %H:%M:%S')).timestamp())
                    try:
                        zkey = 'filtros_end_zadd'
                        dict1 = {}
                        dict1[str(labels)] = local_time
                        r.zadd(zkey,dict1)
                        #rts.create(time.time(), labels=labels)
                    except:
                        print("[ERROR]####################################### rts.create "+str(data))
                        ERR=1
                    if ERR==0:
                        try:
                            all_keys = list(r.hgetall(str(data["data"][x]["key"])).keys())
                            r.hdel(str(data["data"][x]["key"]), *all_keys)
                        except:
                            print("[ERROR]####################################### hdel2 "+str(data))
            if data["insert"]=="1":
                print("[EDITAR] filtros_end_num->"+str(data["num"]))
                for x in range(0,int(data["num"])):
                    print("key->"+str(data["data"][x]["key"]))
                    r.hset(str(data["data"][x]["key"]), "time", str(data["data"][x]["time"]))
                    r.hset(str(data["data"][x]["key"]), "id", str(data["data"][x]["id"]))
                    r.hset(str(data["data"][x]["key"]), "area", str(data["data"][x]["area"]))
                    r.hset(str(data["data"][x]["key"]), "operador", str(data["data"][x]["operador"]))
                    r.hset(str(data["data"][x]["key"]), "key2", str(data["data"][x]["key2"]))
                    r.hset(str(data["data"][x]["key"]), "sitio", str(data["data"][x]["sitio"]))
                    r.hset(str(data["data"][x]["key"]), "nombreFil", str(data["data"][x]["nombreFil"]))
                    r.hset(str(data["data"][x]["key"]), "micraje", str(data["data"][x]["micraje"]))
                    r.hset(str(data["data"][x]["key"]), "startPaso", str(data["data"][x]["startPaso"]))
                    r.hset(str(data["data"][x]["key"]), "endPaso", str(data["data"][x]["endPaso"]))

    def work(self, item):
        data =0
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            key_count=r.get('filtros_end_key')
            key_count=key_count.decode("utf-8") 
            key_count=int(key_count)+1
            print("[GUARDAR] filtros_end_key->"+str(key_count))
            r.hset("filtros_end_"+str(key_count), "time", str(data["time"]))
            r.hset("filtros_end_"+str(key_count), "id", str(data["id"]))
            r.hset("filtros_end_"+str(key_count), "area", str(data["area"]))
            r.hset("filtros_end_"+str(key_count), "operador", str(data["operador"]))
            r.hset("filtros_end_"+str(key_count), "key2", str(data["key"]))
            r.hset("filtros_end_"+str(key_count), "sitio", str(data["sitio"]))
            r.hset("filtros_end_"+str(key_count), "nombreFil", str(data["nombreFil"]))
            r.hset("filtros_end_"+str(key_count), "micraje", str(data["micraje"]))
            r.hset("filtros_end_"+str(key_count), "startPaso", str(data["startPaso"]))
            r.hset("filtros_end_"+str(key_count), "endPaso", str(data["endPaso"]))
            r.set("filtros_end_key",key_count) 

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message["channel"].decode("utf-8")=="filtros_cip_end":
                        self.work(message['data'])
                    if message["channel"].decode("utf-8")=="filtros_cip_end_dash":
                        self.work2(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['filtros_cip_end','filtros_cip_end_dash'])
                        break
            time.sleep(0.001)  # be nice to the system :)

class timer1(threading.Thread):
    def __init__(self,r3):
        threading.Thread.__init__(self)
        while 1:
            time.sleep(15)
            try:
                r3.publish("insertCip_online",1)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    try:
        r = StrictRedis(host='192.168.2.115',port=6379,db=0,health_check_interval=30,socket_keepalive=True)
    except Exception as e:
        print(e)   
    try:
        rts = Client(host="192.168.2.115",port=6379,socket_keepalive=True,retry_on_timeout=True)
    except Exception as e:
        print(e)   

    client1 = Listener1(r,rts, ['circuitos_cip_start','circuitos_cip_start_dash'])
    client1.start()
    client2 = Listener2(r,rts, ['circuitos_cip_end','circuitos_cip_end_dash'])
    client2.start()
    client3 = Listener3(r,rts, ['filtros_cip_end','filtros_cip_end_dash'])
    client3.start()

    t1 = timer1(r)
    t1.start()