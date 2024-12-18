function fetchMessages() {
    fetch("/api/messages")
        .then(response => response.json())
        .then(messages => {
            const list = document.getElementById("message-list");
            list.innerHTML = ""; // Clear the list
            messages.forEach(msg => {
                const li = document.createElement("li");
                li.textContent = msg;
                li.classList.add("message-item");
                li.onclick = () => selectMessage(li);
                list.appendChild(li);
            });
        });
}
setInterval(fetchMessages, 5000);
fetchMessages();
