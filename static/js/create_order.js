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
                window.alert(json['error'])    
            }   
            else if (json["success"]){
                window.alert(json['success'])    
            }
        },
    })}