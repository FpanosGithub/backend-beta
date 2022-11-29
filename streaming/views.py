from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from streaming.circulacion import RegistraCirculacion
from streaming.cambio import RegistrarOperacionCambio


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def MensajeCirculacion(request):
    resultado = RegistraCirculacion(request.data)
    print('')
    print(resultado)  
    print('')   
    return Response(request.data)

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def MensajeCambio(request):
    RegistrarOperacionCambio(request.data)
    return Response(request.data)
    