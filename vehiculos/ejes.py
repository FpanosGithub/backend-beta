from operator import truediv
from vehiculos.models import Eje

def filtrar_ejes(filtro):
    owners = filtro['filtro_ejes']['owners']
    keepers = filtro['filtro_ejes']['keepers']
    fabricantes = filtro['filtro_ejes']['fabricantes']
    EEMs = filtro['filtro_ejes']['EEMs']
    tipos_ejes = filtro['filtro_ejes']['tipos_ejes']

    filter = False
    if (owners or keepers or fabricantes or EEMs or tipos_ejes):
        filter = True
    if filter:
        if owners:
            ejes_owners = Eje.objects.filter(owner__in = owners)
        else:
            ejes_owners = Eje.objects.all()
        if keepers:
            ejes_keeepers = ejes_owners.filter(keeper__in = keepers)
        else:
            ejes_keeepers = ejes_owners
        if fabricantes:
            ejes_fabricantes = ejes_keeepers.filter(fabricante__in = fabricantes)
        else:
            ejes_fabricantes = ejes_keeepers
        if EEMs:
            ejes_mantenedores = ejes_fabricantes.filter(mantenedor__in = EEMs)
        else:
            ejes_mantenedores = ejes_fabricantes
        if tipos_ejes:
            ejes = ejes_mantenedores.filter(tipo_eje__in = tipos_ejes)
        else:
            ejes = ejes_mantenedores
    else:
        ejes = Eje.objects.all()

    return ejes.order_by('-id')