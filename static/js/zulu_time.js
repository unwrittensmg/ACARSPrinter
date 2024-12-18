function updateZuluTime() {
    const now = new Date();
    const zuluTime = now.toISOString().slice(11, 19) + " Z";
    document.getElementById("zulu-time").textContent = zuluTime;
}
setInterval(updateZuluTime, 1000);
updateZuluTime();
