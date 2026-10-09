
from django.contrib import admin
from .models import Estudiante, Curso, Nota


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombres', 'apellidos', 'correo')
    search_fields = ('codigo', 'nombres', 'apellidos')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'creditos')
    search_fields = ('codigo', 'nombre')


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = (
        'estudiante',
        'curso',
        'calificacion',
        'periodo',
        'fecha_registro'
    )

    list_filter = ('periodo', 'curso')
    search_fields = (
        'estudiante__nombres',
        'estudiante__apellidos',
        'curso__nombre'
    )
