from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Genero, Autor, Libro, Calificacion

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nombre']


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad']


class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)
    genero = GeneroSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), source='autor', write_only=True)
    genero_id = serializers.PrimaryKeyRelatedField(queryset=Genero.objects.all(), source='genero', write_only=True)

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'fecha_de_lanzamiento', 'url_del_libro', 'autor', 'genero', 'autor_id', 'genero_id']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CalificacionSerializer(serializers.ModelSerializer):
    libro_id = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all(), source='libro')
    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Calificacion
        fields = ['id', 'libro_id', 'usuario', 'puntuacion']
