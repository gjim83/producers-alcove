function menuClick(x) {
    x.classList.toggle("change");
}

// search page easter egg
let ip = '';
let popupCount = 0;
function easterEgg() {
    if (ip !== '62.31.28.217') { return true; };
    if (popupCount < 2) {
        var popup = document.getElementById("easterEggPopup");
        popup.classList.toggle("show");
        popupCount++;
  };
}

async function getIP () {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        ip = data.ip;
    } catch (error) {
        console.error('Error fetching IP address:', error);
    }
}
