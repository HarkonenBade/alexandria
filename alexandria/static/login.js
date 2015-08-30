$( "#token-set" ).submit(function( event ) {
    event.preventDefault();
    Cookies.set('token', $('#token').val(), {expires: 365});
    window.location.href = "/"
});
