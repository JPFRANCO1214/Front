// Verificar si se debe redirigir a la página final
if (getURLParameter('redirect') === 'true') {
    setTimeout(function() {
        // Redirigir a la página final
        window.location.href = "journey.html";
    }, 5000); // 5000 milisegundos = 5 segundos
}

// Función para obtener parámetros de la URL
function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}