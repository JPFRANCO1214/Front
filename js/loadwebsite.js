if (getURLParameter('redirect') === 'true') {
    setTimeout(function() {
        window.location.href = "website.html";
    }, 5000); 
}

function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}