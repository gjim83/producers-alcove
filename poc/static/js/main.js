function menuClick(x) {
    x.classList.toggle("change");
}

// search page easter egg
let ip = '';
let popupCount = 0;
let ARSip = '167.167.132.11';
let ARIip = '62.31.28.217';
let currentCFip = '104.28.192.51';
let easterEggOffIP = 'whatever';
function easterEgg() {
    if (ip !== ARIip) { return true; };
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
