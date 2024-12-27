from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch,mm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.graphics.charts.lineplots import SimpleTimeSeriesPlot
from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.shapes import Drawing
from datetime import datetime
import io, sys
from io import StringIO
import pandas as pd
from redis import StrictRedis, ConnectionError
import threading,json,time
from redistimeseries.client import Client

####################################################FUNCIONES insert_filtros_cip_end#########################################################################
class Listener1(threading.Thread):
    def __init__(self, r,redisclientrts, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.redisclientrts=redisclientrts
        self.pubsub = self.redis.pubsub()
        print('Listener1...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)   

    def work(self, item):
        data =0
        try:
          data = json.loads(item.decode('utf8'))
          makePR(data)
        except:
            pass

    def work2(self, item):
        data =0
        try:
          data = json.loads(item.decode('utf8'))
          makeRecepcion(data)
        except:
            pass

    def work3(self, item):
        data =0
        try:
          data = json.loads(item.decode('utf8'))
          makeAsignacion(data)
        except:
            pass

    def work4(self, item):
        data =0
        try:
          data = json.loads(item.decode('utf8'))
          makeDevolucion(data)
        except:
            pass

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message["channel"].decode("utf-8")=="yi_pdfs_prs":
                        self.work(message['data'])
                    if message["channel"].decode("utf-8")=="yi_pdfs_recepcion":
                        self.work2(message['data'])
                    if message["channel"].decode("utf-8")=="yi_pdfs_asignacion":
                        self.work3(message['data'])
                    if message["channel"].decode("utf-8")=="yi_pdfs_devolucion":
                        self.work4(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['yi_pdfs_prs', 'yi_pdfs_recepcion', 'yi_pdfs_asignacion', 'yi_pdfs_devolucion'])
                        break
            time.sleep(0.001)  # be nice to the system :)

def _header_footer_portrait(canvas,doc):
  #guardamos el estado de nuestro canvas , para poder dibujar en el 
  canvas.saveState()
  styles = getSampleStyleSheet()

  #header
  header = Image('header-footer/leftHeader.png')
  header.drawHeight = 60
  header.drawWidth = 150
  header.hAlign = 'LEFT'
  w , h = header.wrapOn(doc,doc.width , doc.topMargin)
  header.drawOn(canvas , doc.leftMargin , 720)

  header2 = Image('header-footer/yaainternet.png')
  header2.drawHeight = 90
  header2.drawWidth = 115
  header2.hAlign = 'CENTER'
  w , h = header2.wrapOn(doc,doc.width , doc.topMargin)
  header2.drawOn(canvas, 250,690)

  header3 = Image('header-footer/rightHeader.png')
  header3.drawHeight = 60
  header3.drawWidth = 150
  header3.hAlign = 'RIGHT'
  w , h = header3.wrapOn(doc,doc.width , doc.topMargin)
  header3.drawOn(canvas , 450 , 720)

  # Footer
  header4 = Image('header-footer/leftFooter.png')
  header4.drawHeight = 60
  header4.drawWidth = 170
  header4.hAlign = 'LEFT'
  w , h = header4.wrapOn(doc,doc.width , doc.bottomMargin)
  header4.drawOn(canvas , doc.leftMargin ,10)

  header5 = Image('header-footer/direccion.png')
  header5.drawHeight = 35
  header5.drawWidth = 170
  header5.hAlign = 'LEFT'
  w , h = header5.wrapOn(doc,doc.width , doc.bottomMargin)
  header5.drawOn(canvas , 240 ,10)

  header6 = Image('header-footer/rightFooter.png')
  header6.drawHeight = 30
  header6.drawWidth = 140
  header6.hAlign = 'RIGHT'
  w , h = header6.wrapOn(doc,doc.width , doc.bottomMargin)
  header6.drawOn(canvas, 460,10)

  # Release the canvas
  canvas.restoreState()

##########################    P   D   F   -  P    R    #####################################
def makePR(data):
  import base64

  data2, descripcionT, cantidadT, costoT, totalT = [], '''''', '''''','''''',''''''
  proyecto = data['proyecto']
  encargado = data['encargado']
  noPR = data['noPR']
  fechaPR = data['fecha']
  totalPR = data['totalPR']
  listaCompra = data['lista'].replace("'","[")
  listaCompra1 = json.loads(listaCompra)
  routePDF = '/home/adrian/ws/wave/cassia/apps/pdfs/prs/docs/'
  extensionDoc = '.pdf'
  now = datetime.now()
  spaceBR='''<br></br>'''
  ########################## D O C U M E N T O #######################################    
  doc = SimpleDocTemplate(routePDF+noPR+extensionDoc, pagesize=letter, rightMargin=10,leftMargin=10, topMargin=10,bottomMargin=10)
  document = []
  ########################## ESTILOS DE PARRAFOS #####################################
  styles1 = getSampleStyleSheet()
  styleN = styles1["BodyText"]
  styleN.alignment = TA_CENTER
  styleN.splitLongWords = True
  timeDate = now.strftime('%d/%m/%Y %H:%M:%S')

  b = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/hsm.jpg')  
  b.drawHeight = 0.5*inch
  b.drawWidth = 1.3*inch
  b.alignment = TA_CENTER
  c = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/pl.jpg')  
  c.drawHeight = 0.5*inch
  c.drawWidth = 1.3*inch
  c.alignment = TA_CENTER
  empresa = '''Yaa Internet'''
  areajefe = '''Dirección General'''
  area = '''Medios Impresos'''
  nombre='''<b>Arq. Eddy Romero</b>'''
  nombre1='''<b>Ing. Marco Antonio Espindola</b>'''
  ########################## P A R R A F O S #########################################
  hclave = Paragraph('''Clave''', styleN)
  hversion = Paragraph('''Versión''', styleN)
  hfecha = Paragraph('''Fecha de emisión''', styleN)
  hpagina = Paragraph('''Página''', styleN)
  clave = Paragraph('''FOR-OP-01-01''', styleN)
  version = Paragraph('''1''', styleN)
  fecha = Paragraph('''02-Mayo-2024''', styleN)
  pagina = Paragraph('''1 de 1''', styleN)
  ##################### CAMPOS TABLA ####################
  hconcepto = Paragraph('''<b>Descripción</b>''', styleN)
  hcantidad = Paragraph('''<b>Cantidad</b>''', styleN)
  hcosto = Paragraph('''<b>Costo</b>''', styleN)
  htotal = Paragraph('''<b>Total</b>''', styleN)
  ##################### CONTENIDO TABLA ####################
  #for x in range(0,len(listaCompra1)):
  #  descripcionT = str(listaCompra1[x][4])
  #  cantidadT = str(listaCompra1[x][5])
  #  costoT = str(listaCompra1[x][6])
  #  totalT = str(listaCompra1[x][8])
  #  data2.append([descripcionT,cantidadT,costoT,totalT])
  # Definir un estilo de párrafo para las celdas de la tabla
  cell_style = ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=10)

  # Crear data2 con párrafos justificados
  data2 = [[Paragraph(str(listaCompra1[x][4]), cell_style),
            Paragraph(str(listaCompra1[x][5]), cell_style),
            Paragraph(str(listaCompra1[x][6]), cell_style),
            Paragraph(str(listaCompra1[x][8]), cell_style)] for x in range(len(listaCompra1))]

  hconcepto = Paragraph('''<b>Descripción</b>''', styleN)
  hcantidad = Paragraph('''<b>Cantidad</b>''', styleN)
  ##################### CAMPOS FIRMAS ####################
  hrecibido = Paragraph('''<b>Elaboró:</b>''', styleN)
  hvobo = Paragraph('''<b>Autorizó:</b>''', styleN)
  recibido = Paragraph(nombre+spaceBR+area+spaceBR+empresa,styleN)
  vobo = Paragraph(nombre1+spaceBR+areajefe+spaceBR+empresa,styleN)
  ################# PARRAFOS SEPARADOS ###################
  p_text0 = Paragraph("REQUESICIÓN DE SERVICIOS",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                fontName='Helvetica-Bold',wordWrap='LTR',
                                                                alignment=TA_CENTER,fontSize=12,
                                                                leading=15,textColor=colors.black,
                                                                borderPadding=0,leftIndent=0,
                                                                rightIndent=0,spaceAfter=0,
                                                                spaceBefore=0,splitLongWords=False,
                                                                spaceShrinkage=0.05,))

  p_text1 = Paragraph("SOLICITUD DE COMPRA",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_CENTER,fontSize=12,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=0,
                                                          rightIndent=0,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))

  p_text2 = Paragraph("Fecha de solicitud: "+fechaPR,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                    fontName='Helvetica',wordWrap='LTR',
                                                                    alignment=TA_RIGHT,fontSize=12,
                                                                    leading=15,textColor=colors.black,
                                                                    borderPadding=0,leftIndent=30,
                                                                    rightIndent=35,spaceAfter=0,
                                                                    spaceBefore=0,splitLongWords=False,
                                                                    spaceShrinkage=0.05,))

  p_text3 = Paragraph("Proyecto: "+proyecto,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_LEFT,fontSize=12,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=30,
                                                          rightIndent=35,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))

  p_text4 = Paragraph("Encargado: "+encargado,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=12,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=30,
                                                            rightIndent=35,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))

  p_text5 = Paragraph("N° PR: "+noPR,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica-Bold',wordWrap='LTR',
                                                    alignment=TA_LEFT,fontSize=12,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=30,
                                                    rightIndent=35,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))

  p_text6 = Paragraph("Total estimado de la solicitud: "+totalPR,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                                fontName='Helvetica-Bold',wordWrap='LTR',
                                                                                alignment=TA_LEFT,fontSize=12,
                                                                                leading=15,textColor=colors.black,
                                                                                borderPadding=0,leftIndent=30,
                                                                                rightIndent=35,spaceAfter=0,
                                                                                spaceBefore=0,splitLongWords=False,
                                                                                spaceShrinkage=0.05,))
  ################ T A B L A S ################
  t=Table([[p_text0]], colWidths=180*mm)
  t_style = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT")])
  t.setStyle(t_style)

  data = [[hclave, hversion, hfecha,hpagina], [clave, version, fecha,pagina]]
  t1 = Table(data, colWidths=45*mm)
  t1.setStyle(t_style)

  t1_w = 3.5 * inch
  t2_w = 1.3 * inch
  t3_w = 1.3 * inch
  t4_w = 1.3 * inch

  data1 = [[hconcepto,hcantidad,hcosto,htotal]]
  t2 = Table(data1, colWidths=[t1_w, t2_w,t3_w,t4_w],rowHeights=5*mm)
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t2.setStyle(t_style2)

  t1_w1 = 3.5 * inch
  t2_w1 = 1.3 * inch
  t3_w1 = 1.3 * inch
  t4_w1 = 1.3 * inch
  
  # Crear la tabla t3 con las celdas ajustadas
  t3 = Table(data2, colWidths=[t1_w1, t2_w1, t3_w1, t4_w1], hAlign='CENTER')
  t_style3 = TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                         ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                         ("BACKGROUND", (0, 0), (-1, -1), '#ffffff')])
  t3.setStyle(t_style3)

  data3 = [[hrecibido,hvobo]]
  t5 = Table(data3, colWidths=90*mm,rowHeights=5*mm)
  t_style1 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t5.setStyle(t_style1)

  data4 = [[b,c]]
  tb = Table(data4, colWidths=90*mm,rowHeights=14*mm,hAlign='CENTER')
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  tb.setStyle(t_style2)

  data5 = [[recibido,vobo]]
  t6 = Table(data5, colWidths=90*mm,rowHeights=13*mm)
  t6.setStyle(t_style)
  ################ B U I L D ##############
  document.append(Spacer(1,90))
  document.append(t)
  ###### ENCABEZADO ARCHIVO ######
  document.append(t1)
  document.append(Spacer(1,10))
  ####  TITULO DE ARCHIVO ####
  document.append(p_text1)
  document.append(Spacer(1,5))
  ####FECHA###
  document.append(p_text2)
  document.append(Spacer(1,10))
  document.append(p_text3)
  document.append(p_text4)
  document.append(p_text5)
  document.append(p_text6)
  document.append(Spacer(1,10))
  #### ENCABEZADO DE TABLA ####
  document.append(t2)
  document.append(t3)
  document.append(Spacer(1,30))
  #### FIRMAS ####
  document.append(t5)
  document.append(tb)
  document.append(t6)
  doc.build(document,onFirstPage=_header_footer_portrait,onLaterPages=_header_footer_portrait)
  rootDoc = {'rutaDoc':routePDF+noPR+extensionDoc}
  rootDoc = json.dumps(rootDoc)
  rutaDocument = routePDF+noPR+extensionDoc
  # Leer el archivo PDF
  with open(rutaDocument, 'rb') as file:
      pdf_data = file.read()
  ### Codificar el PDF en base64
  pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
  ## Guardar el PDF codificado en Redis
  r.set(noPR, pdf_base64)
  try:
    result = r.publish("downloadFile",rootDoc)
    time.sleep(0.3)
  except Exception as e:
    print(e)

  ##########################    P   D   F   -  R   E   C   E   P   C   I   O   N    #####################################
