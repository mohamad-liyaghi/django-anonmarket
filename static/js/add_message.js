const chatID = JSON.parse(document.getElementById('chat_id').textContent);
const chatCode = JSON.parse(document.getElementById('chat_code').textContent);

// create a connection
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chats/'
    + chatID
    + '/'
    + chatCode
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageLog = document.querySelector('#message-log');
    
    const messageCard = document.createElement('div');
    messageCard.className = 'card';
    messageCard.innerHTML = `
        <div class="card-header">
            ${data.sender} | ${data.date} | Seen: ${data.is_seen} | Edited: ${data.is_edited}
        </div>
        <div class="card-body">
            <blockquote class="blockquote mb-0">
                <p>${data.text}</p>
                <hr>
            </blockquote>
        </div>
    `;
    messageLog.insertBefore(messageCard, messageLog.firstChild);
};

chatSocket.onclose = function(e) {
    var errorAlert = '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                    'Chat connection closed unexpectedly :/' +
                     '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                  '</div>';
                  $('#message').append(errorAlert);
};

document.querySelector('#message-input').focus();
        document.querySelector('#message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#message-submit').click();
            }
};

document.querySelector('#message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};