
# Sistema Web Seguro de Gestión de Notas UC

## Descripción del proyecto

Sistema web desarrollado como Trabajo Parcial del curso
Desarrollo de Aplicaciones Web de la Universidad Continental.

La aplicación permite gestionar calificaciones académicas
mediante una interfaz dinámica, una API REST y una base
de datos SQLite.

Es un proyecto académico independiente y no está
vinculado con los sistemas oficiales de la universidad.

## Tecnologías utilizadas

- Python y Django 6.1.2
- SQLite
- HTML5 y CSS3
- JavaScript (Vanilla JS)
- Fetch API y Async/Await
- JSON
- bcrypt
- python-dotenv
- Git y GitHub

## Funcionalidades

- Consultar las calificaciones registradas.
- Registrar nuevas notas.
- Editar calificaciones existentes.
- Eliminar notas con confirmación.
- Asociar estudiantes con cursos.
- Visualizar el estado aprobado o desaprobado.
- Actualizar la tabla sin recargar la página.
- Restringir el acceso a usuarios administrativos.

## Arquitectura del proyecto

El backend utiliza una arquitectura modular:

- `notas/models.py`: modelos de estudiantes, cursos y notas.
- `notas/views.py`: recepción de solicitudes y respuestas HTTP.
- `notas/services.py`: reglas de negocio y validaciones.
- `notas/urls.py`: rutas de la API REST.
- `notas/tests.py`: pruebas automatizadas.
- `templates/index.html`: interfaz HTML.
- `static/css/styles.css`: diseño responsivo.
- `static/js/app.js`: interacción y consumo de la API.

Se aplica el principio SOLID de Responsabilidad Única
(SRP), separando las responsabilidades entre módulos.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/DiegoSa55/gestion_notas_uc.git
cd gestion_notas_uc
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows CMD:

```cmd
venv\Scripts\activate.bat
```

En PowerShell, si la política de ejecución lo permite:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Generar una clave segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Agregar al archivo `.env`:

```dotenv
SECRET_KEY=REEMPLAZAR_CON_LA_CLAVE_GENERADA
```

No publicar la clave secreta.

### 6. Preparar la base de datos

```bash
python manage.py migrate
```

### 7. Crear un administrador

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor

```bash
python manage.py runserver
```

Abrir:

http://127.0.0.1:8000/

Panel administrativo:

http://127.0.0.1:8000/admin/

Registrar primero al menos un estudiante y un curso
desde el panel administrativo para utilizar el formulario
de calificaciones.

## API REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/notas/ | Consultar notas |
| POST | /api/notas/ | Registrar nota |
| PUT | /api/notas/{id}/ | Actualizar nota |
| DELETE | /api/notas/{id}/ | Eliminar nota |

Los endpoints requieren autenticación y permisos
administrativos.

Las operaciones de modificación requieren un token
CSRF válido.

## Seguridad implementada

- Hashing de contraseñas con bcrypt.
- Validación de datos en el backend.
- Control de autenticación y autorización.
- Protección CSRF.
- Consultas mediante el ORM de Django.
- Uso de `textContent` para mostrar datos en JavaScript.
- Variables de entorno para claves secretas.
- Archivo `.gitignore` para excluir información privada.

El servidor está configurado para desarrollo local.
Las opciones de HTTPS, HSTS y cookies seguras deben
configurarse antes de un despliegue público.

## Pruebas automatizadas

Ejecutar:

```bash
python manage.py test notas
```

Se implementaron 14 pruebas que comprueban operaciones,
validaciones, permisos y controles de seguridad.

## Autoría

Trabajo Parcial - Desarrollo de Aplicaciones Web

Universidad Continental - 2026

## Repositorio

https://github.com/DiegoSa55/gestion_notas_uc
