from django.shortcuts import render
# importamos l¿nuestro http reponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# nuestro json render
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
# nuestro modelo y nuestro serializer
from toys.models import Toy
from toys.serializers import ToySerializer



# creamos nuestro Json response
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        # recibe los contenidos del JSON
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# por el metodo POST genera un error poner el csrf, para mostar datos
@csrf_exempt
def toy_list(request):
    # metodo get
    if request.method == 'GET':
        # todos los datos de la base de datos
        toys = Toy.objects.all()
        # todos los pasas por el serializer
        toys_serializer = ToySerializer(toys, many=True)
        return JSONResponse(toys_serializer.data)

    # metodo post es para crear
    elif request.method == 'POST':
        # primero paso la peticion a json
        toy_data = JSONParser().parse(request)
        # lo mismo
        toy_serializer = ToySerializer(data=toy_data)
        # verificar la validez
        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data,status=status.HTTP_201_CREATED)

        return JSONResponse(toy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# para editar, crear y eliminar

@csrf_exempt
def toy_detail(request, pk):

    try:
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    # por get solo devuelve uno 
    if request.method == 'GET':
        toy_serializer = ToySerializer(toy)
        
        return JSONResponse(toy_serializer.data)

    # actualizar lo mismo que post
    elif request.method == 'PUT':
        toy_data = JSONParser().parse(request)
        toy_serializer = ToySerializer(toy, data=toy_data)
        if toy_serializer.is_valid():
            toy_serializer.save()
            return JSONResponse(toy_serializer.data)
        return JSONResponse(toy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # eliminar
    elif request.method == 'DELETE':
        toy.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)