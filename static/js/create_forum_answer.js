function create_forum_answer(object_id, object_slug){

    var answer_content = document.getElementById("id_answer");

    $.ajax({
        type: 'POST',
        url:  $("#Answer-Url").attr("data-url"),
        data: {
            object_id: object_id,
            object_slug: object_slug,
            content: answer_content.value,
            csrfmiddlewaretoken: $("#CSRF").attr("data"),
            action: 'post'
        },
        success: function (json) {
            if (json['created']){
                // create a new div element to hold the answer card
                var newAnswerDiv = document.createElement('div');
                newAnswerDiv.classList.add('card', 'mb-3');
        
                // set the innerHTML of the new element to the HTML code for the answer card
                newAnswerDiv.innerHTML = "<div class='card-body'><p class='card-text'><small class='text-muted'>Answered by YOU! on " + json['date'] + "</small></p><p class='card-text'>" + json['answer'] + "</p></div>";
        
                // append the new element to the top of the top answers container
                var topAnswersContainer = document.getElementById('top-answers-container');
                topAnswersContainer.insertBefore(newAnswerDiv, topAnswersContainer.firstChild);
            }
        },
    })}