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
    document.querySelector('#message-log').value += (data.message + '\n');
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