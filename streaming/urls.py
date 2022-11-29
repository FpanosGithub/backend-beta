from django.urls import path
from streaming.views import MensajeCirculacion, MensajeCambio

urlpatterns = [
    path('msg_circ', MensajeCirculacion, name = 'msg_circ'),
    path('msg_cambio', MensajeCambio, name = 'msg_cambio'),
]