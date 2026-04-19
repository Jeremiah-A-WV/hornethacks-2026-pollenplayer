const BACKEND_URL = "http://127.0.0.1:8000/generate-atmosphere";

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

// async function toBackend(payload) {
//     document.getElementById('atmosphereDisplay').innerText = "Analyzing . . .";

//     try {
//         const response = await fetch(BACKEND_URL, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify(payload)
//         });

//         if (!response.ok) throw new Error("Backend failed");

//         const data = await response.json();
//         update(data);
//     } catch (error) {
//         console.error("Error connecting: ", error);
//         alert("Could not connect to the backend.")
//     }
// }


async function toBackend(payload) {
    document.getElementById('atmosphereDisplay').innerText = "Analyzing . . .";

    console.log("📤 Sending payload:", payload);

    try {
        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        console.log("📡 Status:", response.status);

        const text = await response.text();   // read raw response first
        console.log("📥 Raw response:", text);

        if (!response.ok) {
            throw new Error(text);  // show REAL backend error
        }

        const data = JSON.parse(text);
        console.log("✅ Parsed data:", data);

        update(data);

    } catch (error) {
        console.error("❌ FULL ERROR:", error);
        alert("Backend error: " + error.message);
    }
}


function update(data) {

    const playerDiv = document.getElementById('videoContainer');
    const greetingDiv = document.getElementById('greeting');
    const atmosphereDisplay = document.getElementById('atmosphereDisplay');

    playerDiv.innerHTML = '';

    if (data.video_ids && data.video_ids.length > 0) {

        // const firstVideo = data.video_ids[0];

        // const playlistString = data.video_ids.length > 1
        //     ? `&playlist=${data.video_ids.slice(1).join(',')}`
        //     : "";

        // playerDiv.innerHTML = `
        //     <iframe 
        //         width="100%" 
        //         height="380" 
        //         src="https://www.youtube.com/embed/${firstVideo}?autoplay=1${playlistString}" 
        //         frameborder="0" 
        //         allow="autoplay; encrypted-media" 
        //         allowfullscreen>
        //     </iframe>`;
        
        // greetingDiv.innerHTML = null;
        // document.getElementById('atmosphereDisplay').innerText = null;
        greetingDiv.innerHTML = '';
        atmosphereDisplay.innerText = `Atmosphere: ${data.search_words}`;

        const colors = ['blue', 'green', 'pink'];

        data.video_ids.forEach((videoId, index) => {
            const color = colors[index % colors.length];
            const budSrc = `images/${color}bud.png`;
            const flowerSrc = `images/${color}flower.png`;
            const container = document.createElement('div');
            container.className = 'flower-container';
            const img = document.createElement('img');
            img.src = budSrc;
            img.className = 'flower-img';
            img.alt = `${color} flower bud`;
            const videoWrapper = document.createElement('div');
            videoWrapper.className = 'video-wrapper';
            const iframe = document.createElement('iframe');
            iframe.width = "320";
            iframe.height = "180";
            iframe.src = `https://www.youtube.com/embed/${videoId}`; 
            iframe.frameBorder = "0";
            iframe.allowFullscreen = true;

            videoWrapper.appendChild(iframe);
            container.appendChild(img);
            container.appendChild(videoWrapper);
            playerDiv.appendChild(container);

            let isOpen = false;
            img.addEventListener('click', () => {
                isOpen = !isOpen;
                
                if (isOpen) {
                    img.src = flowerSrc;
                    img.classList.add('selected');
                    videoWrapper.classList.add('open');
                } else {
                    img.src = budSrc;
                    img.classList.remove('selected');
                    videoWrapper.classList.remove('open');
                    
                    iframe.src = iframe.src; 
                }
            });
        });
    } else {
        playerDiv.innerHTML = "<p>Could not find a track for this vibe.</p>";
        atmosphereDisplay.innerText = '';
    }
}