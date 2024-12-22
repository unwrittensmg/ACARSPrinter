let selectedMessage = null;

function selectMessage(element) {
    // Remove 'selected' class from all messages
    document.querySelectorAll(".message-item, .atis-item").forEach(li => li.classList.remove("selected"));

    // Add 'selected' class to the clicked message
    element.classList.add("selected");
    selectedMessage = element.textContent;
}

// Fetch and display METAR and TAF from the backend API
function fetchMETAR() {
    const icaoCode = document.getElementById("metar-icao").value.trim().toUpperCase();
    const resultBox = document.getElementById("metar-result");

    if (!icaoCode) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    resultBox.textContent = `Fetching data for ${icaoCode}...`;

    fetch(`/api/metar?icao=${icaoCode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            let displayContent = "";

            if (data.metar) {
                displayContent += `<strong>METAR:</strong><br><pre>${data.metar}</pre><br>`;
            } else {
                displayContent += "<strong>METAR:</strong><br>No METAR data available.<br>";
            }

            if (data.taf) {
                const formattedTAF = data.taf.replace(/(.{50})/g, "$1\n");
                displayContent += `<strong>TAF:</strong><br><pre>${formattedTAF}</pre>`;
            } else {
                displayContent += "<strong>TAF:</strong><br>No TAF data available.";
            }

            resultBox.innerHTML = displayContent;
        })
        .catch(error => {
            console.error("Error fetching METAR and TAF:", error);
            resultBox.textContent = `Error fetching data: ${error.message}`;
        });
}

// Fetch and display ATIS from the backend API
function fetchATIS() {
    const icaoCode = document.getElementById("atis-icao").value.trim().toUpperCase();
    const resultBox = document.getElementById("atis-list");

    if (!icaoCode) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    resultBox.innerHTML = `<li>Fetching ATIS for ${icaoCode}...</li>`;

    fetch(`/api/atis?icao=${icaoCode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.messages && data.messages.length > 0) {
                resultBox.innerHTML = data.messages
                    .map(msg => `<li class="atis-item">${msg}</li>`)
                    .join("");

                // Add click handler for each ATIS item
                document.querySelectorAll(".atis-item").forEach(item => {
                    item.addEventListener("click", () => {
                        document.querySelectorAll(".atis-item").forEach(el => el.classList.remove("selected"));
                        item.classList.add("selected");
                    });
                });
            } else {
                resultBox.innerHTML = `<li>No ATIS data available for ${icaoCode}.</li>`;
            }
        })
        .catch(error => {
            console.error("Error fetching ATIS:", error);
            resultBox.innerHTML = `<li>Error fetching ATIS: ${error.message}</li>`;
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
            console.error("Error printing ATIS:", error);
            alert("Failed to send ATIS to the printer.");
        });
}
