import re

from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError

from .models import Estudiante, Curso, Nota


class NotaService:
    """
    Servicio encargado de gestionar las operaciones
    y reglas de negocio de las calificaciones.
    """

    @staticmethod
    def _validar_datos(datos):
        """
        Valida los datos antes de registrar o editar.
        """

        if not isinstance(datos, dict):
            raise ValueError("Formato de datos incorrecto.")

        try:
            estudiante_id = int(datos["estudiante"])
            curso_id = int(datos["curso"])

            calificacion = Decimal(
                str(datos["calificacion"])
            )

            periodo = datos["periodo"]

            if (
                estudiante_id <= 0
                or curso_id <= 0
                or not calificacion.is_finite()
                or not isinstance(periodo, str)
            ):
                raise ValueError()


            periodo = periodo.strip()

            # Formato permitido: 4 dígitos, guion y periodo
            # Ejemplos: 2026-I, 2026-II
            if not re.fullmatch(r"[0-9]{4}-(I|II)", periodo):
                raise ValueError("Formato de periodo inválido.")


            estudiante = Estudiante.objects.get(
                pk=estudiante_id
            )

            curso = Curso.objects.get(
                pk=curso_id
            )

            return (
                estudiante,
                curso,
                calificacion,
                periodo
            )

        except (
            KeyError,
            ValueError,
            TypeError,
            InvalidOperation,
            Estudiante.DoesNotExist,
            Curso.DoesNotExist
        ) as error:
            raise ValueError(
                "Datos de la nota inválidos."
            ) from error

    @staticmethod
    def listar():
        """
        Consulta las notas con sus relaciones.
        """

        return Nota.objects.select_related(
            "estudiante",
            "curso"
        ).order_by("-fecha_registro", "-id")

    @classmethod
    def crear(cls, datos):
        """
        Registra una calificación.
        """

        estudiante, curso, calificacion, periodo = (
            cls._validar_datos(datos)
        )

        nota = Nota(
            estudiante=estudiante,
            curso=curso,
            calificacion=calificacion,
            periodo=periodo
        )

        nota.full_clean()
        nota.save()

        return nota

    @classmethod
    def actualizar(cls, nota, datos):
        """
        Modifica una calificación existente.
        """

        estudiante, curso, calificacion, periodo = (
            cls._validar_datos(datos)
        )

        nota.estudiante = estudiante
        nota.curso = curso
        nota.calificacion = calificacion
        nota.periodo = periodo

        nota.full_clean()
        nota.save()

        return nota

    @staticmethod
    def eliminar(nota):
        """
        Elimina una calificación.
        """

        nota.delete()
