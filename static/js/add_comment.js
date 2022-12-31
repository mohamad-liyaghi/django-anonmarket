function add_comment(content_type_id, object_id){

    var comment_content = document.getElementById("id_comment");

    $.ajax({
        type: 'POST',
        url:  $("#Comment-Url").attr("data-url"),
        data: {
            object_id: object_id,
            content_type_id: content_type_id,
            content: comment_content.value,
            csrfmiddlewaretoken: $("#CSRF").attr("data"),
            action: 'post'
        },
        success: function (json) {
            if (json["limit-error"]){
                window.alert("Too many attempt, try again after 5 mins.")    
            }   
            else if (json["created"]){
                window.alert("Comment created.")    
            }
            comment_content.value = "";
            console.log(json)
            
        },
    })}