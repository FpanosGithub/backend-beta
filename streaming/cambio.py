from pymongo import MongoClient
from datetime import datetime
import pytz
from red_ferroviaria.models import Cambiador
from eventos.models import AlarmaCambiador, OperacionCambio, CambioEje
from streaming.cambio_eje import ObjCambioEje
from streaming.auxiliares import ObjetoPy

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLASE PRINCIPAL 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def RegistrarOperacionCambio(data):
    ''' Recoge los datos de request, los convierte a objetos python y tiene métodos para 
        disparar alarmas y guardar en Postgres y Mongo.
    '''    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Convierte mensaje JSON en objeto python !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    obj = ObjetoPy(data)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    alarma_cambiador = {'existe':False, 'mensaje':''}
    # VALIDAMOS FECHA/HORA
    try: dt = datetime.strptime(obj.dt,'%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Europe/Madrid'))
    except: dt = datetime.now()
    # EJES
    lista_ejes = []
    ejes = []
    for msg_eje in obj.msgs_ejes:
        lista_ejes.append(msg_eje.eje)
        ejes.append(ObjCambioEje(msg_eje))
    # CAMBIADOR
    cambiador = Cambiador.objects.get(codigo = obj.cambiador)
    cambiador.num_cambios = cambiador.num_cambios + len(lista_ejes)
    cambiador.save()
    # OPERACION CAMBIO
    OperacionCambio (
        dt = dt,
        cambiador = cambiador,
        sentido = obj.sentido
        ).save()   
    operacion = OperacionCambio.objects.last()  
    # ALARMAS
    for eje in ejes:
        alarma_eje = eje.alarmas()
        if alarma_eje['existe']: alarma_cambiador = alarma_eje
    if alarma_cambiador['existe']:
        AlarmaCambiador(
            activa = True,
            cambiador = cambiador,
            dt = dt,
            tipo = 'OPERACION',
            mensaje = alarma_cambiador['mensaje']
            ).save()
        operacion.alarma = True
        operacion.alarma_activa = True
        operacion.save()

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # inicializamos MONGO_DB para guardar mensajes de operación y ejes
    cluster = 'mongodb+srv://admintria:dpJPkafvGJPHXbnN@cluster0.2wbih.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)    
    mercave_mongo = client.mercave_mongo

    for eje in ejes:
        eje.guardar(operacion, cambiador, mercave_mongo)

                                                                                    