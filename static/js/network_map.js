
function mostrarDetalle(ip, nombre, tipo, desc) {
    const contenedor = document.getElementById('contenido-detalle');
    if (!contenedor) return;

    contenedor.classList.remove('fade-in-up');

    let htmlContent = '';
    if (nombre === "Disponible") {
        htmlContent = `
            <div class="alert alert-success d-flex align-items-center gap-2">
                <i class="bi bi-check-circle-fill fs-4"></i>
                <div>
                    <h6 class="alert-heading fw-bold mb-0">IP: ${ip}</h6>
                    <p class="mb-0 small">Esta dirección está libre para ser asignada.</p>
                </div>
            </div>`;
    } else {
        htmlContent = `
            <div class="card shadow-sm detail-card">
                <div class="card-body">
                    <h5 class="card-title text-danger fw-bold d-flex justify-content-between align-items-center">
                        ${ip}
                        <span class="badge bg-danger rounded-pill fs-7">OCUPADA</span>
                    </h5>
                    <h6 class="card-subtitle mb-3 text-muted">
                        Asignada a: <strong style="color: var(--dark-blue);">${nombre}</strong>
                    </h6>
                    <p class="badge bg-secondary mb-3">${tipo}</p>
                    <hr>
                    <p class="mb-1 text-muted small"><strong>Descripción:</strong></p>
                    <p class="mb-0 text-dark" style="white-space: pre-wrap;">${desc}</p>
                </div>
            </div>`;
    }

    contenedor.innerHTML = htmlContent;
    void contenedor.offsetWidth; // Forzar reflow para reiniciar animación
    contenedor.classList.add('fade-in-up');
}