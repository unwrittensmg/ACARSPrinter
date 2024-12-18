let selectedMessage = null;

function selectMessage(element) {
    // Remove 'selected' class from all messages
    document.querySelectorAll(".message-item, .atis-item").forEach(li => li.classList.remove("selected"));

    // Add 'selected' class to the clicked message
    element.classList.add("selected");
    selectedMessage = element.textContent;
}

// Print selected message
function printSelectedMessage() {
    if (!selectedMessage) {
        alert("Please select a message first!");
        return;
    }

    fetch("/api/print_cpdlc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: selectedMessage })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            alert(data.message);
            console.log("Message sent to printer successfully.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to send the message to the printer.");
    });
}

// Fetch and display METAR from OpenWeatherMap
function fetchMETAR() {
    const icaoCode = document.getElementById("metar-icao").value;
    if (!icaoCode) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    fetch(`/api/metar?icao=${icaoCode}`)
        .then(response => response.json())
        .then(data => {
            if (data.metar) {
                document.getElementById("metar-result").textContent = data.metar;
            } else {
                document.getElementById("metar-result").textContent = "Error fetching METAR: " + (data.error || "Unknown error");
            }
        })
        .catch(error => {
            console.error("Error fetching METAR:", error);
            document.getElementById("metar-result").textContent = "Error fetching METAR: " + error.message;
        });
}

// Fetch and display ATIS
function fetchATIS() {
    const icaoCode = document.getElementById("atis-icao").value;
    if (!icaoCode) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    fetch(`/api/atis?icao=${icaoCode}`)
        .then(response => response.json())
        .then(data => {
            const atisList = document.getElementById("atis-list");
            atisList.innerHTML = "";  // Clear existing ATIS messages

            if (data.messages) {
                data.messages.forEach(msg => {
                    const li = document.createElement("li");
                    li.classList.add("atis-item");
                    li.textContent = msg;
                    li.onclick = () => selectMessage(li);  // Add click event for selecting ATIS messages
                    atisList.appendChild(li);
                });
            } else {
                atisList.textContent = "Error fetching ATIS: " + (data.error || "Unknown error");
            }
        })
        .catch(error => {
            console.error("Error fetching ATIS:", error);
            document.getElementById("atis-list").textContent = "Error fetching ATIS: " + error.message;
        });
}

// Print selected ATIS
function printSelectedATIS() {
    const selectedATIS = document.querySelector(".atis-item.selected");
    if (!selectedATIS) {
        alert("Please select an ATIS message first!");
        return;
    }

    fetch("/api/print_atis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: selectedATIS.textContent })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to send ATIS to printer.");
    });
}
