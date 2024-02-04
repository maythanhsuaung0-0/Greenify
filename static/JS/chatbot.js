class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        console.log('openButton:', this.args.openButton);
        console.log('chatBox:', this.args.chatBox);
        console.log('sendButton:', this.args.sendButton);

        this.state = false;  // chatbot is closed initially
        this.messages = [];  // store message
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        // click enter button and will run this onSendButton function too
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        // toggle the value of the 'state' property (true to false, false to true)
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input'); // extract user input
        let text1 = textField.value
        // check if user input is empty
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 } // obj for user input
        this.messages.push(msg1); // add to messages array

        // http://127.0.0.1:5000/predict -- don't need to hard code root
        fetch($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            // cross-origin resource sharing
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Greeny", message: r.answer };  // define obj for chatbot response
            this.messages.push(msg2); // add to messages array
            this.updateChatText(chatbox)
            textField.value = '' // clear input field after sending msg

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Greeny")
            // to check if it's chatbot or user + modify inner html codes
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });
        // chatbox messages container + update inner html with the generated html above
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const chatbox = new Chatbox();
    chatbox.display();
});
