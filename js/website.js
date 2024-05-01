function startJourney() {
    // Redirigir a la página de carga
    window.location.href = "loadjourney.html?redirect=true";
}
function redirigir() {
    setTimeout(function() {window.location.href = "loadjourney.html?redirect=true";}, 250);
}