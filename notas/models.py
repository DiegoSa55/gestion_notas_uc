
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Estudiante(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Curso(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    creditos = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.nombre


class Nota(models.Model):
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name="notas"
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="notas"
    )

    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20)
        ]
    )

    periodo = models.CharField(max_length=20)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.curso}: {self.calificacion}"
