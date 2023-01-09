from vehiculos.models import Vehiculo

def filtrar_vehiculos(filtro):
    owners = filtro['filtro_vehiculos']['owners']
    keepers = filtro['filtro_vehiculos']['keepers']
    EEMs = filtro['filtro_vehiculos']['EEMs']
    #tipos_vehiculos = filtro['filtro_vehiculos']['tipos_vehiculos']

    filter = False
    if (owners or keepers or EEMs):
        filter = True
    if filter:
        if owners:
            vehiculos_owners = Vehiculo.objects.filter(owner__in = owners)
        else:
            vehiculos_owners = Vehiculo.objects.all()
        if keepers:
            vehiculos_keeepers = vehiculos_owners.filter(keeper__in = keepers)
        else:
            vehiculos_keeepers = vehiculos_owners
        if EEMs:
            vehiculos = vehiculos_keeepers.filter(EEM__in = EEMs)
        else:
            vehiculos = vehiculos_keeepers
        #if tipos_vehiculos:
        #    vehiculos = vehiculos_EEM.filter(tipo__in = tipos_vehiculos)
        #else:
        #    vehiculos = vehiculos_EEM
    else:
        vehiculos = Vehiculo.objects.all()

    return vehiculos.order_by('-id')



def filtrar_planes_mantenimiento_vehiculo(id_vehiculo):
    return []
    
