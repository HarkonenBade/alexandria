
function FormModal(elm, url, validate, complete){
    function addError(text){
        $(`${elm} .modal-footer`).prepend(`<div class="alert alert-danger alert-dismissible fade in" role="alert">
                                               <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                                   <span aria-hidden="true">&times;</span>
                                                   <span class="sr-only">Close</span>
                                               </button>
                                               ${text}
                                           </div>`);
    }

    $( `${elm} form` ).submit(function( event ) {
        event.preventDefault();
        var data = $(this).serializeArray().reduce(function(obj, cur){
            obj[cur.name] = cur.value;
            return obj;
        }, {});

        var ret = validate(data);

        if(ret.length > 0){
            $.each(ret, function (idx, elm){
                addError(elm);
            });
        }else{
            $.ajax({
                url: url,
                type: "POST",
                data: JSON.stringify(data),
                contentType: "application/json"
            }).done(function( data, textStatus, jqXHR ) {
                complete(data, textStatus);
                $(elm).modal('hide');
            }).fail(function( jqXHR, textStatus, errorThrown ) {
                addError("An errror occurred when validating the form.");
            });
        }
    });

    $(elm).on('hidden.bs.modal', function (e) {
        $(`${elm} form`)[0].reset();
        $(`${elm} .modal-footer .alert`).alert('close');
    });
}
