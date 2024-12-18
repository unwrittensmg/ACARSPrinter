// Open Settings Modal
function openSettingsModal() {
    document.getElementById("settings-modal").style.display = "flex";
    loadSettings(); // Load current settings into the modal fields
}

// Close Settings Modal
function closeSettingsModal() {
    document.getElementById("settings-modal").style.display = "none";
}

// Fetch and load current settings into modal fields
function loadSettings() {
    fetch("/api/settings")
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch settings.");
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("simbrief-username").value = data.simbrief_username || "";
            document.getElementById("callsign").value = data.callsign || "";
            document.getElementById("logon-code").value = data.logon_code || "";
            document.getElementById("printer-name").value = data.printer_name || "";
        })
        .catch(error => {
            console.error("Error loading settings:", error);
            alert("Failed to load settings. Please try again.");
        });
}

// Save settings and send them to the server
function saveSettings() {
    const settings = {
        simbrief_username: document.getElementById("simbrief-username").value,
        callsign: document.getElementById("callsign").value,
        logon_code: document.getElementById("logon-code").value,
        printer_name: document.getElementById("printer-name").value
    };

    fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to save settings.");
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || "Settings saved successfully!");
            closeSettingsModal();
        })
        .catch(error => {
            console.error("Error saving settings:", error);
            alert("Failed to save settings. Please try again.");
        });
}

// Close the modal when clicking outside the modal content
window.onclick = function(event) {
    const modal = document.getElementById("settings-modal");
    if (event.target === modal) {
        closeSettingsModal();
    }
};