def makeRecepcion(data):
  import base64
  data2, fechaT, noPRT, proyectoT, marcaT, modeloT, descripcionT, garantiaT, noserieT, miscT, fullname, puesto = [], '''''', '''''','''''','''''','''''','''''','''''','''''','''''','''''',''''''
  #proyecto = 'TECOMAN'
  #encargado = 'Jesús Adrián Rojas Hernández'
  #noPR = '20240516-1'
  #fechaPR = '2024-05-16 18:52:19'
  #listaRecepcion = [['2024-06-05 12:23:46', '20240516-1', 'TECOMAN', 'Ubiquiti', 'Módulo Transceptor UFiber', 'SFP+ 10G', '1A', 'T5614T516RFA645FRAS64', '20240516-1/TECOMAN/Ubiquiti/Módulo Transceptor UFiber/SFP+ 10G/T5614T516RFA645FRAS64/20240605', 'Misc'], ['2024-06-05 12:23:52', '20240516-1', 'TECOMAN', 'Mikrotik', 'RB4011iGS', 'ROUTER 10 PUERTOS', '1A', '86RGS4SA6R84GR8S64A', '20240516-1/TECOMAN/Mikrotik/RB4011iGS/ROUTER 10 PUERTOS/86RGS4SA6R84GR8S64A/20240605', 'Misc']]
  proyecto = data['proyecto']
  encargado = data['encargado']
  noPR = data['noPR']
  fechaPR = data['fecha']
  listaRecepcion = data['lista']
  fullname = data['fullname']
  puesto = data['puesto']
  routePDF = '/home/adrian/ws/wave/cassia/apps/pdfs/prs/docs/'
  extensionDoc = '.pdf'
  now = datetime.now()
  spaceBR='''<br></br>'''
  ########################## D O C U M E N T O #######################################    
  doc = SimpleDocTemplate(routePDF+noPR+'-recep'+extensionDoc,pagesize=letter, rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
  document = []
  ########################## ESTILOS DE PARRAFOS #####################################
  styles1 = getSampleStyleSheet()
  styleN = styles1["BodyText"]
  styleN.alignment = TA_CENTER
  styleN.splitLongWords = True
  timeDate = now.strftime('%d/%m/%Y %H:%M:%S')

  b = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/pl.jpg')  
  b.drawHeight = 0.5*inch
  b.drawWidth = 1.3*inch
  b.alignment = TA_CENTER
  c = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/blank.png')  
  c.drawHeight = 0.5*inch
  c.drawWidth = 1.3*inch
  c.alignment = TA_CENTER
  empresa = '''Yaa Internet'''
  area = puesto
  nombre=fullname
  ########################## P A R R A F O S #########################################
  hclave = Paragraph('''Clave''', styleN)
  hversion = Paragraph('''Versión''', styleN)
  hfecha = Paragraph('''Fecha de emisión''', styleN)
  hpagina = Paragraph('''Página''', styleN)
  clave = Paragraph('''FOR-OP-02-01''', styleN)
  version = Paragraph('''1''', styleN)
  fecha = Paragraph('''02-Mayo-2024''', styleN)
  pagina = Paragraph('''1 de 1''', styleN)
  ##################### CAMPOS TABLA ####################
  hmarca = Paragraph('''<b>Marca</b>''', styleN)
  hmodelo = Paragraph('''<b>Modelo</b>''', styleN)
  hdescripcion = Paragraph('''<b>Descripción</b>''', styleN)
  hgarantia = Paragraph('''<b>Garantia</b>''', styleN)
  hnoserie = Paragraph('''<b>N° Serie</b>''', styleN)
  hmisc = Paragraph('''<b>Misc</b>''', styleN)
  ##################### CONTENIDO TABLA ####################
  for x in range(0,len(listaRecepcion)):
    marcaT = str(listaRecepcion[x][3])
    modeloT = str(listaRecepcion[x][4])
    descripcionT = str(listaRecepcion[x][5])
    garantiaT = str(listaRecepcion[x][6])
    noserieT = str(listaRecepcion[x][7])
    miscT = str(listaRecepcion[x][9])
    data2.append([marcaT, modeloT, descripcionT, garantiaT, noserieT, miscT])
  ##################### CAMPOS FIRMAS ####################
  hrecibido = Paragraph('''<b>Recibe y autoriza:</b>''', styleN)
  recibido = Paragraph(nombre+spaceBR+area+spaceBR+empresa,styleN)
  ################# PARRAFOS SEPARADOS ###################
  p_text0 = Paragraph("REQUESICIÓN DE SERVICIOS",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                fontName='Helvetica-Bold',wordWrap='LTR',
                                                                alignment=TA_CENTER,fontSize=12,
                                                                leading=15,textColor=colors.black,
                                                                borderPadding=0,leftIndent=0,
                                                                rightIndent=0,spaceAfter=0,
                                                                spaceBefore=0,splitLongWords=False,
                                                                spaceShrinkage=0.05,))

  p_text1 = Paragraph("ENTRADA DE MERCANCIA",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_CENTER,fontSize=12,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=0,
                                                          rightIndent=0,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))

  p_text2 = Paragraph("Fecha de solicitud: "+fechaPR,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                    fontName='Helvetica',wordWrap='LTR',
                                                                    alignment=TA_RIGHT,fontSize=12,
                                                                    leading=15,textColor=colors.black,
                                                                    borderPadding=0,leftIndent=30,
                                                                    rightIndent=35,spaceAfter=0,
                                                                    spaceBefore=0,splitLongWords=False,
                                                                    spaceShrinkage=0.05,))

  p_text3 = Paragraph("Proyecto: "+proyecto,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_LEFT,fontSize=12,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=30,
                                                          rightIndent=35,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))

  p_text4 = Paragraph("Encargado: "+encargado,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=12,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=30,
                                                            rightIndent=35,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))

  p_text5 = Paragraph("N° PR: "+noPR,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica-Bold',wordWrap='LTR',
                                                    alignment=TA_LEFT,fontSize=12,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=30,
                                                    rightIndent=35,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))

  ################ T A B L A S ################
  t=Table([[p_text0]], colWidths=180*mm)
  t_style = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT")])
  t.setStyle(t_style)

  data = [[hclave, hversion, hfecha,hpagina], [clave, version, fecha,pagina]]
  t1 = Table(data, colWidths=45*mm)
  t1.setStyle(t_style)

  t1_w = 1 * inch
  t2_w = 2 * inch
  t3_w = 1.8 * inch
  t4_w = 0.75 * inch
  t5_w = 1.8 * inch
  t6_w = 0.6 * inch

  data1 = [[hmarca,hmodelo,hdescripcion,hgarantia,hnoserie,hmisc]]
  t2 = Table(data1, colWidths=[t1_w, t2_w,t3_w,t4_w,t5_w,t6_w],rowHeights=5*mm)
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t2.setStyle(t_style2)

  t3 = Table(data2, colWidths=[t1_w, t2_w, t3_w, t4_w,t5_w,t6_w],rowHeights=7*mm,hAlign='CENTER')
  t_style3 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t3.setStyle(t_style3)

  data3 = [[hrecibido]]
  t5 = Table(data3, colWidths=90*mm,rowHeights=5*mm)
  t_style1 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t5.setStyle(t_style1)

  data4 = [[b]]
  tb = Table(data4, colWidths=90*mm,rowHeights=14*mm,hAlign='CENTER')
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  tb.setStyle(t_style2)

  data5 = [[recibido]]
  t6 = Table(data5, colWidths=90*mm,rowHeights=13*mm)
  t6.setStyle(t_style)
  ################ B U I L D ##############
  document.append(Spacer(1,90))
  document.append(t)
  ###### ENCABEZADO ARCHIVO ######
  document.append(t1)
  document.append(Spacer(1,10))
  ####  TITULO DE ARCHIVO ####
  document.append(p_text1)
  document.append(Spacer(1,5))
  ####FECHA###
  document.append(p_text2)
  document.append(Spacer(1,10))
  document.append(p_text3)
  document.append(p_text4)
  document.append(p_text5)
  document.append(Spacer(1,10))
  #### ENCABEZADO DE TABLA ####
  document.append(t2)
  document.append(t3)
  document.append(Spacer(1,30))
  #### FIRMAS ####
  document.append(t5)
  document.append(tb)
  document.append(t6)
  doc.build(document,onFirstPage=_header_footer_portrait,onLaterPages=_header_footer_portrait)
  rootDoc = {'rutaDoc':routePDF+noPR+extensionDoc}
  rootDoc = json.dumps(rootDoc)
  rutaDocument = routePDF+noPR+extensionDoc
  # Leer el archivo PDF
  with open(rutaDocument, 'rb') as file:
      pdf_data = file.read()
  ### Codificar el PDF en base64
  pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
  ## Guardar el PDF codificado en Redis
  r.set(noPR, pdf_base64)
  try:
    result = r.publish("downloadFileRecep",rootDoc)
    time.sleep(0.3)
  except Exception as e:
    print(e)

  ##########################    P   D   F   -  R   E   C   E   P   C   I   O   N    #####################################
