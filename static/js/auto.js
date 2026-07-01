document
.getElementById("startBtn")
.addEventListener("click", () => {

    fetch("/api/start-auto", {
        method: "GET"
    });
});


document
.getElementById("stopBtn")
.addEventListener("click", () => {

    fetch("/api/stop-auto", {
        method: "GET"
    });
});

document
.getElementById("startBtn_v2")
.addEventListener("click", () => {

    fetch("/api/start-auto-v2", {
        method: "GET"
    });
});


document
.getElementById("stopBtn_v2")
.addEventListener("click", () => {

    fetch("/api/stop-auto", {
        method: "GET"
    });
});


fetch("/api/plots")
.then(res => res.json())
.then(data => {

    const div = document.getElementById("plots");
    div.innerHTML = "";

    data.forEach(plot => {
        const img = document.createElement("img");
        img.src = `/api/plots/${plot}`;
        img.className = "plot";
        div.appendChild(img);
    });

});