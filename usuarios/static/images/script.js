document.addEventListener('DOMContentLoaded', function() {
    var inputs = document.querySelectorAll('#profileForm .form-control');
    inputs.forEach(function(input) {
        input.setAttribute('disabled', 'disabled');
    });

    // Habilitar campos cuando se hace clic en el botón "Editar perfil"
    document.getElementById('editButton').addEventListener('click', function() {
        alert("Este es un mensaje de alerta.");
        inputs.forEach(function(input) {
            input.removeAttribute('disabled');
        });
        // Ocultar el botón "Editar perfil" y mostrar el botón "Guardar cambios"
        this.style.display = 'none';
        document.getElementById('saveButton').style.display = 'inline-block';
    });
});