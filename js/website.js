function startJourney() {
    window.location.href = "loadjourney.html?redirect=true";
}
function redirigir() {
    setTimeout(function() {window.location.href = "loadjourney.html?redirect=true";}, 250);
}

  var qrVisible = false;

  function showQR() {
    var qrContainer = document.getElementById("qr-container");
    if (qrVisible) {
      qrContainer.style.display = "none";
      qrVisible = false;
    } else {
      qrContainer.style.display = "block";
      qrVisible = true;
    }
  }
