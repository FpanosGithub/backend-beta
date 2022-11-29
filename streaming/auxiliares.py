from cmath import atan
from vehiculos.models import Eje
from eventos.models import CirculacionVehiculo, EventoVehiculo, AlarmaVehiculo
from red_ferroviaria.models import PuntoRed
import math
from datetime import date, timedelta

ACC_MAXIMA_EJE_X = 5.1
ACC_MAXIMA_EJE_Y = 7.4
ACC_MAXIMA_EJE_Z = 12.2

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIONES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def limpiar_ejes_sueltos(vehiculo, lista_ejes):
    '''Función que busca si hay ejes que se han quedado colgados y los quita del vagón'''
    # Quitamos los ejes que no están
    posibles_ejes = Eje.objects.filter(vehiculo = vehiculo)
    for eje in posibles_ejes:
        if eje.codigo not in lista_ejes:
            eje.vehiculo = None
            eje.save()
     
def punto_red (lng, lat):
    ''' Función que busca si estamos en un punto singular de la red '''
    try:
        puntored = PuntoRed.objects.filter(lng = lng).filter(lat = lat)
    except:
        return None, False

    return None, False  
    # return puntored, puntored.nudo

def umbral_temperaturas(tempa, tempb):
    ''' Función que determina si hemos pasado los umbrales de temperaturas admisibles + Delta -> return 1
        Si estamos por debajo los umbrales de temperaturas admisibles - Delta -> return - 1 
        o si estamos en valores de umbrales +/- Delta -> return 0
    '''
    existe = False
    mensaje = ''

    if tempa >75:
        existe = True
        mensaje = 'Temperatura de rueda A supera MÁXIMO'
    elif tempa < -20:
        existe = True
        mensaje = 'Temperatura de rueda A inferior a MÍNIMO'
    elif tempb >75:
        existe = True
        mensaje = 'Temperatura de rueda b supera MÁXIMO'
    elif tempb < -20:
        existe = True
        mensaje = 'Temperatura de rueda B inferior a MÍNIMO'
    else:
        existe = False
        mensaje = ''
    return {'existe': existe, 'mensaje': mensaje, 'tipo': 'TEMPERATURA'}
             
def umbral_aceleraciones(axMa,axMb,ayMa,ayMb,azMa,azMb):
    ''' Función que determina si hemos pasado los umbrales
        de aceleraciones máximas
    '''
    existe = False
    mensaje = ''

    if axMa > ACC_MAXIMA_EJE_X:
        existe = True
        mensaje = 'aceleración X de rueda A supera MÁXIMO'
    if axMb > ACC_MAXIMA_EJE_X:
        existe = True
        mensaje = 'aceleración X de rueda B supera MÁXIMO'
    if ayMa > ACC_MAXIMA_EJE_Y:
        existe = True
        mensaje = 'aceleración Y de rueda A supera MÁXIMO'
    if ayMb > ACC_MAXIMA_EJE_Y:
        existe = True
        mensaje = 'aceleración Y de rueda B supera MÁXIMO'
    if azMa > ACC_MAXIMA_EJE_Z:
        existe = True
        mensaje = 'aceleración Z de rueda A supera MÁXIMO'
    if azMb > ACC_MAXIMA_EJE_Z:
        existe = True
        mensaje = 'aceleración Z de rueda B supera MÁXIMO' 

    return {'existe': existe, 'mensaje': mensaje, 'tipo': 'CIRCULACION'}

def tipo_evento(parado_ini, distancia, duracion, en_nudo_ini, en_nudo_fin):
    ''' Devuelve que tipo de evento se ha producido '''
    evento = None
    # Si está arrancando -> EVENTO ARRANQUE
    if parado_ini == True and distancia > 0:   
        evento = 'START'
    # Si está parando -> EVENTO PARADA
    elif parado_ini == False and distancia == 0:
        evento = 'STOP'
    # Si está en circulación -> Miramos si hay EVENTO NUDO o EVENTO INTERMEDIO
    elif parado_ini == False and distancia > 0:                                            
        # Si entramos en NUDO ferroviario -> EVENTO NUDO
        if en_nudo_fin == True and en_nudo_ini == False: # entramos en NUDO ferroviario
            evento = 'NUDO'
        # Si ha pasado un tiempo sin eventos -> EVENTO INTERMEDIO (de control)
        elif duracion.total_seconds() > 1.200:      
            evento = 'CIRC'
    return evento

