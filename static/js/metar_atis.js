// Message Handler: Handles user interactions for fetching and printing METAR/ATIS data

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
                displayContent += `<strong style="font-size: 16px;">METAR:</strong><br><pre style="font-size: 16px;">${data.metar}</pre><br>`;
            } else {
                displayContent += "<strong style=\"font-size: 16px;\">METAR:</strong><br>No METAR data available.<br>";
            }

            if (data.taf) {
                const formattedTAF = data.taf.replace(/(.{50})/g, "$1\n"); // Break TAF strings every 50 characters
                displayContent += `<strong style="font-size: 16px;">TAF:</strong><br><pre style="font-size: 16px;">${formattedTAF}</pre>`;
            } else {
                displayContent += "<strong style=\"font-size: 16px;\">TAF:</strong><br>No TAF data available.";
            }

            resultBox.innerHTML = displayContent; // Use innerHTML for formatted content
        })
        .catch(error => {
            console.error("Error fetching METAR and TAF:", error);
            resultBox.textContent = `Error fetching data: ${error.message}`;
        });
}

// Fetch and display ATIS from the backend API
function fetchATIS() {
    const icaoCode = document.getElementById("atis-icao").value.trim().toUpperCase();
    const resultBox = document.getElementById("atis-result");

    if (!icaoCode) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    resultBox.textContent = `Fetching ATIS for ${icaoCode}...`;

    fetch(`/api/atis?icao=${icaoCode}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.messages && data.messages.length > 0) {
                resultBox.innerHTML = data.messages.map(msg => `<li style="font-size: 16px;">${msg}</li>`).join("");
            } else {
                resultBox.innerHTML = `<p style="font-size: 16px;">No ATIS data available for ${icaoCode}.</p>`;
            }
        })
        .catch(error => {
            console.error("Error fetching ATIS:", error);
            resultBox.innerHTML = `<p style="font-size: 16px;">Error fetching ATIS: ${error.message}</p>`;
        });
}

// Print selected METAR
function printMETAR() {
    const resultBox = document.getElementById("metar-result");
    const message = resultBox.textContent;

    if (!message || message.startsWith("Error") || message.startsWith("Fetching")) {
        alert("Please fetch and select valid METAR/TAF data before printing.");
        return;
    }

    const [metar, taf] = message.split("TAF:");

    fetch("/api/print_metar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ metar: metar.trim(), taf: taf.trim() })
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
            console.error("Error printing METAR:", error);
            alert("Failed to send the METAR to the printer.");
        });
}


// Print selected ATIS
function printATIS() {
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
            alert("Failed to send the ATIS to the printer.");
        });
}
