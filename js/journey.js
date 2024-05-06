function redirigir() {
    setTimeout(function() {window.location.href = "loadwebsite.html?redirect=true";}, 250);
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
