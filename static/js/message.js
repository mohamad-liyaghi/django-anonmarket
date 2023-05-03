const chatID = JSON.parse(document.getElementById('chat_id').textContent);
const chatCode = JSON.parse(document.getElementById('chat_code').textContent);
const userName = document.getElementById('username').textContent;


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
    
    if (data['type'] == 'chat_message'){
        const messageCard = document.createElement('div');
        messageCard.className = 'card';
        messageCard.innerHTML = `

            <div id="${data.code}">
                <div class="card-header">
                    ${data.sender} | ${data.date} | Seen: ${data.is_seen} | Edited: ${data.is_edited}
                </div>
                <div class="card-body">
                    <blockquote class="blockquote mb-0">
                        <p>${data.text}</p>
                        <hr>
                    </blockquote>
                </div>
                </div>
        `;

        if (data.sender == userName) {

            messageCard.innerHTML += `
              <footer class="blockquote-footer">
                <button id='delete_${data.code}' onclick="deleteMessage('${data.code}')">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                    <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                  </svg>
                </button>
              </footer>
            `
        };
        messageLog.insertBefore(messageCard, messageLog.firstChild);
    }

    if (data['type'] == 'message_deleted'){
        const messageDiv = document.getElementById(data.code);
        if (messageDiv) {
                const messageCard = messageDiv.parentElement;
                messageCard.parentElement.removeChild(messageCard);
            }
    }
    
    var noMsgFoundEl = document.getElementById('no-message-found');
    if (noMsgFoundEl){
        noMsgFoundEl.innerText = '';
    }
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
        'message': message,
        'type' : 'send_message',
    }));
    messageInputDom.value = '';
};

function deleteMessage(code){
    chatSocket.send(JSON.stringify({
        'code': code,
        'type' : 'delete_message',
    }));
}