from datetime import date
from vehiculos.models import Eje
from eventos.models import CirculacionEje, EventoEje, AlarmaEje
from streaming.auxiliares import umbral_temperaturas, umbral_aceleraciones, actualizar_mantenimientos_eje

ACC_TIPICA_EJE_X = 2.1
FREC_TIPICA_EJE_X = 12
ACC_TIPICA_EJE_Y = 3.4
FREC_TIPICA_EJE_Y = 12
ACC_TIPICA_EJE_Z = 5.2
FREC_TIPICA_EJE_Z = 12



class ObjCirculacionEje():
    ''' Guarda valores del mensaje de circulación, el objeto eje y el objeto circulación correspondientes a un eje '''
    def __init__(self, msg_eje):

        self.codigo = msg_eje.eje
        self._eje = Eje.objects.get(codigo = msg_eje.eje)
        self.tempa = msg_eje.tempa
        self.tempb = msg_eje.tempb
        self.alarma_temperatura = {'existe':False, 'mensaje': '', 'tipo':''}
        self.alarma_aceleraciones = {'existe':False, 'mensaje': '', 'tipo':''}
        self.nueva_alarma = False

        # 1.3 Aceleraciones
        # 1.3.1 Aceleracion eje X
        try: self.axMa = float(msg_eje.axMa)
        except: self.axMa = ACC_TIPICA_EJE_X   # Si no es un float -> le damos valor típico
        try: self.axmeda = float(msg_eje.axmeda)
        except: self.axmeda = ACC_TIPICA_EJE_X   # Si no es un float -> le damos valor típico
        try: self.axMb = float(msg_eje.axMb)
        except:self.axMb = ACC_TIPICA_EJE_X   # Si no es un float -> le damos valor típico
        try: self.axmedb = float(msg_eje.axmedb)
        except: self.axmedb = ACC_TIPICA_EJE_X   # Si no es un float -> le damos valor típico
        try: self.fxa = float(msg_eje.fxa)
        except:self.fxa = FREC_TIPICA_EJE_X   # Si no es un float -> le damos valor típico
        try: self.fxb = float(msg_eje.fxb)
        except: self.fxb = FREC_TIPICA_EJE_X   # Si no es un float -> le damos valor típico
        
        # 1.3.1 Aceleracion eje Y
        try: self.ayMa = float(msg_eje.ayMa)
        except: self.ayMa = ACC_TIPICA_EJE_Y   # Si no es un float -> le damos valor típico
        try: self.aymeda = float(msg_eje.aymeda)
        except: self.aymeda = ACC_TIPICA_EJE_Y   # Si no es un float -> le damos valor típico
        try: self.ayMb = float(msg_eje.ayMb)
        except: self.ayMb = ACC_TIPICA_EJE_Y   # Si no es un float -> le damos valor típico
        try: self.aymedb = float(msg_eje.aymedb)
        except: self.aymedb = ACC_TIPICA_EJE_Y   # Si no es un float -> le damos valor típico
        try: self.fya = float(msg_eje.fya)
        except: self.fya = FREC_TIPICA_EJE_Y   # Si no es un float -> le damos valor típico
        try: self.fyb = float(msg_eje.fyb)
        except: self.fyb = FREC_TIPICA_EJE_Y   # Si no es un float -> le damos valor típico

        # 1.3.1 Aceleracion eje Z
        try: self.azMa = float(msg_eje.azMa)
        except: self.azMa = ACC_TIPICA_EJE_Z   # Si no es un float -> le damos valor típico
        try: self.azmeda = float(msg_eje.azmeda)
        except: self.azmeda = ACC_TIPICA_EJE_Z   # Si no es un float -> le damos valor típico
        try: self.azMb = float(msg_eje.azMb)
        except: self.azMb = ACC_TIPICA_EJE_Z   # Si no es un float -> le damos valor típico
        try: self.azmedb = float(msg_eje.azmedb)
        except: self.azmedb = ACC_TIPICA_EJE_Z   # Si no es un float -> le damos valor típico
        try: self.fza = float(msg_eje.fza)
        except: self.fza = FREC_TIPICA_EJE_Z   # Si no es un float -> le damos valor típico
        try: self.fzb = float(msg_eje.fzb)
        except: self.fzb = FREC_TIPICA_EJE_Z   # Si no es un float -> le damos valor típico

       # BUSCAMOS LA ÚLTIMA CIRCULACIÓN ABIERTA PARA ACTUALIZARLA O PARA CERRARLA Y ABRIR UNA NUEVA
        self.circulacion_1 = CirculacionEje.objects.filter(eje=self._eje.id, abierta = True).last()      
        self.circulacion_2 = None
 

        
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # EVENTO => CirculacionEje / EventoEje / AlarmaEje
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def evento(self, ini, fin, vehiculo):

        circulacion_activa = 1
        # COMPROBAMOS SI LOS DATOS DEL MENSAJE PROVOCAN ALARMAS
        alarma = {'existe':False, 'mensaje': '', 'tipo':''}
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Comprobaciones a realizar con I.A en siguiente fase de desarrollo
        self.alarma_temperatura = umbral_temperaturas(self.tempa, self.tempb)
        self.alarma_aceleraciones = umbral_aceleraciones(
            self.axMa, 
            self.axMb,
            self.ayMa,
            self.ayMb,
            self.azMa,
            self.azMb)

        # SEGÚN EL TIPO DE EVENTO QUE HAYA RESULTADO DEL MENSAJE DE CIRCULACIÓN, ACTUAMOS:   
        # 1. Si el evento es STOP:
        if fin.tipo_evento == 'STOP':
            # 1.1 Cerramos circulacion abierta si la hay con valores del evento (valores finales)
            if self.circulacion_1:
                self.circulacion_1.dt_final = fin.dt
                self.circulacion_1.lat_final = fin.lat
                self.circulacion_1.lng_final = fin.lng
                self.circulacion_1.alarma = alarma['existe']
                self.circulacion_1.abierta = False          #¡** cerrada  **!
                self.circulacion_1.save()                   #¡** guardada **!

        # 2. Si el evento es START:
        elif fin.tipo_evento == 'START':         
            # 2.1 Si hay circulacion abierta, la cerramos con valores iniciales o 'de antes del evento'. 
            if self.circulacion_1:
                self.circulacion_1.dt_final = ini.dt
                self.circulacion_1.lng_final = ini.lng
                self.circulacion_1.lat_final = ini.lat
                self.circulacion_1.alarma = alarma['existe']
                self.circulacion_1.abierta = False         #¡** cerrada  **!
                self.circulacion_1.save()                  #¡** guardada **!
            # 2.2 Abrimos nueva circulación con valores finales o 'del evento'
            CirculacionEje(
                eje=self._eje, 
                abierta = True,
                en_vehiculo = vehiculo,
                dt_inicial = fin.dt,
                lng_inicial = fin.lng,
                lat_inicial = fin.lat,
                dt_final = fin.dt,
                lng_final = fin.lng,
                lat_final = fin.lat,
                alarma = alarma['existe'],
                ).save() # ***
            self.circulacion_2 = CirculacionEje.objects.filter(eje = self._eje, abierta = True,).last()
            circulacion_activa = 2  
       # 3. Si el evento es CIRC actualizamos valores circulacion abierta si la hay. Si no hay, Abrimos nueva
        elif fin.tipo_evento == 'CIRC':
            # 3.1 Si hay circulacion abierta, actualizamos con valores del evento (finales). 
            if self.circulacion_1:
                self.circulacion_1.dt_final = fin.dt
                self.circulacion_1.lng_final = fin.lng
                self.circulacion_1.lat_final = fin.lat
                self.circulacion_1.alarma = alarma['existe']
                self.circulacion_1.abierta = True
                self.circulacion_1.save()      #¡** guardada **!
            # 3.2 Si No hay circulacion abierta, la creamos con valores del evento (finales). 
            else:
                CirculacionEje(
                eje=self._eje,  
                abierta = True,
                en_vehiculo = vehiculo,
                dt_inicial = fin.dt,
                lng_inicial = fin.lng,
                lat_inicial = fin.lat,
                dt_final = fin.dt,
                lng_final = fin.lng,
                lat_final = fin.lat,
                alarma = alarma['existe'],
                ).save()
                self.circulacion_2 = CirculacionEje.objects.filter(eje = self._eje, abierta = True,).last()
                circulacion_activa = 2 
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
        # CREAMOS EVENTO EJE       
        if circulacion_activa ==1:
            circulacion = self.circulacion_1
        else:
            circulacion = self.circulacion_2   
        if circulacion and fin.tipo_evento:   
            EventoEje(
                    dt = fin.dt,
                    eje = self._eje, 
                    en_vehiculo = vehiculo,
                    lng = fin.lng, 
                    lat = fin.lat,
                    punto_red = fin.puntored,
                    evento = fin.tipo_evento,
                    tempa = self.tempa,
                    tempb = self.tempb,
                    vel = fin.vel,
                    alarma = alarma['existe'],

                    circulacion = circulacion,
                    axMa = self.axMa,
                    axMb = self.axMb,
                    ayMa = self.ayMa,
                    ayMb = self.ayMb,
                    azMa = self.azMa,
                    azMb = self.azMb,
                    axmeda = self.axmeda,
                    axmedb = self.axmedb,
                    aymeda = self.aymeda,
                    aymedb = self.aymedb,
                    azmeda = self.azmeda,
                    azmedb = self.azmedb,
                    ).save() # ***

        # CREAMOS ALARMA EJE => Si hay nueva alarma creamos la nueva alarma
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.alarma_aceleraciones['existe']:
            alarma = self.alarma_aceleraciones
        elif self.alarma_temperatura['existe']:
            alarma = self.alarma_temperatura     
        if not circulacion.alarma and alarma['existe']:
            self.nueva_alarma = True
        if self.nueva_alarma:
            AlarmaEje (
                activa = True,
                eje = self._eje, 
                dt = fin.dt,
                tipo = alarma['tipo'],
                mensaje = alarma['mensaje'],
                ).save()    # ***

        return alarma
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # GUARDAMOS DATOS DEL EJE TRAS LA CIRCULACIÓN
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def guardar(self, fin, vehiculo, mercave_mongo):
        # Actualización de los mantenimientos del eje
        proximo_mantenimiento = actualizar_mantenimientos_eje (self._eje, fin.distancia)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # En que vagón va
        self._eje.vehiculo = vehiculo
        # Mantenimiento
        self._eje.km_proximo_mant = self._eje.km_proximo_mant - fin.distancia
        try: 
            self._eje.dias_proximo_mant = proximo_mantenimiento.dias
        except:
            self._eje.dias_proximo_mant = 1000
        # Estado de circulación   
        self._eje.alarma_temp = self.alarma_temperatura['existe']
        self._eje.alarma_aceleraciones = self.alarma_aceleraciones['existe']
        self._eje.tempa = self.tempa                 
        self._eje.tempb = self.tempb
        self._eje.lng = fin.lng
        self._eje.lat = fin.lat
        self._eje.vel = fin.vel
        self._eje.km_totales = self._eje.km_totales + fin.distancia
        if fin.en_movimiento:
            self._eje.estado = 'CIRCULANDO'
        else:
            self._eje.estado = 'PARADO'
        # ************************
        self._eje.save()
        # ************************


        msg= {
            'dt': fin.dt, 
            'tipo_msg':fin.tipo_msg,
            'eje':self.codigo,
            'en_vagon': vehiculo.codigo, 
            'lng':fin.lng, 
            'lat':fin.lat,
            'vel':fin.vel, 
            'tempa': self.tempa, 
            'tempb': self.tempb, 
            'axMa':self.axMa,
            'axMb':self.axMb,
            'ayMa':self.ayMa,
            'ayMb':self.ayMb,
            'azMa':self.azMa,
            'azMb':self.azMb,
            'axmeda':self.axmeda,
            'axmedb': self.axmedb,
            'aymeda': self.aymeda,
            'aymedb': self.aymedb,
            'azmedb': self.azmedb,
            'fxa': self.fxa,
            'fxb': self.fxb,
            'fya': self.fya,
            'fyb': self.fyb,
            'fza': self.fza,
            'fzb': self.fzb
        }
        # ************************
        mercave_mongo.circulaciones_ejes.insert_one(msg)
        # ************************