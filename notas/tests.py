import json

from django.utils.html import escape
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Estudiante, Curso, Nota


class SeguridadNotasTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username="admin_prueba",
            password="ClaveSegura123!",
            is_staff=True
        )

        self.usuario = User.objects.create_user(
            username="usuario_prueba",
            password="ClaveSegura456!",
            is_staff=False
        )

        self.estudiante = Estudiante.objects.create(
            codigo="TEST001",
            nombres="Estudiante",
            apellidos="Prueba",
            correo="estudiante@example.com"
        )

        self.curso = Curso.objects.create(
            codigo="CUR001",
            nombre="Curso de prueba",
            creditos=3
        )

        self.nota = Nota.objects.create(
            estudiante=self.estudiante,
            curso=self.curso,
            calificacion=15,
            periodo="2026-II"
        )

    def test_visitante_no_puede_consultar_notas(self):
        respuesta = self.client.get(
            reverse("listar_notas")
        )

        self.assertEqual(respuesta.status_code, 401)

    def test_usuario_sin_permisos_no_puede_consultar(self):
        self.client.force_login(self.usuario)

        respuesta = self.client.get(
            reverse("listar_notas")
        )

        self.assertEqual(respuesta.status_code, 403)

    def test_administrador_puede_consultar_notas(self):
        self.client.force_login(self.admin)

        respuesta = self.client.get(
            reverse("listar_notas")
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.json()["total"],
            1
        )

    def test_administrador_puede_eliminar_nota(self):
        self.client.force_login(self.admin)

        respuesta = self.client.delete(
            reverse(
                "detalle_nota",
                args=[self.nota.id]
            )
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(
            Nota.objects.filter(
                id=self.nota.id
            ).exists()
        )

    def test_registrar_nota_valida(self):
        self.client.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 18,
            "periodo": "2026-II"
        }

        respuesta = self.client.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Nota.objects.count(), 2)

    def test_actualizar_nota(self):
        self.client.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 19,
            "periodo": "2026-II"
        }

        respuesta = self.client.put(
            reverse("detalle_nota", args=[self.nota.id]),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 200)

        self.nota.refresh_from_db()
        self.assertEqual(self.nota.calificacion, 19)

    def test_rechazar_nota_mayor_a_20(self):
        self.client.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 25,
            "periodo": "2026-II"
        }

        respuesta = self.client.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Nota.objects.count(), 1)

    def test_visitante_no_puede_eliminar(self):
        respuesta = self.client.delete(
            reverse("detalle_nota", args=[self.nota.id])
        )

        self.assertEqual(respuesta.status_code, 401)
        self.assertTrue(
            Nota.objects.filter(pk=self.nota.id).exists()
        )

    def test_usuario_sin_permiso_no_puede_registrar(self):
        self.client.force_login(self.usuario)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 16,
            "periodo": "2026-II"
        }

        respuesta = self.client.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 403)
        self.assertEqual(Nota.objects.count(), 1)

    def test_csrf_obligatorio_en_post(self):
        from django.test import Client

        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 18,
            "periodo": "2026-II"
        }

        respuesta = cliente.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 403)
        self.assertEqual(Nota.objects.count(), 1)

    def test_rechazar_periodo_con_html_malicioso(self):
        self.client.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 18,
            "periodo": "<script>alert(1)</script>"
        }

        respuesta = self.client.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Nota.objects.count(), 1)

    def test_escape_html_de_django(self):
        texto = "<script>alert(1)</script>"

        resultado = escape(texto)

        self.assertNotIn("<script>", resultado)
        self.assertIn("&lt;script&gt;", resultado)

    def test_rechazar_html_en_periodo(self):
        self.client.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 18,
            "periodo": "<b>2026-II</b>"
        }

        respuesta = self.client.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Nota.objects.count(), 1)

    def test_rechazar_periodo_incorrecto(self):
        self.client.force_login(self.admin)

        datos = {
            "estudiante": self.estudiante.id,
            "curso": self.curso.id,
            "calificacion": 18,
            "periodo": "PERIODO_INCORRECTO"
        }

        respuesta = self.client.post(
            reverse("listar_notas"),
            data=json.dumps(datos),
            content_type="application/json"
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(Nota.objects.count(), 1)
