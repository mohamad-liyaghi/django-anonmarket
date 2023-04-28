function create_order(object_id, object_slug){

    var quantity = document.getElementById("id_quantity").value;
    var description = document.getElementById("id_description").value;


    $.ajax({
        type: 'POST',
        url:  $("#CREATE_ORDER_URL").attr("data-url"),
        data: {
            object_id: object_id,
            object_slug: object_slug,
            quantity: quantity,
            description: description,
            csrfmiddlewaretoken: $("#CSRF").attr("data"),
            action: 'post'
        },
        success: function (json) {
            if (json["error"]){

                var errorAlert = '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                     json['error'] +
                     '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                  '</div>';
                  $('#message').append(errorAlert);
                
            }   
            else if (json["success"]){
                var errorAlert = '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                     json['success'] +
                     '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                  '</div>';
                  $('#message').append(errorAlert);
            }
        },
    })}