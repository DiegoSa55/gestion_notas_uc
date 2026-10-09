
import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Estudiante, Curso, Nota
from .services import NotaService


# Comprobar autenticacion y permisos
def verificar_acceso(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Debes iniciar sesión.'
        }, status=401)

    if not request.user.is_staff:
        return JsonResponse({
            'error': 'No tienes permisos para gestionar notas.'
        }, status=403)

    return None


# Vista principal
def inicio(request):
    if request.user.is_authenticated and request.user.is_staff:
        estudiantes = Estudiante.objects.all().order_by(
            'apellidos'
        )
        cursos = Curso.objects.all().order_by('nombre')
    else:
        estudiantes = Estudiante.objects.none()
        cursos = Curso.objects.none()

    return render(request, 'index.html', {
        'estudiantes': estudiantes,
        'cursos': cursos
    })


# API para consultar y registrar
@require_http_methods(["GET", "POST"])
def listar_notas(request):

    error = verificar_acceso(request)
    if error is not None:
        return error

    if request.method == "GET":
        notas = NotaService.listar()

        resultado = []

        for nota in notas:
            resultado.append({
                'id': nota.id,
                'estudiante_id': nota.estudiante_id,
                'curso_id': nota.curso_id,
                'estudiante': str(nota.estudiante),
                'curso': nota.curso.nombre,
                'calificacion': float(nota.calificacion),
                'periodo': nota.periodo,
                'fecha_registro': nota.fecha_registro.isoformat()
            })

        return JsonResponse({
            'total': len(resultado),
            'notas': resultado
        })

    try:
        datos = json.loads(request.body)
        nota = NotaService.crear(datos)

        return JsonResponse({
            'mensaje': 'Nota registrada correctamente.',
            'id': nota.id
        }, status=201)

    except (
        ValueError,
        ValidationError,
        json.JSONDecodeError
    ):
        return JsonResponse({
            'error': 'Los datos enviados no son válidos.'
        }, status=400)


# API para editar y eliminar
@require_http_methods(["PUT", "DELETE"])
def detalle_nota(request, nota_id):

    error = verificar_acceso(request)
    if error is not None:
        return error

    nota = get_object_or_404(Nota, pk=nota_id)

    if request.method == "DELETE":
        NotaService.eliminar(nota)

        return JsonResponse({
            'mensaje': 'Nota eliminada correctamente.'
        })

    try:
        datos = json.loads(request.body)
        nota = NotaService.actualizar(nota, datos)

        return JsonResponse({
            'mensaje': 'Nota actualizada correctamente.',
            'id': nota.id
        })

    except (
        ValueError,
        ValidationError,
        json.JSONDecodeError
    ):
        return JsonResponse({
            'error': 'Los datos enviados no son válidos.'
        }, status=400)
