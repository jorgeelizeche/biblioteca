from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Genero, Autor, Libro, Calificacion
from .serializers import (
    GeneroSerializer, AutorSerializer,
    LibroSerializer, CalificacionSerializer
)

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        libros = self.get_queryset()
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            libro = self.get_object()
            serializer = self.get_serializer(libro)
            return Response(serializer.data)
        except Libro.DoesNotExist:
            return Response({'detail': 'Libro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        libro = self.get_object()
        serializer = self.get_serializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        libro = self.get_object()
        libro.delete()
        return Response({'detail': 'Libro eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        generos = self.get_queryset()
        serializer = self.get_serializer(generos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            genero = self.get_object()
            serializer = self.get_serializer(genero)
            return Response(serializer.data)
        except Genero.DoesNotExist:
            return Response({'detail': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        genero = self.get_object()
        serializer = self.get_serializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        genero = self.get_object()
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        autores = self.get_queryset()
        serializer = self.get_serializer(autores, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            autor = self.get_object()
            serializer = self.get_serializer(autor)
            return Response(serializer.data)
        except Autor.DoesNotExist:
            return Response({'detail': 'Autor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        autor = self.get_object()
        serializer = self.get_serializer(autor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        autor = self.get_object()
        autor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        calificaciones = self.get_queryset()
        serializer = self.get_serializer(calificaciones, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            calificacion = self.get_object()
            serializer = self.get_serializer(calificacion)
            return Response(serializer.data)
        except Calificacion.DoesNotExist:
            return Response({'detail': 'Calificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        libro_id = request.data.get('libro_id')
        usuario = request.user

        if Calificacion.objects.filter(libro_id=libro_id, usuario=usuario).exists():
            return Response({'detail': 'Ya has calificado este libro.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        calificacion = self.get_object()
        serializer = self.get_serializer(calificacion, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        calificacion = self.get_object()
        calificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)