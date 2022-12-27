from pymongo import MongoClient
from datetime import datetime
import pytz
from streaming.auxiliares import punto_red, distancia_km, tipo_evento, evento_circulacion
from vehiculos.models import Vehiculo
from streaming.circulacion_eje import ObjCirculacionEje
from streaming.auxiliares import ObjetoPy, limpiar_ejes_sueltos

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class DatosIniciales():
    ''' Guarda valores finales de la circulación '''
    def __init__(self, vehiculo):
        self.dt = vehiculo.ultimo_evento_dt 
        self.lng = vehiculo.lng
        self.lat = vehiculo.lat
        if (vehiculo.estado_servicio == 'BAJA'): self.baja = True
        else: self.baja = False
        if (vehiculo.estado_servicio == 'MANTENIMIENTO'): self.mantenimiento = True
        else: self.mantenimiento = False
        if (vehiculo.estado_servicio == 'PARADO'): self.parado = True
        else: self.parado = False
        self.en_nudo = vehiculo.en_nudo   
        self.alarma = vehiculo.alarma 
class DatosFinales():
    ''' Guarda valores finales de la circulación '''
    def __init__(self, obj):
        try: self.dt = datetime.strptime(obj.dt,'%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Europe/Madrid'))
        except: self.dt = datetime.now()
        self.lng = float(obj.lng)
        self.lat = float(obj.lat) 
        self.vel = float(obj.vel)
        self.puntored, self.en_nudo = punto_red(self.lng, self.lat)     
        if obj.tipo_msg == 'SLEEP': self.transmitiendo = False
        else: self.transmitiendo = True
        self.alarma = {'existe':False, 'mensaje': ''}
        self.nueva_alarma = False
        self.en_movimiento = False
        self.distancia = 0
        self.duracion = 0
        self.tipo_msg = obj.tipo_msg
        self.tipo_evento = None

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIÓN PRINCIPAL 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def RegistraCirculacion(data):
    ''' Recoge los datos de request, los convierte a objetos python y tiene métodos para 
        disparar los eventos, alarmas y guardar en Postgres y Mongo.
    '''
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    obj = ObjetoPy(data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # COGEMOS EL OBJETO VAGÓN DE LA CIRCULACIÓN
    vehiculo = Vehiculo.objects.get(id = obj.vehiculo)
    # DATOS DE ANTES Y DESPUÉS DE LA CIRCULACIÓN
    ini = DatosIniciales(vehiculo)
    fin = DatosFinales (obj)   
    #¡¡¡ IMPORTANTE !!!
    # SI EL VAGÓN ESTÁ DE BAJA O EN MANTENIMIENTO NO SE PUEDE MOVER Y NO SE REGISTRA LA CIRCULACIÓN DE EL NI DE LOS EJES QUE LLEVA
    if ini.baja or ini.mantenimiento:
        respuesta = 'IMPOSIBLE CIRCULAR EL VEHÍCULO: ' + vehiculo.codigo + ', POR ENCONTRARSE EN ESTADO: ' + vehiculo.estado_servicio
        return respuesta

    # CALCULAMOS DISTANCIA, DURACIÓN Y TIPO DE EVENTO DE LA CIRCULACIÓN - LOS GUARDAMOS EN DATOS FINALES
    fin.distancia =  distancia_km (ini.lng, ini.lat, fin.lng, fin.lat) 
    if fin.distancia > 0: fin.en_movimiento = True     
    try: fin.duracion = (fin.dt - ini.dt)
    except: fin.duracion = 0  
    fin.tipo_evento = tipo_evento(ini.parado, fin.distancia, fin.duracion, ini.en_nudo, fin.en_nudo, )
 
    # EJES
    lista_ejes = []
    ejes = []
    for msg_eje in obj.msgs_ejes:
        lista_ejes.append(msg_eje.eje)
        ejes.append(ObjCirculacionEje(msg_eje))

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CHEQUEAMOS Y DISPARAMOS CIRCULACIONES, EVENTOS Y ALARMAS
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CIRCULACIONES, EVENTOS Y ALARMAS DE LOS DISTINTOS EJES
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for eje in ejes:
        alarma_eje = eje.evento(ini, fin, vehiculo)
        if alarma_eje['existe']: fin.alarma = alarma_eje
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CIRCULACIONES, EVENTOS Y ALARMAS DEL VAGÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    evento_circulacion(ini, fin, vehiculo) 
    # Actualización de los mantenimientos
    # proximo_mantenimiento = actualizar_mantenimientos_vehiculo (vehiculo, fin.distancia)
                                              
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS NUEVOS EN LOS EJES Y EN EL VAGÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # inicializamos MONGO_DB para guardar mensajes de vagón y ejes
    cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)    
    mercave_mongo = client.mercave_mongo
    # 1. Guardamos los nuevos datos de cada eje y los mensajes de cada eje en bruto en Mongo
    for eje in ejes:
        eje.guardar(fin, vehiculo, mercave_mongo)
    # 2. Guardamos los nuevos datos del vagón
    vehiculo.lng = fin.lng
    vehiculo.lat = fin.lat
    vehiculo.km_totales = vehiculo.km_totales + fin.distancia
    vehiculo.km_proximo_mant = vehiculo.km_proximo_mant - fin.distancia
    vehiculo.transmitiendo = fin.transmitiendo
    if fin.en_movimiento: vehiculo.estado_servicio = 'CIRCULANDO'
    else: vehiculo.estado_servicio = 'PARADO'
    vehiculo.alarma = fin.alarma['existe']
    vehiculo.ultimo_evento_dt = fin.dt
    vehiculo.en_nudo = fin.en_nudo
    vehiculo.vel = fin.vel
    vehiculo.save() # ***
    
    limpiar_ejes_sueltos (vehiculo, lista_ejes)
    
    # 4. Guardamos circulación - VEHICULO en mercave_mongo
    msg= {
        'dt': fin.dt.strftime("%m/%d/%Y %H:%M:%S"), 
        'tipo_msg':fin.tipo_msg,
        'vagon': vehiculo.id, 
        'lng':fin.lng, 
        'lat':fin.lat,
        'vel':fin.vel,
        }
    mercave_mongo.circulaciones_vehiculos.insert_one(msg) # ***

    respuesta = 'CIRCULACIÓN DEL VEHÍCULO: ' + vehiculo.matricula + ', REGISTRADA CON ÉXITO'
    return respuesta
    