def makeAsignacion(data):
  import base64
  data2, noDevT, noserieT, proyectoT, marcaT, modeloT, descripcionT, garantiaT  = [], '''''', '''''','''''','''''','''''','''''',''''''
  usuarioA = data['usuarioA']
  puestoA = data['puestoA']
  listaAsignacion = data['lista']
  now = datetime.now()
  timeDate = now.strftime('%d-%m-%Y %H:%M:%S')
  routePDF = '/home/adrian/ws/wave/cassia/apps/pdfs/prs/docs/'
  extensionDoc = '.pdf'
  spaceBR='''<br></br>'''
  ########################## D O C U M E N T O #######################################    
  doc = SimpleDocTemplate(routePDF+timeDate+'-'+usuarioA+'-asig'+extensionDoc,pagesize=letter, rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
  document = []
  ########################## ESTILOS DE PARRAFOS #####################################
  styles1 = getSampleStyleSheet()
  styleN = styles1["BodyText"]
  styleN.alignment = TA_CENTER
  styleN.splitLongWords = True
  styleBH = styles1["Normal"]
  styleBH.alignment = TA_CENTER

  b = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/pl.jpg')  
  b.drawHeight = 0.5*inch
  b.drawWidth = 1.3*inch
  b.alignment = TA_CENTER
  c = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/blank.png')  
  c.drawHeight = 0.5*inch
  c.drawWidth = 1.3*inch
  c.alignment = TA_CENTER
  empresa = '''Yaa Internet'''
  areaEntrega = '''Encargado de Almacen'''
  nombreEntrega = '''Neza Almacen'''
  areaRecibe = puestoA
  nombreRecibe = usuarioA
  ########################## P A R R A F O S #########################################
  hclave = Paragraph('''Clave''', styleN)
  hversion = Paragraph('''Versión''', styleN)
  hfecha = Paragraph('''Fecha de emisión''', styleN)
  hpagina = Paragraph('''Página''', styleN)
  clave = Paragraph('''FOR-OP-03-01''', styleN)
  version = Paragraph('''1''', styleN)
  fecha = Paragraph('''02-Mayo-2024''', styleN)
  pagina = Paragraph('''1 de 1''', styleN)
  ##################### CAMPOS TABLA ####################
  hnodev = Paragraph('''<b>N°</b>''', styleN)
  hnoserie = Paragraph('''<b>N° Serie</b>''', styleN)
  hproyecto = Paragraph('''<b>Proyecto</b>''', styleN)
  hmarca = Paragraph('''<b>Marca</b>''', styleN)
  hmodelo = Paragraph('''<b>Modelo</b>''', styleN)
  hdescripcion = Paragraph('''<b>Descripción</b>''', styleN)
  hgarantia = Paragraph('''<b>Garantia</b>''', styleN)
  ##################### CONTENIDO TABLA ####################
  for x in range(0,len(listaAsignacion)):
    noDevT = str(listaAsignacion[x][0])
    noserieT = str(listaAsignacion[x][1])
    proyectoT = str(listaAsignacion[x][2])
    marcaT = str(listaAsignacion[x][3])
    modeloT = str(listaAsignacion[x][4])
    descripcionT = str(listaAsignacion[x][5])
    garantiaT = str(listaAsignacion[x][6])
    data2.append([noDevT, noserieT, proyectoT, marcaT, modeloT, descripcionT, garantiaT])
  ##################### CAMPOS FIRMAS ####################
  hentrega = Paragraph('''<b>Entrega:</b>''', styleN)
  entrega = Paragraph(nombreEntrega+spaceBR+areaEntrega+spaceBR+empresa,styleN)
  hrecibe = Paragraph('''<b>Recibe:</b>''', styleN)
  recibe = Paragraph(nombreRecibe+spaceBR+areaRecibe+spaceBR+empresa,styleN)
  ################# PARRAFOS SEPARADOS ###################
  p_text0 = Paragraph("REQUESICIÓN DE SERVICIOS",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                fontName='Helvetica-Bold',wordWrap='LTR',
                                                                alignment=TA_CENTER,fontSize=12,
                                                                leading=15,textColor=colors.black,
                                                                borderPadding=0,leftIndent=0,
                                                                rightIndent=0,spaceAfter=0,
                                                                spaceBefore=0,splitLongWords=False,
                                                                spaceShrinkage=0.05,))
  p_text1 = Paragraph("ASIGNACIÓN DE MERCANCIA",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_CENTER,fontSize=12,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=0,
                                                          rightIndent=0,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))
  p_text2 = Paragraph("Fecha de solicitud: "+str(timeDate),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                    fontName='Helvetica',wordWrap='LTR',
                                                                    alignment=TA_RIGHT,fontSize=12,
                                                                    leading=15,textColor=colors.black,
                                                                    borderPadding=0,leftIndent=30,
                                                                    rightIndent=35,spaceAfter=0,
                                                                    spaceBefore=0,splitLongWords=False,
                                                                    spaceShrinkage=0.05,))
  p_text3 = Paragraph("Asignado a: "+str(usuarioA),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=12,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=30,
                                                            rightIndent=35,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  p_text4 = Paragraph("Puesto: "+str(puestoA),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica-Bold',wordWrap='LTR',
                                                    alignment=TA_LEFT,fontSize=12,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=30,
                                                    rightIndent=35,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  ################ T A B L A S ################
  t=Table([[p_text0]], colWidths=180*mm)
  t_style = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT")])
  t.setStyle(t_style)

  data = [[hclave, hversion, hfecha,hpagina], [clave, version, fecha,pagina]]
  t1 = Table(data, colWidths=45*mm)
  t1.setStyle(t_style)

  t1_w = 0.4 * inch
  t2_w = 2 * inch
  t3_w = 1 * inch
  t4_w = 1 * inch
  t5_w = 1.3 * inch
  t6_w = 1.5 * inch
  t7_w = 0.8 * inch

  data1 = [[hnodev, hnoserie, hproyecto, hmarca, hmodelo, hdescripcion, hgarantia]]
  t2 = Table(data1, colWidths=[t1_w, t2_w, t3_w, t4_w, t5_w, t6_w, t7_w],rowHeights=5*mm)
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t2.setStyle(t_style2)

  t3 = Table(data2, colWidths=[t1_w, t2_w, t3_w, t4_w, t5_w, t6_w, t7_w],rowHeights=7*mm,hAlign='CENTER')
  t_style3 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t3.setStyle(t_style3)

  data3 = [[hentrega,hrecibe]]
  t5 = Table(data3, colWidths=90*mm,rowHeights=5*mm)
  t_style1 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t5.setStyle(t_style1)

  data4 = [[b,b]]
  tb = Table(data4, colWidths=90*mm,rowHeights=14*mm,hAlign='CENTER')
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  tb.setStyle(t_style2)

  data5 = [[entrega,recibe]]
  t6 = Table(data5, colWidths=90*mm,rowHeights=13*mm)
  t6.setStyle(t_style)
  ################ B U I L D ##############
  document.append(Spacer(1,90))
  document.append(t)
  ###### ENCABEZADO ARCHIVO ######
  document.append(t1)
  document.append(Spacer(1,10))
  ####  TITULO DE ARCHIVO ####
  document.append(p_text1)
  document.append(Spacer(1,5))
  ####FECHA###
  document.append(p_text2)
  document.append(Spacer(1,10))
  document.append(p_text3)
  document.append(p_text4)
  document.append(Spacer(1,10))
  #### ENCABEZADO DE TABLA ####
  document.append(t2)
  document.append(t3)
  document.append(Spacer(1,30))
  #### FIRMAS ####
  document.append(t5)
  document.append(tb)
  document.append(t6)
  doc.build(document,onFirstPage=_header_footer_portrait,onLaterPages=_header_footer_portrait)
  rootDoc = {'rutaDoc':routePDF+fecha+'-'+usuarioA+'-asig'+extensionDoc}
  rootDoc = json.dumps(rootDoc)
  rutaDocument = routePDF+fecha+'-'+usuarioA+'-asig'+extensionDoc
  # Leer el archivo PDF
  with open(rutaDocument, 'rb') as file:
      pdf_data = file.read()
  ### Codificar el PDF en base64
  pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
  ## Guardar el PDF codificado en Redis
  r.set(fecha+'-'+usuarioA+'-asig', pdf_base64)
  try:
    result = r.publish("downloadFileAsig",rootDoc)
    time.sleep(0.3)
  except Exception as e:
    print(e)

  ##########################    P   D   F   -  R   E   C   E   P   C   I   O   N    #####################################
def makeDevolucion(data):
  import base64
  data2, noserieT, proyectoT, marcaT, modeloT, descripcionT, garantiaT, motivoT  = [], '''''', '''''','''''','''''','''''','''''',''''''
  usuarioD = data['usuarioD']
  puestoD = data['puestoD']
  listaDevolucion = data['lista']
  now = datetime.now()
  timeDate = now.strftime('%d-%m-%Y %H:%M:%S')
  routePDF = '/home/adrian/ws/wave/cassia/apps/pdfs/prs/docs/'
  extensionDoc = '.pdf'
  spaceBR='''<br></br>'''
  ########################## D O C U M E N T O #######################################    
  doc = SimpleDocTemplate(routePDF+timeDate+'-'+usuarioD+'-devol'+extensionDoc,pagesize=letter, rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
  document = []
  ########################## ESTILOS DE PARRAFOS #####################################
  styles1 = getSampleStyleSheet()
  styleN = styles1["BodyText"]
  styleN.alignment = TA_CENTER
  styleN.splitLongWords = True

  b = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/hsm.jpg')  
  b.drawHeight = 0.5*inch
  b.drawWidth = 1.3*inch
  b.alignment = TA_CENTER
  c = Image('/home/adrian/ws/wave/cassia/apps/pdfs/prs/img/firmas/pl.jpg')  
  c.drawHeight = 0.5*inch
  c.drawWidth = 1.3*inch
  c.alignment = TA_CENTER
  empresa = '''Yaa Internet'''
  areaEntrega = '''Encargado de Almacen'''
  nombreEntrega = '''Neza Almacen'''
  areaRecibe = puestoD
  nombreRecibe = usuarioD
  ########################## P A R R A F O S #########################################
  hclave = Paragraph('''Clave''', styleN)
  hversion = Paragraph('''Versión''', styleN)
  hfecha = Paragraph('''Fecha de emisión''', styleN)
  hpagina = Paragraph('''Página''', styleN)
  clave = Paragraph('''FOR-OP-04-01''', styleN)
  version = Paragraph('''1''', styleN)
  fecha = Paragraph('''02-Mayo-2024''', styleN)
  pagina = Paragraph('''1 de 1''', styleN)
  ##################### CAMPOS TABLA ####################
  hnoserie = Paragraph('''<b>N° Serie</b>''', styleN)
  hproyecto = Paragraph('''<b>Proyecto</b>''', styleN)
  hmarca = Paragraph('''<b>Marca</b>''', styleN)
  hmodelo = Paragraph('''<b>Modelo</b>''', styleN)
  hdescripcion = Paragraph('''<b>Descripción</b>''', styleN)
  hgarantia = Paragraph('''<b>Garantia</b>''', styleN)
  hmotivo = Paragraph('''<b>Motivo</b>''', styleN)
  ##################### CONTENIDO TABLA ####################
  for x in range(0,len(listaDevolucion)):
    noserieT = str(listaDevolucion[x][1])
    proyectoT = str(listaDevolucion[x][2])
    marcaT = str(listaDevolucion[x][3])
    modeloT = str(listaDevolucion[x][4])
    descripcionT = str(listaDevolucion[x][5])
    garantiaT = str(listaDevolucion[x][6])
    motivoT = str(listaDevolucion[x][7])
    data2.append([noserieT, proyectoT, marcaT, modeloT, descripcionT, garantiaT, motivoT])
  ##################### CAMPOS FIRMAS ####################
  hrecibe = Paragraph('''<b>Recibe:</b>''', styleN)
  recibe = Paragraph(nombreEntrega+spaceBR+areaEntrega+spaceBR+empresa,styleN)
  hdevuelve = Paragraph('''<b>Devuelve:</b>''', styleN)
  devuelve = Paragraph(nombreRecibe+spaceBR+areaRecibe+spaceBR+empresa,styleN)
  ################# PARRAFOS SEPARADOS ###################
  p_text0 = Paragraph("REQUESICIÓN DE SERVICIOS",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                fontName='Helvetica-Bold',wordWrap='LTR',
                                                                alignment=TA_CENTER,fontSize=12,
                                                                leading=15,textColor=colors.black,
                                                                borderPadding=0,leftIndent=0,
                                                                rightIndent=0,spaceAfter=0,
                                                                spaceBefore=0,splitLongWords=False,
                                                                spaceShrinkage=0.05,))
  p_text1 = Paragraph("DEVOLUCIÓN DE MERCANCIA",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_CENTER,fontSize=12,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=0,
                                                          rightIndent=0,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))
  p_text2 = Paragraph("Fecha de solicitud: "+str(timeDate),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                    fontName='Helvetica',wordWrap='LTR',
                                                                    alignment=TA_RIGHT,fontSize=12,
                                                                    leading=15,textColor=colors.black,
                                                                    borderPadding=0,leftIndent=30,
                                                                    rightIndent=35,spaceAfter=0,
                                                                    spaceBefore=0,splitLongWords=False,
                                                                    spaceShrinkage=0.05,))
  p_text3 = Paragraph("Devuelto por: "+str(usuarioD),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=12,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=30,
                                                            rightIndent=35,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  p_text4 = Paragraph("Puesto: "+str(puestoD),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica-Bold',wordWrap='LTR',
                                                    alignment=TA_LEFT,fontSize=12,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=30,
                                                    rightIndent=35,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  ################ T A B L A S ################
  t=Table([[p_text0]], colWidths=180*mm)
  t_style = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT")])
  t.setStyle(t_style)

  data = [[hclave, hversion, hfecha,hpagina], [clave, version, fecha,pagina]]
  t1 = Table(data, colWidths=45*mm)
  t1.setStyle(t_style)

  t1_w = 2 * inch
  t2_w = 1 * inch
  t3_w = 1 * inch
  t4_w = 1 * inch
  t5_w = 1.3 * inch
  t6_w = 0.8 * inch
  t7_w = 1 * inch

  data1 = [[hnoserie, hproyecto, hmarca, hmodelo, hdescripcion, hgarantia, hmotivo]]
  t2 = Table(data1, colWidths=[t1_w, t2_w, t3_w, t4_w, t5_w, t6_w, t7_w],rowHeights=5*mm)
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t2.setStyle(t_style2)

  t3 = Table(data2, colWidths=[t1_w, t2_w, t3_w, t4_w, t5_w, t6_w, t7_w],rowHeights=7*mm,hAlign='CENTER')
  t_style3 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t3.setStyle(t_style3)

  data3 = [[hrecibe,hdevuelve]]
  t5 = Table(data3, colWidths=90*mm,rowHeights=5*mm)
  t_style1 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t5.setStyle(t_style1)

  data4 = [[b,c]]
  tb = Table(data4, colWidths=90*mm,rowHeights=14*mm,hAlign='CENTER')
  t_style2 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"),("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  tb.setStyle(t_style2)

  data5 = [[recibe,devuelve]]
  t6 = Table(data5, colWidths=90*mm,rowHeights=13*mm)
  t6.setStyle(t_style)
  ################ B U I L D ##############
  document.append(Spacer(1,90))
  document.append(t)
  ###### ENCABEZADO ARCHIVO ######
  document.append(t1)
  document.append(Spacer(1,10))
  ####  TITULO DE ARCHIVO ####
  document.append(p_text1)
  document.append(Spacer(1,5))
  ####FECHA###
  document.append(p_text2)
  document.append(Spacer(1,10))
  document.append(p_text3)
  document.append(p_text4)
  document.append(Spacer(1,10))
  #### ENCABEZADO DE TABLA ####
  document.append(t2)
  document.append(t3)
  document.append(Spacer(1,30))
  #### FIRMAS ####
  document.append(t5)
  document.append(tb)
  document.append(t6)

  doc.build(document,onFirstPage=_header_footer_portrait,onLaterPages=_header_footer_portrait)
  rootDoc = {'rutaDoc':routePDF+fecha+'-'+usuarioD+'-devol'+extensionDoc}
  rootDoc = json.dumps(rootDoc)
  rutaDocument = routePDF+fecha+'-'+usuarioD+'-devol'+extensionDoc
  # Leer el archivo PDF
  with open(rutaDocument, 'rb') as file:
      pdf_data = file.read()
  ### Codificar el PDF en base64
  pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
  ## Guardar el PDF codificado en Redis
  r.set(fecha+'-'+usuarioD+'-devol', pdf_base64)
  try:
    result = r.publish("downloadFileDevol",rootDoc)
    time.sleep(0.3)
  except Exception as e:
    print(e)
  ######################  M  A   I   N  ######################
if __name__ == "__main__":
    try:
        r = StrictRedis(host='10.0.3.84',port=6379,db=0,health_check_interval=30,socket_keepalive=True)
    except Exception as e:
        print(e)
    try:
        redisclientrts = Client(host='10.0.3.84',port=6379,socket_keepalive=True,retry_on_timeout=True)
    except Exception as e:
        print(e)

    client1 = Listener1(r,redisclientrts, ['yi_pdfs_prs', 'yi_pdfs_recepcion', 'yi_pdfs_asignacion', 'yi_pdfs_devolucion'])
    client1.start()