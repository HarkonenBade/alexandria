$( "#token-set" ).submit(function( event ) {
    event.preventDefault();
    Cookies.set('token', $('#token').val());
    window.location.href = "/"
});
