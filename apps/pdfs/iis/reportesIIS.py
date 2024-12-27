from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape, legal
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
from num2words import num2words

####################################################    F  U   N   C   I   O   N   E   S    #########################################################################
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
          makeResponsivaComprado(data)
        except:
            pass

    def work2(self, item):
        data =0
        try:
          data = json.loads(item.decode('utf8'))
          makeResponsivaComodato(data)
        except:
            pass

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message["channel"].decode("utf-8")=="yi_pdfs_iis_comprado":
                        self.work(message['data'])
                    if message["channel"].decode("utf-8")=="yi_pdfs_iis_comodato":
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
                        self.pubsub.subscribe(['yi_pdfs_iis_comprado', 'yi_pdfs_iis_comodato'])
                        break
            time.sleep(0.001)  # be nice to the system :)

def _header_footer_portrait(canvas,doc):
  #guardamos el estado de nuestro canvas , para poder dibujar en el 
  canvas.saveState()
  styles = getSampleStyleSheet()
  #header
  header = Image('header-footer/yaainternet.png')
  header.drawHeight = 30
  header.drawWidth = 30
  header.hAlign = 'LEFT'
  w , h = header.wrapOn(doc,doc.width , doc.topMargin)
  header.drawOn(canvas , 30, 950)
  #header
  header2 = Image('header-footer/yaainternet2.png')
  header2.drawHeight = 15
  header2.drawWidth = 70
  header2.hAlign = 'LEFT'
  w , h = header2.wrapOn(doc,doc.width , doc.topMargin)
  header2.drawOn(canvas , 70, 955)
  # Footer 1
  footer3 = Image('header-footer/left-footer.png')
  footer3.drawHeight = 5
  footer3.drawWidth = 150
  footer3.hAlign = 'LEFT'
  w , h = footer3.wrapOn(doc,doc.width , doc.bottomMargin)
  footer3.drawOn(canvas , 30, 25)
  # Footer 2
  footer4 = Image('header-footer/direccion1.png')
  footer4.drawHeight = 10
  footer4.drawWidth = 200
  footer4.hAlign = 'LEFT'
  w , h = footer4.wrapOn(doc,doc.width , doc.bottomMargin)
  footer4.drawOn(canvas , 220, 22)
  # Footer 3
  footer5 = Image('header-footer/right-footer.png')
  footer5.drawHeight = 5
  footer5.drawWidth = 130
  footer5.hAlign = 'RIGHT'
  w , h = footer5.wrapOn(doc,doc.width , doc.bottomMargin)
  footer5.drawOn(canvas, 460, 25)
  # Release the canvas
  canvas.restoreState()

