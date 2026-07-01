function updateStatus() {

    fetch('/api/status')
        .then(res => res.json())
        .then(data => {

            document.getElementById('speed').innerText =
                data.speed;

            document.getElementById('direction').innerText =
                data.direction;

            document.getElementById('dataStatus').innerText =
                data.data;

        });
}

function loadLearningData() {

    fetch('/api/learning-data')
        .then(res => res.json())
        .then(data => {

            document.getElementById('A_IMG').innerText =
                data.rotation_img;

            document.getElementById('a_csv').innerText =
                data.rotation_csv;
            
            document.getElementById('S_IMG').innerText =
                data.speed_img;

            document.getElementById('s_csv').innerText =
                data.speed_csv;

            document.getElementById('V_IMG').innerText =
                data.vertical_img;

            document.getElementById('v_csv').innerText =
                data.vertical_csv;
        });
}

setInterval(updateStatus, 500);
loadLearningData()
setInterval(loadLearningData,120000);


document
.getElementById("restrictedSpeed")
.addEventListener("change", () => {

    fetch("/restrictedSpeed", {
        method: "GET"
    });
});

document
.getElementById("engines")
.addEventListener("change", () => {

    fetch("/enginesOff", {
        method: "GET"
    });
});