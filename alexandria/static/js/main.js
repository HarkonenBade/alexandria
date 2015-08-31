$( "#logout" ).click(function( event ) {
    Cookies.remove('token');
    window.location.href = "/"
});
