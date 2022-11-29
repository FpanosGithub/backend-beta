from rest_framework.routers import SimpleRouter
from red_ferroviaria.views import Lineas, PuntosRed

router = SimpleRouter()
router.register('lineas', Lineas, basename = 'lineas')
router.register('puntos_red', PuntosRed, basename = 'puntos_red')

urlpatterns = router.urls