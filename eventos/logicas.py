from datetime import datetime, timedelta, timezone
from eventos.models import CambioEje, OperacionCambio, CirculacionEje, CirculacionVehiculo

# Calculamos el rango temporal antes y despues de dt para hacer la query a mongodb sobre los mensajes 
def calcular_rango_evento (dt, rango):
    '''Función que comprueba si dt es una fecha válida'''
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    if isinstance(dt, datetime):
        dt_fin = dt + timedelta(seconds=rango)
        dt_inicio = dt - timedelta(seconds=rango)
    else:
        dt_fin = datetime.now()
        dt_inicio = dt_fin - timedelta(seconds=rango)
    
    return dt_inicio, dt_fin

# Filtramos las circulaciones que vamos a mostrar de un eje por fechas
def filtrar_circulaciones_eje(filtro, id_eje):

    inicio_naive = datetime.strptime(filtro['inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
    inicio = inicio_naive.replace(tzinfo=timezone.utc)
    fin_naive = datetime.strptime(filtro['fin'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fin = fin_naive.replace(tzinfo=timezone.utc)
    num_max = filtro['num_max']

    Circulaciones1 = CirculacionEje.objects.filter(eje = id_eje).order_by('-id')
    Circulaciones2 = Circulaciones1.filter(dt_inicial__gte = inicio)
    Circulaciones = Circulaciones2.filter(dt_final__lte = fin)[:num_max]
    
    return Circulaciones

# Filtramos las circulaciones que vamos a mostrar de un vagón por fechas
def filtrar_circulaciones_vehiculo(filtro, id_vehiculo):

    inicio_naive = datetime.strptime(filtro['inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
    inicio = inicio_naive.replace(tzinfo=timezone.utc)
    fin_naive = datetime.strptime(filtro['fin'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fin = fin_naive.replace(tzinfo=timezone.utc)
    num_max = filtro['num_max']

    Circulaciones1 = CirculacionVehiculo.objects.filter(vehiculo = id_vehiculo).order_by('-id')
    Circulaciones2 = Circulaciones1.filter(dt_inicial__gte = inicio)
    Circulaciones = Circulaciones2.filter(dt_final__lte = fin)[:num_max]
    
    return Circulaciones

# Filtramos los eventos que vamos a mostrar de un eje por fechas
def filtrar_cambios_eje(filtro, id_eje):

    inicio_naive = datetime.strptime(filtro['inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
    inicio = inicio_naive.replace(tzinfo=timezone.utc)
    fin_naive = datetime.strptime(filtro['fin'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fin = fin_naive.replace(tzinfo=timezone.utc)
    num_max = filtro['num_max']

    cambios = CambioEje.objects.filter(eje = id_eje).order_by('-inicio')
    cambios2 = cambios.filter(inicio__gte = inicio)
    cambios3 = cambios2.filter(inicio__lte = fin)[:num_max]
 
    return cambios3

# Filtramos las operaciones de cambio que vamos a mostrar por fechas
def filtrar_operaciones_cambio(filtro):

    inicio_naive = datetime.strptime(filtro['inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
    inicio = inicio_naive.replace(tzinfo=timezone.utc)
    fin_naive = datetime.strptime(filtro['fin'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fin = fin_naive.replace(tzinfo=timezone.utc)
    num_max = filtro['num_max']

    operaciones1 = OperacionCambio.objects.filter(dt__gte = inicio)
    operaciones = operaciones1.filter(dt__lte = fin).order_by('-id')[:num_max]
 
    return operaciones