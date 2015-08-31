FormModal('#add_user', '/user',
function(data){
    var ret = [];

    if( data.name == ""){
        ret.push("Error: Please specify a username.");
    }

    return ret;
},function(data, textStatus){
    $('.footer').prepend(`<div id="post-${data.id}" class="alert alert-success alert-dismissable fade in text-center">
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                  <span aria-hidden="true">&times;</span>
                                  <span class="sr-only">Close</span>
                              </button>
                              User ${data.name} sucessfully created. They can now authenticate with the token <code>${data.token}</code>
                          </div>`);
});