#####################################    P   D   F   -  C  O   M   P   R   A   D   O    #####################################
def makeResponsivaComprado(data):
  import base64
  data2, noDevT, noserieT, proyectoT, marcaT, modeloT, descripcionT, garantiaT  = [], '''''', '''''','''''','''''','''''','''''',''''''
  usuarioA = data['usuarioA']
  puestoA = data['puestoA']
  listaAsignacion = data['lista']
  if data['ticketcompleto']['formatoPago'] == 'True':
    factura_cliente = "SI"
  else:
    factura_cliente = "NO"
  #listaAsignacion = data['lista'].replace("'","[")
  #listaAsignacion = json.loads(listaCompra)
  now = datetime.now()
  timeDate = now.strftime('%d-%m-%Y %H:%M:%S')
  timeDate1 = now.strftime('%Y-%m-%d')
  fecha = datetime.strptime(timeDate1, '%Y-%m-%d')
  # Obtener el día de la semana (0 = Lunes, 6 = Domingo)
  dia_semana = fecha.weekday()
  # Convertir el número del mes a nombre del mes
  numero_mes = fecha.month
  # Convertir el número del día a nombre del día
  dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  nombre_dia = dias_semana[dia_semana]
  nombre_mes = meses[numero_mes - 1]
  timeDate2 = now.strftime('%d de '+str(nombre_mes)+' del %Y')
  numero_en_palabras = num2words(float(1325.00), lang='es')
  routePDF = '/home/adrian/ws/wave/cassia/apps/pdfs/iis/docs/'
  extensionDoc = '.pdf'
  spaceBR='''<br></br>'''
  ########################## D O C U M E N T O #######################################    
  doc = SimpleDocTemplate(routePDF+'timeDate'+'-'+usuarioA+'-asig'+extensionDoc,pagesize=legal, rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
  document = []
  ########################## ESTILOS DE PARRAFOS #####################################
  styles1 = getSampleStyleSheet()
  styleN = styles1["BodyText"]
  styleN.alignment = TA_CENTER
  styleN.splitLongWords = True
  styleN.fontSize = 8

  styleBH = styles1["Normal"]
  styleBH.alignment = TA_CENTER
  # Definir un estilo de párrafo para las celdas de la tabla
  cell_style = ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=8)
  medium_cell_style = ParagraphStyle(name='SmallCellStyle', alignment=TA_CENTER, fontSize=9)
  small_cell_style = ParagraphStyle(name='SmallCellStyle', alignment=TA_CENTER, fontSize=7.5)
  b = Image('/home/adrian/ws/wave/cassia/apps/pdfs/iis/img/firmas/pl.jpg')  
  b.drawHeight = 0.5*inch
  b.drawWidth = 1.3*inch
  b.alignment = TA_CENTER
  c = Image('/home/adrian/ws/wave/cassia/apps/pdfs/iis/img/firmas/blank.png')  
  c.drawHeight = 0.5*inch
  c.drawWidth = 1.3*inch
  c.alignment = TA_CENTER
  nombre_empresa = "DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A. DE C.V"
  nombre_cliente = data['ticketcompleto']['name_client']
  nombre_tecnico = data['ticketcompleto']['instalador'].split("/")
  nombre_tecnico = nombre_tecnico[0]
  cliente_firmas = '''SUSCRIPTOR (CLIENTE)'''
  empresa_firmas = '''REPRESENTANTE LEGAL DEL OPERADOR'''
  tecnico_firmas = '''TÉCNICO INSTALADOR'''
  empresafiscal = Paragraph('''<b>DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A. DE C.V.</b>''', styleN)
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
  hequipos = Paragraph('''<b>EQUIPOS ENTREGADOS AL CLIENTE</b>''', styleN)
  hnoserie = Paragraph('''<b>N° Serie</b>''', styleN)
  hmarca = Paragraph('''<b>Marca</b>''', styleN)
  hmodelo = Paragraph('''<b>Modelo</b>''', styleN)
  hdescripcion = Paragraph('''<b>Descripción</b>''', styleN)
  ##################### CAMPOS FIRMAS ####################
  clientetable = Paragraph(nombre_cliente+spaceBR+cliente_firmas,styleN)
  empresatable = Paragraph(empresa_firmas,styleN)
  tecnicotable = Paragraph(nombre_tecnico+spaceBR+tecnico_firmas,styleN)
  parrafo1 = "CONTRATO DE PRESTACIÓN DE SERVICIOS QUE CELEBRAN POR UNA PARTE DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A. DE C.V. (EN LO SUCESIVO “OPERADOR”) Y POR LA OTRA PARTE, LA PERSONA FISICA O MORAL CUYO NOMBRE Y DIRECCION QUEDAN ASENTADOS EN LA TABLA DE DATOS GENERALES DEL CLIENTE DE ESTE DOCUMENTO (EN LO SUCESIVO “SUSCRIPTOR”), AL TENOR DE LAS SIGUIENTES DECLARACIONES Y CLÁUSULAS:"
  p_text1 = Paragraph(parrafo1,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_JUSTIFY,fontSize=7,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=10,
                                                          rightIndent=10,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))
  p_text3 = Paragraph("DECLARACIONES DEL OPERADOR: ",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo3 = "A) Declara 'EL OPERADOR' ser una sociedad mercantil legalmente constituida meidante la escritura pública N° 1520 mil quinientos veinte, celebrada el 21 de Marzo de 2023, pasada ante la fe del Lic. Carlos Eduardo"
  parrafo4 = " Barrera Cedillo, notario Corredor Público N° 3 de la plaza del Estado de Colima, la cual ha sido debidamente inscrita ante el Registro Público del Comercio."
  p_text4 = Paragraph(parrafo3+parrafo4,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo5 = "B) Tener el título de concesión otorgada por el Instituto Federal de Telecomunicaciones."
  p_text5 = Paragraph(parrafo5,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  p_text6 = Paragraph("DECLARACIONES DEL CLIENTE: ",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo6 = "A) Declara 'EL CLIENTE' que los datos que se asientan en el presente instrumento contractual son ciertos."
  p_text7 = Paragraph(parrafo6,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo7 = "B) En caso de que así sea y lo marque el contrato, que es su voluntad celebrar el presente contrato de servicios con la persona moral denominada DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A DE C.V."
  p_text8 = Paragraph(parrafo7,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  p_text9 = Paragraph("Fecha de solicitud: "+str(timeDate),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                    fontName='Helvetica',wordWrap='LTR',
                                                                    alignment=TA_RIGHT,fontSize=10,
                                                                    leading=15,textColor=colors.black,
                                                                    borderPadding=0,leftIndent=30,
                                                                    rightIndent=10,spaceAfter=0,
                                                                    spaceBefore=0,splitLongWords=False,
                                                                    spaceShrinkage=0.05,))
  p_text10 = Paragraph("CLAUSULAS:",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo8 = "I) El SUSCRIPTOR deberá abstenerse de acceder, alterar o destruir cualquier información que no sea de su propiedad y, en general, de efectuar o permitir cualquier acto en contra de los intereses del OPERADOR y/o de cualquiera de sus clientes, que directa o indirectamente puedan repercutir en las actividades o imagen de negocios del OPERADOR o de cualesquiera de sus clientes."
  p_text11 = Paragraph(parrafo8,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo9 = "II) La vigencia del presente contrato será por tiempo indeterminado y entrará en vigor a partir de la fecha en que el SUSCRIPTOR contrate el servicio."
  p_text12 = Paragraph(parrafo9,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo10 = "III) En caso de falla del equipo terminal, EL OPERADOR procederá a reemplazar el mismo, siempre y cuando el SUSCRIPTOR entregue el equipo terminal al personal del servicio técnico que se presente en el domicilio del SUSCRIPTOR para atender la falla del servicio. El SUSCRIPTOR deberá devolver, cuando menos, el módem y el adaptador de corriente, en el estado en que los recibió, salvo por el deterioro causado por el uso normal de los mismos, acordando las partes que, si el SUSCRIPTOR no devuelve el equipo terminal en la forma señalada, o por que el equipo terminal haya sufrido una descarga eléctrica y eso haya ocasionado defectos en el servicio, quedará obligado a pagar al OPERADOR un nuevo equipo terminal. Al momento de su entrega, se proporcionará al SUSCRIPTOR una nota de recepción del EQUIPO TERMINAL la cual deberá contener el nombre del SUSCRIPTOR, número de serie del equipo terminal, nombre de la persona que lo entrega y lo recibe. En caso de falla imputable al SUSCRIPTOR, robo o extravío del equipo terminal, el SUSCRIPTOR reportará dicha eventualidad al OPERADOR, con el objeto de que se le proporcione otro equipo terminal, quedando obligado el SUSCRIPTOR a pagar, el cargo por reemplazo de equipo terminal de conformidad con la tarifa vigente."
  p_text13 = Paragraph(parrafo10,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo11 = "IV) El servicio contará con soporte técnico de las 8:00 am a 6:00 pm del día los 365 (trescientos sesenta y cinco) días del año, para lo cual el SUSCRIPTOR deberá comunicarse al Centro de Atención y Soporte Técnico a Clientes, o bien, a cualquier otro centro de atención que se le indique, en caso de que: El SUSCRIPTOR requiera información para la configuración del equipo terminal; o se presente una falla en el servicio y/o equipo terminal. EL SUSCRIPTOR reconoce y acepta que en caso de que el servicio no pueda ser prestado por fallas o daños imputables al SUSCRIPTOR en los accesorios, este último deberá reemplazar dichos accesorios por su cuenta. Para los efectos de supervisión, mantenimiento o reparación de las instalaciones del OPERADOR hasta el dispositivo de interconexión terminal, el SUSCRIPTOR conviene en permitir a los trabajadores del OPERADOR, el libre acceso al lugar donde están colocadas dichas instalaciones, previa identificación vigente del personal respectivo."
  p_text14 = Paragraph(parrafo11,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo12 = "V) El SUSCRIPTOR podrá solicitar la cancelación del servicio, en cuyo caso deberá comunicarse personalmente al Centro de Atención y Soporte Técnico a Clientes del OPERADOR. La cancelación del servicio dará lugar a la terminación del presente contrato."
  p_text15 = Paragraph(parrafo12,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo13 = "VI) EL OPERADOR tiene el derecho de proceder a recindir este contrato en dado caso que el cliente no haya pagado el servicio durante 8 meses y que en este tiempo no haya solicitado una reconexión de su servicio."
  p_text16 = Paragraph(parrafo13,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  p_text17 = Paragraph("CONDICIONES PARA EL USO DEL SERVICIO Y ACLARACIONES:",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo14 = "I) Este Contrato no autoriza y por lo tanto no está permitido: (i) la comercialización, venta o reventa del SERVICIO; (ii) la comercialización, venta o reventa de aplicaciones sobre la base del SERVICIO para prestar servicios de telecomunicaciones o para realizar actividades tales como transportar o reoriginar tráfico público conmutado originado en otra cuidad o país, así como realizar actividades de regreso de llamadas y puenteo de llamadas; y (iii) la conexión del SERVICIO por parte del SUSCRIPTOR con terceros que se ubiquen fuera del domicilio del SUSCRIPTOR a través de cualquier tecnología que le permita al tercero hacer uso del SERVICIO, en el entendido que el SUSCRIPTOR será responsable de tomar las medidas que sean necesarias para evitar el acceso al SERVICIO a cualquier tercero que no se encuentre dentro del domicilio del SUSCRIPTOR."
  p_text18 = Paragraph(parrafo14,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo15 = "II) EL OPERADOR autorizará el reemplazo del equipo mediante garantía por defectos de fabrica del equipo terminal en un plazo máximo de 12 meses de conformidad con lo establecido en el numeral tercero del apartado de CLAUSULAS del presente contrato."
  p_text19 = Paragraph(parrafo15,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  ################ T A B L A S ################
  t=Table([["Fecha:", str(timeDate)], ["N° Contrato:", str("1501")], ["N° Cliente:", data['ticketcompleto']['id_client']]],rowHeights=4*mm, colWidths=40*mm, hAlign='RIGHT')
  t_style = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
  t.setStyle(t_style)

  t0_w1 = 7.8 * inch
  data0 = [[Paragraph("DATOS GENERALES DEL CLIENTE", medium_cell_style)]]
  t0 = Table(data0, colWidths=[t0_w1],rowHeights=4*mm)
  t_style0 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t0.setStyle(t_style0)

  t1_w1, t1_w2 = 6.3 * inch, 1.5 * inch
  data1 = [[Paragraph("NOMBRE DEL TITULAR O RAZÓN SOCIAL: "+data['ticketcompleto']['name_client'], small_cell_style),Paragraph("GIRO: "+"RESIDENCIAL", small_cell_style)]]
  t1 = Table(data1, colWidths=[t1_w1,t1_w2],rowHeights=4*mm)
  t1.setStyle(t_style)

  t2_w1, t2_w2, t2_w3, t2_w4 = 2 * inch, 2 * inch, 2 * inch, 1.8 * inch
  data2 = [[Paragraph("SERVICIO: "+"INSTALACIÓN NUEVA", small_cell_style), Paragraph("CONTACTO: "+data['ticketcompleto']['phone_client'], small_cell_style), Paragraph("E-MAIL: "+data['ticketcompleto']['email_client'], small_cell_style),Paragraph("EQUIPO: "+data['ticketcompleto']['paqueteplan'], small_cell_style)]]
  t2 = Table(data2, colWidths=[t2_w1, t2_w2, t2_w3, t2_w4],rowHeights=4*mm)
  t2.setStyle(t_style)

  t3_w1, t3_w2, t3_w3 = 3.2 * inch, 2.6 * inch, 2 * inch
  data3 = [[Paragraph("CALLE Y NÚMERO: "+data['ticketcompleto']['address_client'], small_cell_style), Paragraph("COLONIA: "+data['ticketcompleto']['colonia_client'], small_cell_style), Paragraph("LOCALIDAD: "+data['ticketcompleto']['localidad_client'], small_cell_style)]]
  t3 = Table(data3, colWidths=[t3_w1, t3_w2, t3_w3],rowHeights=4*mm)
  t3.setStyle(t_style)

  t4_w1, t4_w2, t4_w3, t4_w4 = 1.9 * inch, 1.9 * inch, 3 * inch, 1 * inch
  data4 = [[Paragraph("MUNICIPIO: "+data['ticketcompleto']['municipio_client'], small_cell_style), Paragraph("ESTADO: "+data['ticketcompleto']['municipio_client'], small_cell_style), Paragraph("FORMA DE PAGO: "+data['ticketcompleto']['formatoPago'], small_cell_style), Paragraph("FACTURA: "+factura_cliente, small_cell_style)]]
  t4 = Table(data4, colWidths=[t4_w1, t4_w2, t4_w3, t4_w4],rowHeights=4*mm)
  t4.setStyle(t_style)

  t5_w1, t5_w2, t5_w3 = 2.4 * inch, 3 * inch, 2.4 * inch
  data5 = [[Paragraph("PAQUETE: "+data['ticketcompleto']['anchoBanda'], small_cell_style),Paragraph("TOTAL INSTALACIÓN+EQUIPOS: "+'$'+str(float(data['ticketcompleto']['precio_client'])), small_cell_style), Paragraph("COSTO MENSUAL: "+"$"+str(float(data['ticketcompleto']['precioMensual'])), small_cell_style)]]
  t5 = Table(data5, colWidths=[t5_w1, t5_w2, t5_w3],rowHeights=4*mm)
  t5.setStyle(t_style)

  t6_w1 = 7.8 * inch
  data6 = [[hequipos]]
  t6 = Table(data6, colWidths=[t6_w1],rowHeights=4*mm,hAlign='CENTER')
  t_style6 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE") ,("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t6.setStyle(t_style6)

  t7_w1, t7_w2, t7_w3, t7_w4 = 1.4 * inch, 1.2 * inch, 1.2 * inch, 4 * inch
  data7 = [[hnoserie, hmarca, hmodelo, hdescripcion]]
  t7 = Table(data7, colWidths=[t7_w1, t7_w2, t7_w3, t7_w4],rowHeights=4.5*mm,hAlign='CENTER')
  t_style7 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE") ,("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t7.setStyle(t_style7)

  t8_w1, t8_w2, t8_w3, t8_w4 = 1.4 * inch, 1.2 * inch, 1.2 * inch, 4 * inch
  data8 = [[Paragraph(str(listaAsignacion[x][1]), ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=8, wordWrap='CJK', splitLongWords=True)),
            Paragraph(str(listaAsignacion[x][3]), ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=8, wordWrap='CJK', splitLongWords=True)),
            Paragraph(str(listaAsignacion[x][4]), ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=8, wordWrap='CJK', splitLongWords=True)),
            Paragraph(str(listaAsignacion[x][5]), ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=8, wordWrap='CJK', splitLongWords=True))] for x in range(len(listaAsignacion))]
  t8 = Table(data8, colWidths=[t8_w1, t8_w2, t8_w3, t8_w4], hAlign='CENTER')
  t_style8 = TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                         ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                         ("BACKGROUND", (0, 0), (-1, -1), '#ffffff')])
  t8.setStyle(t_style8)

  data9 = [[c,b,c]]
  t9 = Table(data9, colWidths=50*mm,rowHeights=15*mm,hAlign='CENTER')
  t_style9 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t9.setStyle(t_style9)

  data10 = [[clientetable,empresatable,tecnicotable]]
  t10 = Table(data10, colWidths=50*mm,rowHeights=8*mm)
  t10.setStyle(t_style)
  ################ B U I L D ##############
  document.append(Spacer(1,10))
  document.append(t)
  ####  TITULO DE ARCHIVO ####
  document.append(Spacer(1,10))
  document.append(p_text1)
  ###### ENCABEZADO ARCHIVO ######
  document.append(Spacer(1,5))
  document.append(t0)
  document.append(t1)
  document.append(t2)
  document.append(t3)
  document.append(t4)
  document.append(t5)
  document.append(Spacer(1,5))
  document.append(p_text3)
  document.append(p_text4)
  document.append(p_text5)
  document.append(p_text6)
  document.append(p_text7)
  document.append(p_text8)
  document.append(Spacer(1,5))
  #### CLAUSULAS ####
  document.append(p_text10)
  document.append(p_text11)
  document.append(p_text12)
  document.append(p_text13)
  document.append(p_text14)
  document.append(p_text15)
  document.append(p_text16)
  document.append(p_text17)
  document.append(p_text18)
  document.append(p_text19)
  document.append(Spacer(1,8))
  #### ENCABEZADO DE TABLA ####
  document.append(t6)
  document.append(t7)
  document.append(t8)
  document.append(Spacer(1,8))
  #### FIRMAS ####
  document.append(t9)
  document.append(t10)
  doc.build(document,onFirstPage=_header_footer_portrait,onLaterPages=_header_footer_portrait)
#  rootDoc = {'rutaDoc':routePDF+timeDate+'-'+usuarioA+'-asig'+extensionDoc}
#  rootDoc = json.dumps(rootDoc)
#  rutaDocument = routePDF+timeDate+'-'+usuarioA+'-asig'+extensionDoc
  # Leer el archivo PDF
#  with open(rutaDocument, 'rb') as file:
#      pdf_data = file.read()
#  ### Codificar el PDF en base64
#  pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
#  ## Guardar el PDF codificado en Redis
#  #r.set(fecha+'-'+usuarioA+'-asig', pdf_base64)
#  try:
#    result = r.publish("downloadFileAsig",rootDoc)
#    time.sleep(0.3)
#  except Exception as e:
#    print(e)
#
  ##########################    P   D   F   -  R   E   C   E   P   C   I   O   N    #####################################
def makeResponsivaComodato():
  import base64
  data2, noDevT, noserieT, proyectoT, marcaT, modeloT, descripcionT, garantiaT  = [], '''''', '''''','''''','''''','''''','''''',''''''
  usuarioA = "Jesus Adrian Rojas Hernandez"#data['usuarioA']
  puestoA = 'Desarrollador'#data['puestoA']
  listaAsignacion = [['9C05D6880EC2', 'UBIQUITI', 'LITEBEAM 5AC', 'Antena Direccional LiteBeam M5, 23dBi, 5.1 - 5.8GHz GEN 2'], 
                     ['9C05D6880EC2', 'UBIQUITI', 'LITEBEAM 5AC', 'Antena Direccional LiteBeam M5, 23dBi, 5.1 - 5.8GHz GEN 2'], 
                     ['9C05D6880EC2', 'UBIQUITI', 'LITEBEAM 5AC', 'Antena Direccional LiteBeam M5, 23dBi, 5.1 - 5.8GHz GEN 2'], 
                     ['9C05D6880EC2', 'UBIQUITI', 'LITEBEAM 5AC', 'Antena Direccional LiteBeam M5, 23dBi, 5.1 - 5.8GHz GEN 2'], 
                     ['9C05D6880EC2', 'UBIQUITI', 'LITEBEAM 5AC', 'Antena Direccional LiteBeam M5, 23dBi, 5.1 - 5.8GHz GEN 2']
                    ]#data['lista']
  #listaAsignacion = data['lista'].replace("'","[")
  #listaAsignacion = json.loads(listaCompra)
  now = datetime.now()
  timeDate = now.strftime('%d-%m-%Y %H:%M:%S')
  timeDate1 = now.strftime('%Y-%m-%d')
  fecha = datetime.strptime(timeDate1, '%Y-%m-%d')
  # Obtener el día de la semana (0 = Lunes, 6 = Domingo)
  dia_semana = fecha.weekday()
  # Convertir el número del mes a nombre del mes
  numero_mes = fecha.month
  # Convertir el número del día a nombre del día
  dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  nombre_dia = dias_semana[dia_semana]
  nombre_mes = meses[numero_mes - 1]
  timeDate2 = now.strftime('%d de '+str(nombre_mes)+' del %Y')
  numero_en_palabras = num2words(float(1325.00), lang='es')
  routePDF = '/home/adrian/ws/wave/cassia/apps/pdfs/iis/docs/'
  extensionDoc = '.pdf'
  spaceBR='''<br></br>'''
  ########################## D O C U M E N T O #######################################    
  doc = SimpleDocTemplate(routePDF+'timeDate'+'-'+usuarioA+'-asig'+extensionDoc,pagesize=legal, rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)
  document = []
  ########################## ESTILOS DE PARRAFOS #####################################
  styles1 = getSampleStyleSheet()
  styleN = styles1["BodyText"]
  styleN.alignment = TA_CENTER
  styleN.splitLongWords = True
  styleN.fontSize = 8

  styleBH = styles1["Normal"]
  styleBH.alignment = TA_CENTER
  # Definir un estilo de párrafo para las celdas de la tabla
  cell_style = ParagraphStyle(name='CellStyle', alignment=TA_CENTER, fontSize=8)
  medium_cell_style = ParagraphStyle(name='SmallCellStyle', alignment=TA_CENTER, fontSize=9)
  small_cell_style = ParagraphStyle(name='SmallCellStyle', alignment=TA_CENTER, fontSize=7.5)
  b = Image('/home/adrian/ws/wave/cassia/apps/pdfs/iis/img/firmas/pl.jpg')  
  b.drawHeight = 0.5*inch
  b.drawWidth = 1.3*inch
  b.alignment = TA_CENTER
  c = Image('/home/adrian/ws/wave/cassia/apps/pdfs/iis/img/firmas/blank.png')  
  c.drawHeight = 0.5*inch
  c.drawWidth = 1.3*inch
  c.alignment = TA_CENTER
  nombre_empresa = "DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A. DE C.V"
  nombre_cliente = '''Paola Caraballo Fernández'''
  nombre_tecnico = '''Robert Espinoza Creuhuet'''
  cliente_firmas = '''SUSCRIPTOR (CLIENTE)'''
  empresa_firmas = '''REPRESENTANTE LEGAL'''
  tecnico_firmas = '''TÉCNICO INSTALADOR'''
  empresafiscal = Paragraph('''<b>DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A. DE C.V.</b>''', styleN)
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
  hequipos = Paragraph('''<b>EQUIPOS ENTREGADOS AL CLIENTE</b>''', styleN)
  hnoserie = Paragraph('''<b>N° Serie</b>''', styleN)
  hmarca = Paragraph('''<b>Marca</b>''', styleN)
  hmodelo = Paragraph('''<b>Modelo</b>''', styleN)
  hdescripcion = Paragraph('''<b>Descripción</b>''', styleN)
  ##################### CAMPOS FIRMAS ####################
  clientetable = Paragraph(nombre_cliente+spaceBR+cliente_firmas,styleN)
  empresatable = Paragraph(empresa_firmas,styleN)
  tecnicotable = Paragraph(nombre_tecnico+spaceBR+tecnico_firmas,styleN)
  parrafo1 = "CONTRATO DE COMODATO QUE CELEBRA POR UNA PARTE LA PERSONA MORAL DENOMINADA DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A DE C.V POR CONDUCTO DE SU ADMINISTRADOR UNICO A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ "
  parrafo2 = "LA OPERADORA Y POR OTRA PARTE EL CLIENTE AL TENOR DE LAS DECLARACIONES Y CLAUSULAS QUE EN EL PRESENTE CONTRATO SE ESTABLECEN."
  p_text1 = Paragraph(parrafo1+parrafo2,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                          fontName='Helvetica-Bold',wordWrap='LTR',
                                                          alignment=TA_JUSTIFY,fontSize=7,
                                                          leading=15,textColor=colors.black,
                                                          borderPadding=0,leftIndent=10,
                                                          rightIndent=10,spaceAfter=0,
                                                          spaceBefore=0,splitLongWords=False,
                                                          spaceShrinkage=0.05,))
  p_text3 = Paragraph("DECLARACIONES DEL OPERADOR: ",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo3 = "A) Declara 'EL OPERADOR' ser una sociedad mercantil legalmente constituida meidante la escritura pública N° 1520 mil quinientos veinte, celebrada el 21 de Marzo de 2023, pasada ante la fe del Lic. Carlos Eduardo"
  parrafo4 = " Barrera Cedillo, notario Corredor Público N° 3 de la plaza del Estado de Colima, la cual ha sido debidamente inscrita ante el Registro Público del Comercio."
  p_text4 = Paragraph(parrafo3+parrafo4,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo5 = "B) Tener el título de concesión otorgada por el Instituto Federal de Telecomunicaciones."
  p_text5 = Paragraph(parrafo5,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  p_text6 = Paragraph("DECLARACIONES DEL CLIENTE: ",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo6 = "A) Declara 'EL CLIENTE' que los datos que se asientan en el presente instrumento contractual son ciertos."
  p_text7 = Paragraph(parrafo6,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo7 = "B) En caso de que así sea y lo marque el contrato, que es su voluntad celebrar el presente contrato de COMODATO con la persona moral denominada DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A DE C.V."
  p_text8 = Paragraph(parrafo7,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  p_text9 = Paragraph("Fecha de solicitud: "+str(timeDate),ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                                    fontName='Helvetica',wordWrap='LTR',
                                                                    alignment=TA_RIGHT,fontSize=10,
                                                                    leading=15,textColor=colors.black,
                                                                    borderPadding=0,leftIndent=30,
                                                                    rightIndent=10,spaceAfter=0,
                                                                    spaceBefore=0,splitLongWords=False,
                                                                    spaceShrinkage=0.05,))
  p_text10 = Paragraph("CLAUSULAS:",ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                            fontName='Helvetica-Bold',wordWrap='LTR',
                                                            alignment=TA_LEFT,fontSize=7,
                                                            leading=15,textColor=colors.black,
                                                            borderPadding=0,leftIndent=10,
                                                            rightIndent=10,spaceAfter=0,
                                                            spaceBefore=0,splitLongWords=False,
                                                            spaceShrinkage=0.05,))
  parrafo8 = "I) EL OPERADOR ENTREGA EN COMODATO los equipos AL CLIENTE, para el uso exclusivo de los servicios de suministro de INTERNET que le brindara EL OPERADOR."
  p_text11 = Paragraph(parrafo8,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo9 = "II) EL CLIENTE recibe de conformidad para su uso, guarda y custodia los equipos señalados en el apartado de DESCRIPCIÓN DE EQUIPOS ENTREGADOS del presente instrumento contractual."
  p_text12 = Paragraph(parrafo9,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo10 = "III) EL CLIENTE, se obliga a conservar los equipos entregados en COMODATO y es responsable de manera enunciativa más no limitativa de todo daño, perdida, robo o extravío que puedan los equipos que se encuentren bajo su resguardo."
  p_text13 = Paragraph(parrafo10,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo11 = "IV) EL CLIENTE, no puede SIN CONSENTIMIENTO del OPERADOR cambiar de domicilio los equipos entregados en COMODATO."
  p_text14 = Paragraph(parrafo11,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo12 = "V) El presente contrato es de vigencia indefinida que dará inicio a la firma del presente contrato, entrega del equipo y el mismo se dará por terminado una vez que el CLIENTE haga entrega de los equipos que le fueron entregados, en óptimas condiciones para su buen funcionamiento."
  p_text15 = Paragraph(parrafo12,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo13 = "VI) En caso de que el CLIENTE no entregue el equipo, o lo entregue incompleto, tendrá la obligación de pagarlos al valor actual del mercado."
  p_text16 = Paragraph(parrafo13,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo14 = "VII) En caso de que los equipos presenten fallas y las mismas no sean atribuibles al CLIENTE, deberá dar aviso al OPERADOR para que realice de manera gratuita el reemplazo de los equipos."
  p_text17 = Paragraph(parrafo14,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo15 = "VIII) En caso de que los equipos sean desconfigurados por cuestiones atribuibles al CLIENTE, ya sea por desarmarlos, alterar o dañar los mismos, y se requiera la asistencia técnica, EL CLIENTE tendrá que pagar la visita del técnico la cual tendrá un costo de $350.00m.n (trescientos cincuenta pesos moneda nacional) y la reposición del equipo si en ese caso es necesario."
  p_text18 = Paragraph(parrafo15,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo16 = "IX) En caso de que el CLIENTE sufra el robo de los equipos que tiene bajo su resguardo, deberá presentar la denuncia penal ante la autoridad que corresponda, y dar aviso al OPERADOR."
  p_text19 = Paragraph(parrafo16,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo17 = "X) En caso de cualquier controversia relacionada al presente instrumento contractual será resuelta por los juzgados competentes de la ciudad de Colima, Colima."
  p_text20 = Paragraph(parrafo17,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo18 = "XI) A la firma del presente contrato las partes aceptan el contenido del mismo y se sujetan a sus CLAUSULAS."
  p_text21 = Paragraph(parrafo18,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo19 = "XII) EL OPERADOR entrega en COMODATO los equipos mencionados en el presente contrato única y exclusivamente para el uso y suministro de internet propocionado por la operadora en los siguientes términos: el cliente pagará todas las mensualidades"
  parrafo20 = " SIN EXCEPCIÓN hasta que el cliente solicite la cancelación del servicio y facilite la entrega de los equipos. Las fechas de corte y medios de pago de las mensualidades son: las fechas del pago serán el día 1ro de cada mes,"
  parrafo21 = " teniendo como fecha límite de pago el día 5 de cada mes. Después del día 5 se cobrará un recargo por mora o reconexión de $50.00 m.n. Cuando el servicio sea instalado un día diferente al 1ro del mes el cliente pagará la fracción proporcional que le resta al mes."
  p_text22 = Paragraph(parrafo19+parrafo20+parrafo21,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo22 = "XIII) EL OPERADOR tiene el derecho de proceder a recindir este contrato en dado caso que el cliente no haya pagado el servicio durante 3 meses y que en este tiempo no haya solicitado una reconexión de su servicio, "
  parrafo23 = "EL CLIENTE se obliga a regresar los equipos que se le hayan instalado y se muestren en la tabla coincidiendo tanto con la marca como con el número de serie del equipo. En caso contrario EL CLIENTE se olbiga a pagar la cantidad que el pagaré indique."
  p_text23 = Paragraph(parrafo22+parrafo23,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo24 = "PAGARÉ 1/1 "+str(nombre_dia)+" "+str(timeDate2)
  p_text24 = Paragraph(parrafo24,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                    spaceShrinkage=0.05,))
  parrafo25 = "Debo y pagaré de manera incondicional por medio del presente a la orden DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A. DE C.V. en la ciudad de Colima, Col. el día "+str(nombre_dia)+" "+str(timeDate2)
  parrafo26 = " la cantidad de $1320.00 ("+str(numero_en_palabras)+" pesos m.n.), valor recibido en bienes a mi entera satisfacción, este pagaré está sujeto a la condición de que, al no pagarse a su vencimiento, causará intereses moratorios de 2.5% mensual, pagadero en esta ciudad juntamente con el principal."
  p_text25 = Paragraph(parrafo25+parrafo26,ParagraphStyle(name='Normal_CENTER',parent=styles1['Normal'],
                                                    fontName='Helvetica',wordWrap='LTR',
                                                    alignment=TA_JUSTIFY,fontSize=7,
                                                    leading=15,textColor=colors.black,
                                                    borderPadding=0,leftIndent=10,
                                                    rightIndent=10,spaceAfter=0,
                                                    spaceBefore=0,splitLongWords=False,
                                                   spaceShrinkage=0.05,))
  ################ T A B L A S ################
  t=Table([["Fecha:", str(timeDate)], ["N° Contrato:", str("1501")], ["N° Cliente:", str("0325")]],rowHeights=4*mm, colWidths=40*mm, hAlign='RIGHT')
  t_style = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
  t.setStyle(t_style)

  t0_w1 = 7.8 * inch
  data0 = [[Paragraph("DATOS GENERALES DEL CLIENTE", medium_cell_style)]]
  t0 = Table(data0, colWidths=[t0_w1],rowHeights=4*mm)
  t_style0 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t0.setStyle(t_style0)

  t1_w1, t1_w2 = 5.8 * inch, 2 * inch
  data1 = [[Paragraph("NOMBRE DEL TITULAR O RAZÓN SOCIAL: "+"DISEÑO DE REDES DE DATOS VILLA WIRELESS S.A DE C.V", small_cell_style),Paragraph("GIRO: "+"RESIDENCIAL", small_cell_style)]]
  t1 = Table(data1, colWidths=[t1_w1,t1_w2],rowHeights=4*mm)
  t1.setStyle(t_style)

  t2_w1, t2_w2, t2_w3, t2_w4 = 2 * inch, 2 * inch, 2 * inch, 1.8 * inch
  data2 = [[Paragraph("SERVICIO: "+"INSTALACIÓN NUEVA", small_cell_style), Paragraph("CONTACTO: "+"3133298336", small_cell_style), Paragraph("E-MAIL: "+"adrianfime27@gmail.com", small_cell_style),Paragraph("EQUIPO: "+"PRESTADO", small_cell_style)]]
  t2 = Table(data2, colWidths=[t2_w1, t2_w2, t2_w3, t2_w4],rowHeights=4*mm)
  t2.setStyle(t_style)

  t3_w1, t3_w2, t3_w3, t3_w4 = 2.2 * inch, 1 * inch, 2.6 * inch, 2 * inch
  data3 = [[Paragraph("CALLE: "+"PASEO DE PRIMAVERAS", small_cell_style), Paragraph("NÚMERO: "+"196", small_cell_style), Paragraph("COLONIA: "+"JARDINES DE BUGAMBILIAS", small_cell_style), Paragraph("LOCALIDAD: "+"VILLA DE ALVAREZ", small_cell_style)]]
  t3 = Table(data3, colWidths=[t3_w1, t3_w2, t3_w3, t3_w4],rowHeights=4*mm)
  t3.setStyle(t_style)

  t4_w1, t4_w2, t4_w3, t4_w4 = 1.9 * inch, 1.9 * inch, 3 * inch, 1 * inch
  data4 = [[Paragraph("MUNICIPIO: "+"VILLA DE ALVAREZ", small_cell_style), Paragraph("ESTADO: "+"COLIMA", small_cell_style), Paragraph("FORMA DE PAGO: "+"TRANSFERENCIA ELECTRÓNICA", small_cell_style), Paragraph("FACTURA: "+"SI", small_cell_style)]]
  t4 = Table(data4, colWidths=[t4_w1, t4_w2, t4_w3, t4_w4],rowHeights=4*mm)
  t4.setStyle(t_style)

  t5_w1, t5_w2, t5_w3 = 2.4 * inch, 3 * inch, 2.4 * inch
  data5 = [[Paragraph("PAQUETE: "+"100 MB", small_cell_style),Paragraph("TOTAL INSTALACIÓN+EQUIPOS: "+"$1320.00", small_cell_style), Paragraph("COSTO MENSUAL: "+"$350.00", small_cell_style)]]
  t5 = Table(data5, colWidths=[t5_w1, t5_w2, t5_w3],rowHeights=4*mm)
  t5.setStyle(t_style)

  t6_w1 = 7.8 * inch
  data6 = [[hequipos]]
  t6 = Table(data6, colWidths=[t6_w1],rowHeights=4*mm,hAlign='CENTER')
  t_style6 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE") ,("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t6.setStyle(t_style6)

  t7_w1, t7_w2, t7_w3, t7_w4 = 1.4 * inch, 1.2 * inch, 1.2 * inch, 4 * inch
  data7 = [[hnoserie, hmarca, hmodelo, hdescripcion]]
  t7 = Table(data7, colWidths=[t7_w1, t7_w2, t7_w3, t7_w4],rowHeights=4.5*mm,hAlign='CENTER')
  t_style7 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "LEFT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE") ,("BACKGROUND", (0,0), (-1,-1), '#b8bdbf')])
  t7.setStyle(t_style7)

  t8_w1, t8_w2, t8_w3, t8_w4 = 1.4 * inch, 1.2 * inch, 1.2 * inch, 4 * inch
  # Crear data2 con párrafos justificados
  data8 = [[Paragraph(str(listaAsignacion[x][0]), cell_style),
            Paragraph(str(listaAsignacion[x][1]), cell_style),
            Paragraph(str(listaAsignacion[x][2]), cell_style),
            Paragraph(str(listaAsignacion[x][3]), cell_style)] for x in range(len(listaAsignacion))]
  t8 = Table(data8, colWidths=[t8_w1, t8_w2, t8_w3, t8_w4],rowHeights=4*mm,hAlign='CENTER')
  t_style8 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE") ,("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t8.setStyle(t_style8)

  t9_w1 = 7.8 * inch
  data9 = [[p_text24]]
  t9 = Table(data9, colWidths=[t9_w1],rowHeights=4*mm,hAlign='CENTER')
  t_style9 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t9.setStyle(t_style9)

  t10_w1 = 7.8 * inch
  data10 = [[p_text25]]
  t10 = Table(data10, colWidths=[t10_w1],rowHeights=17*mm,hAlign='CENTER')
  t_style10 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t10.setStyle(t_style10)

  data11 = [[b,b,b]]
  t11 = Table(data11, colWidths=50*mm,rowHeights=15*mm,hAlign='CENTER')
  t_style11 = TableStyle([("BOX",(0,0),(-1,-1),0.5,colors.black),("GRID",(0,0),(-1,-1),0.5,colors.black),("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0,0), (-1,-1), '#ffffff')])
  t11.setStyle(t_style11)

  data12 = [[clientetable,empresatable,tecnicotable]]
  t12 = Table(data12, colWidths=50*mm,rowHeights=8*mm)
  t12.setStyle(t_style)
  ################ B U I L D ##############
  document.append(Spacer(1,10))
  document.append(t)
  ####  TITULO DE ARCHIVO ####
  document.append(Spacer(1,10))
  document.append(p_text1)
  ###### ENCABEZADO ARCHIVO ######
  document.append(Spacer(1,5))
  document.append(t0)
  document.append(t1)
  document.append(t2)
  document.append(t3)
  document.append(t4)
  document.append(t5)
  document.append(Spacer(1,5))
  document.append(p_text3)
  document.append(p_text4)
  document.append(p_text5)
  document.append(p_text6)
  document.append(p_text7)
  document.append(p_text8)
  document.append(Spacer(1,5))
  #### CLAUSULAS ####
  document.append(p_text10)
  document.append(p_text11)
  document.append(p_text12)
  document.append(p_text13)
  document.append(p_text14)
  document.append(p_text15)
  document.append(p_text16)
  document.append(p_text17)
  document.append(p_text18)
  document.append(p_text19)
  document.append(p_text20)
  document.append(p_text21)
  document.append(p_text22)
  document.append(p_text23)
  #### ENCABEZADO DE TABLA ####
  document.append(t6)
  document.append(t7)
  document.append(t8)
  document.append(Spacer(1,8))
  #### PAGARÉ ####
  document.append(t9)
  document.append(t10)
  document.append(Spacer(1,8))
  #### FIRMAS ####
  document.append(t11)
  document.append(t12)
  doc.build(document,onFirstPage=_header_footer_portrait,onLaterPages=_header_footer_portrait)
#  rootDoc = {'rutaDoc':routePDF+timeDate+'-'+usuarioA+'-asig'+extensionDoc}
#  rootDoc = json.dumps(rootDoc)
#  rutaDocument = routePDF+timeDate+'-'+usuarioA+'-asig'+extensionDoc
  # Leer el archivo PDF
#  with open(rutaDocument, 'rb') as file:
#      pdf_data = file.read()
#  ### Codificar el PDF en base64
#  pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
#  ## Guardar el PDF codificado en Redis
#  #r.set(fecha+'-'+usuarioA+'-asig', pdf_base64)
#  try:
#    result = r.publish("downloadFileAsig",rootDoc)
#    time.sleep(0.3)
#  except Exception as e:
#    print(e)
#
  ######################  M  A   I   N  ######################
if __name__ == "__main__":
    try:
        r = StrictRedis(host='192.168.100.127',port=6379,db=0,health_check_interval=30,socket_keepalive=True)
    except Exception as e:
        print(e)
    try:
        redisclientrts = Client(host='192.168.100.127',port=6379,socket_keepalive=True,retry_on_timeout=True)
    except Exception as e:
        print(e)

    client1 = Listener1(r,redisclientrts, ['yi_pdfs_iis_comprado', 'yi_pdfs_iis_comodato'])
    client1.start()