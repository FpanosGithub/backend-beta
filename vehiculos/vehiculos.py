from vehiculos.models import Vehiculo

def filtrar_vehiculos(filtro):
    owners = filtro['filtro_vehiculos']['owners']
    keepers = filtro['filtro_vehiculos']['keepers']
    EEMs = filtro['filtro_vehiculos']['EEMs']
    #tipos_vagones = filtro['filtro_vehiculos']['tipos_vagones']

    filter = False
    if (owners or keepers or EEMs):
        filter = True
    if filter:
        if owners:
            vehiculos_operadores = Vehiculo.objects.filter(operador__in = owners)
        else:
            vehiculos_operadores = Vehiculo.objects.exclude(operador__in = owners)
        if keepers:
            vehiculos_keeepers = vehiculos_operadores.filter(keeper__in = keepers)
        else:
            vehiculos_keeepers = vehiculos_operadores.exclude(keeper__in = keepers)
        if EEMs:
            vehiculos = vehiculos_keeepers.filter(mantenedor__in = EEMs)
        else:
            vehiculos = vehiculos_keeepers.exclude(mantenedor__in = EEMs)
    else:
        vehiculos = Vehiculo.objects.all()

    return vehiculos.order_by('-id')