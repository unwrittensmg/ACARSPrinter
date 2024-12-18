let selectedMessage = null;

function selectMessage(element) {
    // Remove 'selected' class from all messages
    document.querySelectorAll("#message-list li").forEach(li => li.classList.remove("selected"));

    // Add 'selected' class to the clicked message
    element.classList.add("selected");
    selectedMessage = element.textContent;
}

function printSelectedMessage() {
    if (!selectedMessage) {
        alert("Please select a message first!");
        return;
    }

    // Open a new window for printing
    const printWindow = window.open("", "", "width=600,height=400");
    printWindow.document.write("<html><head><title>Print Message</title></head><body>");
    printWindow.document.write(`<p>${selectedMessage}</p>`);
    printWindow.document.write("</body></html>");
    printWindow.document.close();
    printWindow.print();
}
