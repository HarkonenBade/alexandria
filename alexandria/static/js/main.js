$( "#logout" ).click(function( event ) {
    Cookies.remove('token');
    window.location.href = "/"
});

FormModal('#add_quote', '/quote',
function(data){
    var ret = [];

    if( data.text == ""){
        ret.push("Error: Please enter quote text.");
    }
    if( data.person == ""){
        ret.push("Error: Please add a source to your quote.");
    }

    return ret;
},function(data, textStatus){
    $('.footer').prepend(`<div id="post-${data.id}" class="alert alert-success fade in text-center">
                              Post sucessfully added.
                          </div>`);
    setTimeout(function (){
        $('#post-' + data.id).alert('close');
    }, 2000);
});
