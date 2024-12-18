// Fetch METAR Data
function fetchMETAR() {
    const icao = document.getElementById("metar-icao").value.trim().toUpperCase();
    const resultBox = document.getElementById("metar-result");

    if (!icao) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    resultBox.textContent = `Fetching METAR for ${icao}...`;

    fetch(`/api/metar?icao=${icao}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.metar) {
                resultBox.textContent = data.metar;
            } else {
                resultBox.textContent = `No METAR data available for ${icao}.`;
            }
        })
        .catch(error => {
            console.error("Error fetching METAR:", error);
            resultBox.textContent = `Error fetching METAR: ${error.message}`;
        });
}

// Fetch ATIS Data
function fetchATIS() {
    const icao = document.getElementById("atis-icao").value.trim().toUpperCase();
    const atisList = document.getElementById("atis-list");

    if (!icao) {
        alert("Please enter a valid ICAO code.");
        return;
    }

    atisList.innerHTML = `<li>Fetching ATIS for ${icao}...</li>`;

    fetch(`/api/atis?icao=${icao}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            atisList.innerHTML = ""; // Clear the list
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(msg => {
                    const listItem = document.createElement("li");
                    listItem.textContent = msg;
                    listItem.classList.add("atis-item");
                    listItem.onclick = selectATIS; // Add selection functionality
                    atisList.appendChild(listItem);
                });
            } else {
                atisList.innerHTML = `<li>No ATIS data available for ${icao}.</li>`;
            }
        })
        .catch(error => {
            console.error("Error fetching ATIS:", error);
            atisList.innerHTML = `<li>${error.message}</li>`;
        });
}

// Highlight Selected ATIS Message
function selectATIS(event) {
    // Remove "selected" class from all ATIS items
    document.querySelectorAll(".atis-item").forEach(item => item.classList.remove("selected"));
    // Add "selected" class to the clicked item
    event.target.classList.add("selected");
}

// Print Selected ATIS Message
function printSelectedATIS() {
    const selected = document.querySelector(".atis-item.selected");
    if (!selected) {
        alert("Please select an ATIS message to print.");
        return;
    }

    fetch("/api/print", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script: "print_atis.py", content: selected.textContent })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "ATIS printed successfully!");
        })
        .catch(error => {
            console.error("Error printing ATIS:", error);
            alert("Failed to print ATIS. Please try again.");
        });
}

// Print METAR Data
function printMETAR() {
    const icao = document.getElementById("metar-icao").value;
    const result = document.getElementById("metar-result").textContent;

    if (!icao || !result.trim()) {
        alert("Please fetch a METAR before printing.");
        return;
    }

    fetch("/api/print", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script: "print_metar.py", content: `ICAO: ${icao}, ${result}` })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "METAR printed successfully!");
        })
        .catch(error => {
            console.error("Error printing METAR:", error);
            alert("Failed to print METAR. Please try again.");
        });
}
