from operator import truediv
from vehiculos.models import Eje

def filtrar_ejes(filtro):
    owners = filtro['filtro_ejes']['owners']
    keepers = filtro['filtro_ejes']['keepers']
    fabricantes = filtro['filtro_ejes']['fabricantes']
    EEMs = filtro['filtro_ejes']['EEMs']
    versiones_ejes = filtro['filtro_ejes']['versiones_ejes']

    filter = False
    if (owners or keepers or fabricantes or EEMs or versiones_ejes):
        filter = True
    if filter:
        if owners:
            ejes_operadores = Eje.objects.filter(operador__in = owners)
        else:
            ejes_operadores = Eje.objects.exclude(operador__in = owners)
        if keepers:
            ejes_keeepers = ejes_operadores.filter(keeper__in = keepers)
        else:
            ejes_keeepers = ejes_operadores.exclude(keeper__in = keepers)
        if fabricantes:
            ejes_fabricantes = ejes_keeepers.filter(fabricante__in = fabricantes)
        else:
            ejes_fabricantes = ejes_keeepers.exclude(fabricante__in = fabricantes)
        if EEMs:
            ejes_mantenedores = ejes_fabricantes.filter(mantenedor__in = EEMs)
        else:
            ejes_mantenedores = ejes_fabricantes.exclude(mantenedor__in = EEMs)
        if versiones_ejes:
            ejes = ejes_mantenedores.filter(version__in = versiones_ejes)
        else:
            ejes = ejes_mantenedores.exclude(version__in = versiones_ejes)
    else:
        ejes = Eje.objects.all()

    return ejes.order_by('-id')