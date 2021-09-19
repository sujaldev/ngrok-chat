let PAD = document.getElementsByTagName("main")[0];
let INPUT = document.getElementsByTagName("input")[0];
let ENTER = document.getElementsByTagName("button")[0];
let USERNAME = "John Doe"


function add_message(author, msg, time) {
    PAD.innerHTML += `
        <div class="message">
            <span class="message-author">${author}</span>
            <span class="message-content">
                ${msg}
                <span class="message-time">${time}</span>
            </span>
        </div>`
    PAD.scrollTop = PAD.scrollHeight;
}

function on_enter() {
    add_message(USERNAME, INPUT.value, "00:00")
    INPUT.value = ""
}

ENTER.onclick = on_enter
INPUT.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        on_enter();
    }
})

add_message("SERVER", "Welcome to ngrok chat.", "00:00")
