const startBtn = document.getElementById("startBtnRotation");
const startBtnSpeed = document.getElementById("startBtnSpeed");
const startBtnV = document.getElementById("startBtnVertical");
const progress = document.getElementById("progress");
const statusText = document.getElementById("statusText");
const loader = document.getElementById("loaderContainer");

startBtn.addEventListener("click", () => {

    fetch("/start-learning", {
        method: "GET"
    }).then(r => r.json()).then(data => {
         if(data.success == false){
            console.log("Przerwana v1")
            return;
         }
    });

    loader.style.display = "block";

    const interval = setInterval(() => {

        fetch("/learning-status")
        .then(r => r.json())
        .then(data => {

            progress.style.width =
                data.progress + "%";

            statusText.innerText =
                data.message;

            if(data.finished){

                clearInterval(interval);
                
                progress.style.width = "100%";
                statusText.innerText =
                    "Proces zakończony";

                loader.style.display = "none";
            }
        });

    }, 500);
});

startBtnSpeed.addEventListener("click", () => {

    fetch("/start-learning-speed", {
        method: "GET"
    }).then(r => r.json()).then(data => {
         if(data.success == false){
            console.log("Przerwana v2")
            return;
         }
    });


    loader.style.display = "block";
    
    const interval = setInterval(() => {

        fetch("/learning-status")
        .then(r => r.json())
        .then(data => {

            progress.style.width =
                data.progress + "%";

            statusText.innerText =
                data.message;

            if(data.finished){

                clearInterval(interval);
                
                progress.style.width = "100%";
                statusText.innerText =
                    "Proces zakończony";

                loader.style.display = "none";
            }
        });

    }, 500);
});

startBtnV.addEventListener("click", () => {

    fetch("/start-learning-v", {
        method: "GET"
    }).then(r => r.json()).then(data => {
         if(data.success == false){
            console.log("Przerwana v3")
            return;
         }
    });


    loader.style.display = "block";
    
    const interval = setInterval(() => {

        fetch("/learning-status")
        .then(r => r.json())
        .then(data => {

            progress.style.width =
                data.progress + "%";

            statusText.innerText =
                data.message;

            if(data.finished){

                clearInterval(interval);
                
                progress.style.width = "100%";
                statusText.innerText =
                    "Proces zakończony";

                loader.style.display = "none";
            }
        });

    }, 500);
});