from vehiculos.models import Eje
from eventos.models import AlarmaEje, CambioEje
from datetime import datetime
import pytz

FMAX_TIPICA_DESENCERROJAMIENTO = 31
FMAX_TIPICA_CAMBIO = 26
FMIN_TIPICA_ENCERROJAMIENTO = 0.1

class ObjCambioEje():
    ''' Guarda valores del mensaje de cambio, y el objeto eje '''
    def __init__(self, msg_eje):
        # INICIALIZAMOS ALARMA
        self.alarma = {'existe':False, 'mensaje': ''}
        # OBJETO EJE
        self._eje = Eje.objects.get(codigo = msg_eje.eje)
        # DATETIME DEL CAMBIO QUE VAMOS A USAR
        try: self.inicio = datetime.strptime(msg_eje.inicio,'%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Europe/Madrid'))
        except: self.inicio = datetime.now()   
        # DATOS DEL MENSAJE
        self.valores = msg_eje       

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CHEQUEAMOS Y DISPARAMOS ALARMA
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def alarmas(self):
        ''' Si hay alarma creamos evento de eje y creamos alarma de cambio'''
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Mas adelante evaluaremos el cambio en el módulo de IA. Haremos
        # un request a la API correspondiente pasando los valores del cambio
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #||||||||   alarma = cambio.ml.predict(self.valores_cambio)   |||||||||
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # fuerza de descerrojamiento en ruedas A y B.
        if (self.valores.fdaM > FMAX_TIPICA_DESENCERROJAMIENTO) or (self.valores.fdbM > FMAX_TIPICA_DESENCERROJAMIENTO):
            self.alarma['existe'] = True
            self.alarma['mensaje'] = 'Fuerza excesiva en desencerrojamiento'
        # fuerza de descerrojamiento en ruedas A y B.
        elif (self.valores.fcaM > (FMAX_TIPICA_CAMBIO) or (self.valores.fcbM > FMAX_TIPICA_CAMBIO)):
            self.alarma['existe'] = True
            self.alarma['mensaje'] = 'Fuerza excesiva en cambio'
        # fuerza de descerrojamiento en ruedas A y B.
        elif (self.valores.feam < FMIN_TIPICA_ENCERROJAMIENTO) or (self.valores.febm < FMIN_TIPICA_ENCERROJAMIENTO):
            self.alarma['existe']
            self.alarma['mensaje'] = 'El disco despegado en encerrojamiento'

        return (self.alarma)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS DEL EJE TRAS LA CIRCULACIÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def guardar(self, operacion, cambiador, mercave_mongo):
        # Guardamos EJE
        self._eje.alarma_cambio = self.alarma['existe']
        self._eje.num_cambios = self._eje.num_cambios +1
        self._eje.save()
        
        # OBJETO CambioEje
        self.cambio_eje = CambioEje(
            operacion = operacion,
            eje = self._eje,
            num_cambio_eje = self._eje.num_cambios,
            cambiador = cambiador,
            alarma = self.alarma['existe'],
            inicio = self.inicio,               
            V = self.valores.V,
            FV = self.valores.FV, 
            # VALORES RUEDA A
            tdaM = self.valores.tdaM,
            fdaM = self.valores.fdaM,
            ddaM = self.valores.ddaM, 
            tcaM = self.valores.tcaM,
            fcaM = self.valores.fcaM, 
            dcaM = self.valores.dcaM,
            team = self.valores.team,
            feam = self.valores.feam,
            deam = self.valores.deam,
            # VALORES RUEDA B 
            tdbM = self.valores.tdbM,
            fdbM = self.valores.fdbM,
            ddbM = self.valores.ddbM,
            tcbM = self.valores.tcbM,
            fcbM = self.valores.fcbM,
            dcbM = self.valores.dcbM,
            tebm = self.valores.tebm,
            febm = self.valores.febm,
            debm = self.valores.debm).save()

        # Generamos AlarmaEje si existe
        if self.alarma['existe']:
            AlarmaEje(
                activa = self.alarma['existe'],
                eje = self._eje,
                dt = self.inicio,
                tipo = 'CAMBIO',
                mensaje = self.alarma['mensaje']
            ).save()
        
        # Guardamos cambio en Mongo
        msg= {
            'operacion': operacion.pk, 
            'eje': self._eje.codigo,
            'num_cambio_eje' : self._eje.num_cambios,
            'cambiador' : cambiador.codigo,
            'alarma' : self.alarma['existe'],
            'inicio' : self.inicio,               
            'V' : self.valores.V,
            'FV' : self.valores.FV, 
            # VALORES RUEDA A
            'tdaM' : self.valores.tdaM,
            'fdaM' : self.valores.fdaM,
            'ddaM' : self.valores.ddaM, 
            'tcaM' : self.valores.tcaM,
            'fcaM' : self.valores.fcaM, 
            'dcaM' : self.valores.dcaM,
            'team' : self.valores.team,
            'feam' : self.valores.feam,
            'deam' : self.valores.deam,
            # VALORES RUEDA B 
            'tdbM' : self.valores.tdbM,
            'fdbM' : self.valores.fdbM,
            'ddbM' : self.valores.ddbM,
            'tcbM' : self.valores.tcbM,
            'fcbM' : self.valores.fcbM,
            'dcbM' : self.valores.dcbM,
            'tebm' : self.valores.tebm,
            'febm' : self.valores.febm,
            'debm' : self.valores.debm,
            }
        mercave_mongo.cambios_ejes.insert_one(msg)

        # Generamos EventoEje
        #EventoEje(
        #    dt = self.inicio,
        #    eje = self._eje,
        #    en_vagon = self._eje.vagon,
        #    lng = self.cambio.cambiador.lng,
        #    lat = self.cambio.cambiador.lat,
        #    evento = 'CAMBIO',
        #    alarma = self.alarma['existe']
        #).save()