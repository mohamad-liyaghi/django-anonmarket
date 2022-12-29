
function reaction(content_type_id, object_id, vote_action, like_count, dislike_count){
        $.ajax({
        type: 'POST',
        url:  $("#Url").attr("data-url"),
        data: {
            object_id: object_id,
            content_type_id: content_type_id,
            vote_action: vote_action,
            csrfmiddlewaretoken:$("#CSRF").attr("data"),
            action: 'post'
        },
        success: function (json) {
            document.getElementById(like_count).innerHTML = json['likes']
            document.getElementById(dislike_count).innerHTML = json['dislikes']
        },
        error: function (xhr, errmsg, err) {
    
        }
        });
}
