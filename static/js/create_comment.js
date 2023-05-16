var objectContentTypeId = document.getElementById("objectContentTypeId").value;
var parentCommentID = document.getElementById("parentCommentID").getAttribute("data-url");


function add_comment(object_id){

    var comment_content = document.getElementById("id_comment");

    $.ajax({
        type: 'POST',
        url:  $("#Comment-Url").attr("data-url"),
        data: {
            object_id: object_id,
            content_type_id: objectContentTypeId,
            body: comment_content.value,
            parent_id: parentCommentID,
            csrfmiddlewaretoken: $("#CSRF").attr("data"),
            action: 'post'
        },
        success: function (json) {
            if (json["created"]){
                var comment_list = document.getElementById("comment-list");
                var new_comment = `
                    <li class="media my-4">
                        <div class="media-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h5 class="mt-0 comment-user">${json.created.user}</h5>
                                    <p class="comment-date">${json.created.date}</p>
                                </div>
                            </div>
                            <p class="mb-0">${json.created.body}</p>
                        </div>
                    </li>`;
                comment_list.insertAdjacentHTML('afterbegin', new_comment);
            }
            comment_content.value = "";
            
        },
    })
}