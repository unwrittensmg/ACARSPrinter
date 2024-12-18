function fetchMessages() {
    fetch("/api/messages")
        .then(response => response.json())
        .then(messages => {
            const list = document.getElementById("message-list");
            list.innerHTML = "";
            messages.forEach(msg => {
                const li = document.createElement("li");
                li.textContent = msg;
                li.onclick = () => selectMessage(li);
                list.appendChild(li);
            });
        });
}
setInterval(fetchMessages, 5000);
fetchMessages();
