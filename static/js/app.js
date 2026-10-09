
let notasActuales = [];

document.addEventListener("DOMContentLoaded", () => {
    cargarNotas();

    const formulario = document.getElementById("form-nota");
    const cancelar = document.getElementById("boton-cancelar");

    if (formulario) {
        formulario.addEventListener("submit", guardarNota);
    }

    if (cancelar) {
        cancelar.addEventListener("click", cancelarEdicion);
    }
});


// Obtener el token CSRF de Django
function obtenerCSRF() {
    const campo = document.querySelector(
        '[name="csrfmiddlewaretoken"]'
    );

    return campo ? campo.value : "";
}


// Consultar todas las notas
async function cargarNotas() {
    const tabla = document.getElementById("tabla-notas");
    const mensaje = document.getElementById("mensaje-notas");

    tabla.replaceChildren();
    mensaje.textContent = "Cargando notas...";

    try {
        const respuesta = await fetch("/api/notas/", {
            credentials: "same-origin",
            headers: {
                "Accept": "application/json"
            }
        });

        if (respuesta.status === 401 || respuesta.status === 403) {
            mensaje.textContent =
                "Inicia sesión con una cuenta autorizada para consultar notas.";
            return;
        }

        if (!respuesta.ok) {
            throw new Error("Error HTTP: " + respuesta.status);
        }

        const datos = await respuesta.json();

        if (!Array.isArray(datos.notas)) {
            throw new Error("Respuesta inválida");
        }

        notasActuales = datos.notas;

        datos.notas.forEach(nota => {
            const fila = document.createElement("tr");

            function agregarCelda(valor) {
                const celda = document.createElement("td");
                celda.textContent = String(valor);
                fila.appendChild(celda);
                return celda;
            }

            agregarCelda(nota.estudiante);
            agregarCelda(nota.curso);
            agregarCelda(
                Number(nota.calificacion).toFixed(2)
            );
            agregarCelda(nota.periodo);

            const aprobado = nota.calificacion >= 11;

            const celdaEstado = agregarCelda(
                aprobado ? "Aprobado" : "Desaprobado"
            );

            celdaEstado.className = aprobado
                ? "aprobado"
                : "desaprobado";

            // Acciones disponibles para administradores
            if (document.getElementById("form-nota")) {
                const celdaAcciones = document.createElement("td");

                const editar = document.createElement("button");
                editar.type = "button";
                editar.textContent = "Editar";
                editar.className = "boton-editar";

                editar.addEventListener("click", () => {
                    editarNota(nota.id);
                });

                const eliminar = document.createElement("button");
                eliminar.type = "button";
                eliminar.textContent = "Eliminar";
                eliminar.className = "boton-eliminar";

                eliminar.addEventListener("click", () => {
                    eliminarNota(nota.id);
                });

                celdaAcciones.append(editar, eliminar);
                fila.appendChild(celdaAcciones);
            }

            tabla.appendChild(fila);
        });

        mensaje.textContent =
            `Se encontraron ${datos.notas.length} notas.`;

    } catch (error) {
        console.error(error);
        mensaje.textContent =
            "No se pudieron cargar las calificaciones.";
    }
}


// Registrar o actualizar una nota
async function guardarNota(evento) {
    evento.preventDefault();

    const formulario = document.getElementById("form-nota");
    const boton = document.getElementById("boton-guardar");
    const mensaje = document.getElementById("mensaje-formulario");
    const notaId = document.getElementById("nota-id").value;

    const datos = {
        estudiante: document.getElementById("estudiante").value,
        curso: document.getElementById("curso").value,
        calificacion: document.getElementById("calificacion").value,
        periodo: document.getElementById("periodo").value.trim()
    };

    const esEdicion = notaId !== "";

    const url = esEdicion
        ? `/api/notas/${notaId}/`
        : "/api/notas/";

    const metodo = esEdicion ? "PUT" : "POST";

    boton.disabled = true;
    mensaje.textContent = "";

    try {
        const respuesta = await fetch(url, {
            method: metodo,
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCSRF()
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                resultado.error || "No se pudo guardar la nota."
            );
        }

        cancelarEdicion();

        mensaje.textContent = resultado.mensaje;
        mensaje.className = "mensaje-exito";

        await cargarNotas();

    } catch (error) {
        mensaje.textContent = error.message;
        mensaje.className = "mensaje-error";

    } finally {
        boton.disabled = false;
    }
}


// Cargar una nota en el formulario para editarla
function editarNota(id) {
    const nota = notasActuales.find(n => n.id === id);

    if (!nota) {
        return;
    }

    document.getElementById("nota-id").value = nota.id;

    document.getElementById("estudiante").value =
        nota.estudiante_id;

    document.getElementById("curso").value =
        nota.curso_id;

    document.getElementById("calificacion").value =
        nota.calificacion;

    document.getElementById("periodo").value =
        nota.periodo;

    document.getElementById("boton-guardar").textContent =
        "Actualizar nota";

    document.getElementById("boton-cancelar").hidden = false;

    document.getElementById("mensaje-formulario").textContent = "";

    document.getElementById("form-nota").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// Cancelar la edición
function cancelarEdicion() {
    const formulario = document.getElementById("form-nota");

    if (!formulario) return;

    formulario.reset();

    document.getElementById("nota-id").value = "";

    document.getElementById("boton-guardar").textContent =
        "Guardar nota";

    document.getElementById("boton-cancelar").hidden = true;
}


// Eliminar una nota con confirmación
async function eliminarNota(id) {
    const confirmar = confirm(
        "¿Estás seguro de que deseas eliminar esta nota? " +
        "Esta acción no se puede deshacer."
    );

    if (!confirmar) {
        return;
    }

    try {
        const respuesta = await fetch(`/api/notas/${id}/`, {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": obtenerCSRF()
            }
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                resultado.error || "No se pudo eliminar."
            );
        }

        if (document.getElementById("nota-id").value === String(id)) {
            cancelarEdicion();
        }

        await cargarNotas();

        alert(resultado.mensaje);

    } catch (error) {
        alert(error.message);
    }
}
