from datetime import datetime, timezone
from eventos.models import IntervencionEje, IntervencionVehiculo


# Filtramos los mantenimientos que vamos a mostrar de un eje por fechas
def filtrar_intervenciones_eje(filtro, id_eje):

    inicio_naive = datetime.strptime(filtro['inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
    inicio = inicio_naive.replace(tzinfo=timezone.utc)
    fin_naive = datetime.strptime(filtro['fin'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fin = fin_naive.replace(tzinfo=timezone.utc)
    num_max = filtro['num_max']

    intervenciones1 = IntervencionEje.objects.filter(eje = id_eje).order_by('-id')
    intervenciones2 = intervenciones1.filter(inicio__gte = inicio)
    intervenciones = intervenciones2.filter(fin__lte = fin)[:num_max]
    
    return intervenciones

# Filtramos los mantenimientos que vamos a mostrar de un vagón por fechas
def filtrar_intervenciones_vehiculo(filtro, id_vehiculo):

    inicio_naive = datetime.strptime(filtro['inicio'], "%Y-%m-%dT%H:%M:%S.%fZ")
    inicio = inicio_naive.replace(tzinfo=timezone.utc)
    fin_naive = datetime.strptime(filtro['fin'], "%Y-%m-%dT%H:%M:%S.%fZ")
    fin = fin_naive.replace(tzinfo=timezone.utc)
    num_max = filtro['num_max']

    intervenciones1 = IntervencionVehiculo.objects.filter(vehiculo = id_vehiculo).order_by('-id')
    intervenciones2 = intervenciones1.filter(inicio__gte = inicio)
    intervenciones = intervenciones2.filter(fin__lte = fin)[:num_max]
    
    return intervenciones