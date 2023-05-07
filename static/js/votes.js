var objectContentTypeId = document.getElementById("objectContentTypeId").value;


function reaction(object_id, choice, like_count, dislike_count){
        $.ajax({
        type: 'POST',
        url:  $("#Url").attr("data-url"),
        data: {
            object_id: object_id,
            content_type_id: objectContentTypeId,
            choice: choice,
            csrfmiddlewaretoken:$("#CSRF").attr("data"),
            action: 'post'
        },
        success: function (json) {
            document.getElementById('upvotes_count').innerHTML = json['upvotes']
            document.getElementById('downvotes_count').innerHTML = json['downvotes']
        },
        error: function (xhr, errmsg, err) {
    
        }
        });
}
