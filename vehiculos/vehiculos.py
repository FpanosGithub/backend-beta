from vehiculos.models import Vehiculo

def filtrar_vehiculos(filtro):
    owners = filtro['filtro_vehiculos']['owners']
    keepers = filtro['filtro_vehiculos']['keepers']
    EEMs = filtro['filtro_vehiculos']['EEMs']
    tipos_vehiculos = filtro['filtro_vehiculos']['tipos_vehiculos']

    filter = False
    if (owners or keepers or EEMs or tipos_vehiculos):
        filter = True
    if filter:
        if owners:
            vehiculos_operadores = Vehiculo.objects.filter(operador__in = owners)
        else:
            vehiculos_operadores = Vehiculo.objects.all()
        if keepers:
            vehiculos_keeepers = vehiculos_operadores.filter(keeper__in = keepers)
        else:
            vehiculos_keeepers = vehiculos_operadores
        if EEMs:
            vehiculos_EEM = vehiculos_keeepers.filter(mantenedor__in = EEMs)
        else:
            vehiculos_EEM = vehiculos_keeepers
        if tipos_vehiculos:
            vehiculos = vehiculos_EEM.filter(tipo__in = tipos_vehiculos)
        else:
            vehiculos = vehiculos_EEM
    else:
        vehiculos = Vehiculo.objects.all()

    return vehiculos.order_by('-id')