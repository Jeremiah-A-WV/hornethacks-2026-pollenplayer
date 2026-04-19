const BACKEND_URL = "http://localhost:8000/generate-atmosphere"

document.getElementById('geoBtn').addEventListener('click', getGeoloc);
document.getElementById('zipBtn').addEventListener('click', getZipCode);
document.getElementById('darkModeButton').addEventListener('click', toggle);

function toggle() {
    var body = document.body;
    var heading = document.h1;
    var input = document.input;
    var button = document.button;

    body.classList.toggle("darkMode");
    heading.classList.toggle("darkMode");
    input.classList.toggle("darkMode");
    button.classList.toggle("darkMode");
}

function getGeoloc() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const payload = {
                type: "coords",
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            toBackend(payload);
        })
    } else {
        alert("Geolocation is not supported.")
    }
}

function getZipCode() {
    const zipCode = document.getElementById('zipCode').value;
    if (zipCode) {
        const payload = { type: "zip", zip_code: zipCode };
        toBackend(payload);
    } else {
        alert("Please enter a zipcode.")
    }
}

async function toBackend(payload) {
    document.getElementById('atmosphereDisplay').innerText = "Analyzing . . .";

    try {
        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Backend failed");

        const data = await response.json();
        update(data);
    } catch (error) {
        console.error("Error connecting: ", error);
        alert("Could not connect to the backend.")
    }
}

function update(data) {

    const playerDiv = document.getElementById('videoContainer');
    const greetingDiv = document.getElementById('greeting');

    if (data.video_ids && data.video_ids.length > 0) {

        const firstVideo = data.video_ids[0];

        const playlistString = data.video_ids.length > 1
            ? `&playlist=${data.video_ids.slice(1).join(',')}`
            : "";

        playerDiv.innerHTML = `
            <iframe 
                width="100%" 
                height="380" 
                src="https://www.youtube.com/embed/${firstVideo}?autoplay=1${playlistString}" 
                frameborder="0" 
                allow="autoplay; encrypted-media" 
                allowfullscreen>
            </iframe>`;
        
        greetingDiv.innerHTML = null;
        document.getElementById('atmosphereDisplay').innerText = null;
    } else {
        playerDiv.innerHTML = "<p>Could not find a track for this vibe.</p>";
    }
}