
from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.inicio,
        name='inicio'
    ),
    path(
        'api/notas/',
        views.listar_notas,
        name='listar_notas'
    ),
    path(
        'api/notas/<int:nota_id>/',
        views.detalle_nota,
        name='detalle_nota'
    ),
]
