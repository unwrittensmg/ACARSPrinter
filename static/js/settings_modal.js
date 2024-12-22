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

            // Auto-fetch callsign if SimBrief username is available
            if (data.simbrief_username) {
                fetch(`/api/simbrief_callsign?username=${data.simbrief_username}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error("Failed to fetch SimBrief callsign.");
                        }
                        return response.json();
                    })
                    .then(callsignData => {
                        if (callsignData.callsign) {
                            document.getElementById("callsign").value = callsignData.callsign;
                        }
                    })
                    .catch(error => {
                        console.error("Error fetching SimBrief callsign:", error);
                        alert("Failed to fetch SimBrief callsign. Please check the username.");
                    });
            }
        })
        .catch(error => {
            console.error("Error loading settings:", error);
            alert("Failed to load settings. Please try again.");
        });
}

// Save settings and send them to the server
function saveSettings() {
    const settings = {
        simbrief_username: document.getElementById("simbrief-username").value.trim(),
        callsign: document.getElementById("callsign").value.trim(),
        logon_code: document.getElementById("logon-code").value.trim(),
        printer_name: document.getElementById("printer-name").value.trim()
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

// Automatically open settings modal if triggered
function triggerSettingsModal() {
    const settingsButton = document.getElementById("open-settings-btn");
    if (settingsButton) {
        settingsButton.addEventListener("click", openSettingsModal);
    }
}

// Initialize modal and bind buttons when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    triggerSettingsModal();
    const saveButton = document.getElementById("save-settings-btn");
    if (saveButton) {
        saveButton.addEventListener("click", saveSettings);
    }
});