def distancia_km (lng_ini, lat_ini, lng_fin, lat_fin):
    '''Calculamos la distancia en km entre 2 puntos: ini y fin'''
    # The earth's radius in kilometers.
    R = 6372.7955 
    rad = math.pi/180
    D_Lo = lng_fin - lng_ini 
    D_La = lat_fin - lat_ini 
    a = (math.sin(rad * D_La / 2))**2 + math.cos(rad * lat_ini) * math.cos(rad * lat_fin) * (math.sin(rad * D_Lo / 2))**2  
    distancia = 2 * R * math.asin(math.sqrt(a))
    
    # Resultado
    return round(distancia, 2)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIÓN AUXILIAR DE CIRCULACIÓN PARA LIMPIAR CÓDIGO DE: circulacion.py
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def evento_circulacion (ini, fin, vehiculo):
    # BUSCAMOS LA ÚLTIMA CIRCULACIÓN ABIERTA PARA ACTUALIZARLA O PARA CERRARLA Y ABRIR UNA NUEVA
    circulacion_1 = CirculacionVehiculo.objects.filter(vehiculo = vehiculo.id, abierta = True).last()      
    circulacion_2 = None
    circulacion_activa = 1
    nueva_alarma = False

    # SEGÚN EL TIPO DE EVENTO ACTUAMOS: 
    # 1. Si el evento es STOP:
    if fin.tipo_evento == 'STOP':
        # 1.1 Cerramos circulacion abierta si la hay con valores del evento (valores finales)
        if circulacion_1:
            circulacion_1.dt_final = fin.dt
            circulacion_1.lat_final = fin.lat
            circulacion_1.lng_final = fin.lng
            circulacion_1.alarma = fin.alarma['existe']
            circulacion_1.abierta = False     #¡** cerrada  **!
            circulacion_1.save()              #¡** guardada **!
        # 2. Si el evento es START:
    elif fin.tipo_evento == 'START':
        # 2.1 Si hay circulacion abierta, la cerramos con valores iniciales o 'de antes del evento. 
        if circulacion_1:
            circulacion_1.dt_final = ini.dt
            circulacion_1.lat_final = ini.lat
            circulacion_1.lng_final = ini.lng
            circulacion_1.alarma = fin.alarma['existe']
            circulacion_1.abierta = False     #¡** cerrada  **!
            circulacion_1.save()              #¡** guardada **!
        # 2.2 Abrimos nueva circulación con valores finales o 'del evento'
        CirculacionVehiculo(
            vehiculo= vehiculo, 
            abierta = True,
            dt_inicial = fin.dt,
            lng_inicial = fin.lng,
            lat_inicial = fin.lat,
            dt_final = fin.dt,
            lng_final = fin.lng,
            lat_final = fin.lat,
            alarma = fin.alarma['existe']
            ).save()  
        circulacion_2 = CirculacionVehiculo.objects.filter(vehiculo = vehiculo, abierta = True).last()     
        circulacion_activa = 2
    # 3. Si el evento es CIRC actualizamos valores circulacion abierta si la hay. Si no hay, Abrimos nueva
    elif fin.tipo_evento == 'CIRC':
        # 3.1 Si hay circulacion abierta, actualizamos con valores del evento (finales). 
        if circulacion_1:
            circulacion_1.dt_final = fin.dt
            circulacion_1.lng_final = fin.lng
            circulacion_1.lat_final = fin.lat
            circulacion_1.alarma = fin.alarma['existe']
            circulacion_1.abierta = True
            circulacion_1.save()      #¡** guardada **!
        # 3.2 Si No hay circulacion abierta, la creamos con valores del evento (finales). 
        else:
            CirculacionVehiculo(
                vehiculo= vehiculo, 
                abierta = True,
                dt_inicial = fin.dt,
                lng_inicial = fin.lng,
                lat_inicial = fin.lat,
                dt_final = fin.dt,
                lng_final = fin.lng,
                lat_final = fin.lat,
                ).save()
            circulacion_2 = CirculacionVehiculo.objects.filter(vehiculo = vehiculo, abierta = True).last()      
            circulacion_activa = 2
        
    # EVENTO VEHÍCULO => creamos nuevo
    if circulacion_activa ==1:
        circulacion = circulacion_1
    else:
        circulacion = circulacion_2   
    if circulacion:   
        EventoVehiculo(
            dt = fin.dt,
            vehiculo = vehiculo, 
            lng = fin.lng, 
            lat = fin.lat,
            punto_red = fin.puntored,
            evento = fin.tipo_evento,
            vel = fin.vel,
            alarma = fin.alarma['existe'],
            circulacion = circulacion,
            ).save()
        
    # ALARMA => Si hay nueva alarma creamos la nueva alarma
    if (not circulacion.alarma) and fin.alarma['existe']:
        nueva_alarma = True
    if nueva_alarma:
        AlarmaVehiculo (
            activa = True,
            vehiculo = vehiculo, 
            dt = fin.dt,
            tipo = 'CIRCULACION',
            mensaje = fin.alarma['mensaje'],
            ).save()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FUNCIÓNES AUXILIARES PARA ACTUALIZAR SITUACIÓN DE MANTENIMIENTO DE 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def actualizar_mantenimientos_vehiculo (vehiculo, distancia):
    # 0. Esto solo interesa si el Vehiculo ha circulado y/o ha pasado más de 1 dia 
    nivel_proximo = None
    if distancia > 0:
        km_menores = 100.000
        nivel_km_menores = None
        dias_menores = 1000
        nivel_dias_menores = None      
        # Elegimos cual es el proximo mantenimiento
        if dias_menores < 365:
            nivel_proximo = nivel_dias_menores
        else:
            nivel_proximo = nivel_km_menores
    
    return nivel_proximo

def actualizar_mantenimientos_eje (eje, distancia):
    # 0. Esto solo interesa si el vagón ha circulado y/o ha pasado más de 1 dia 
    nivel_proximo = None
    if distancia > 0:
        km_menores = 100.000
        nivel_km_menores = None
        dias_menores = 1000
        nivel_dias_menores = None      
        # Elegimos cual es el proximo mantenimiento
        if dias_menores < 365:
            nivel_proximo = nivel_dias_menores
        else:
            nivel_proximo = nivel_km_menores
    
    return nivel_proximo



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASES AUXILIARES 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class ObjetoPy(object):
    '''Convierte la estructuar en objetos con los nombres de las keys pero son todo tipo str'''
    def __init__(self, data):
        data = dict(data)
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if isinstance(value, list):
            return [self.compute_attr_value(x) for x in value]
        elif isinstance(value, dict):
            return ObjetoPy(value)
        else:
            return value



