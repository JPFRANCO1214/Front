function startJourney() {
    window.location.href = "loadjourney.html";
    window.onload = function() {
        setTimeout(function() {
            window.location.href = "journey.html";
        }, 5000); // 5000 milisegundos = 5 segundos
    };
}
