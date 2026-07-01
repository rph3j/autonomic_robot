import sys
import os
from flask import Flask, Response, jsonify, render_template, send_from_directory
from Controler import JoyControl
import autoRunMain as ar
sys.path.insert(1, '/home/rph3j/Magisterka/Learning')
import learning as lr
import Camera
import threading
from time import sleep

joy = JoyControl()

app = Flask(__name__)

record_data = {
    "speed": 0,
    "direction": 'Stop',
    "dataStatus": "Brak"
}

###############################
# ------ Main routs ----------
###############################
@app.route("/")
def main():
    return render_template("main.html")

@app.route("/manual")
def manual():
    thread_control = threading.Thread(target=joy.EventListener)
    thread_control.daemon = True
    thread_control.start()
    return render_template("manual.html")

@app.route("/autonomous")
def auto():
    return render_template("autonomous.html")

@app.route("/learning")
def learning():
    return render_template("learning.html")
######################################
# ------ Manuel endpoints ----------
######################################
@app.route("/api/status")
def status():
    return jsonify(record_data)

@app.route("/enginesOff")
def enginesOff():
    joy.toggleEngine()
    return {"status": "changed"}

@app.route("/restrictedSpeed")
def restrictedSpeed():
    joy.toggleRestrictedSpeed()
    return {"status": "changed"}

@app.route("/api/learning-data")
def learning_data():
    learning_data = {
        "rotation_csv": 0,
        "rotation_img": 0,
        "speed_csv": 0,
        "speed_img": 0,
        "vertical_csv": 0,
        "vertical_img": 0,
    }
    ends = ["rotation","speed","vertical"]
    for name in ends:
        path = "/home/rph3j/Magisterka/LearningData/"+name
        for i in os.listdir(path):
            full_path = os.path.join(path, i)
            if os.path.isdir(full_path):
                for i in os.listdir(full_path):
                    learning_data[name+"_img"] += 1
            elif os.path.isfile(full_path):
                learning_data[name+"_csv"] += 1
    return jsonify(learning_data)

@app.route("/video_feed")
def video_feed():
    return Response(
        Camera.generate_frame(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

########################################
# ------ Autonomus endpoints ----------
########################################
@app.route("/api/start-auto")
def start_v1():
    ar.autoChange(True)
    thread_auto_v1 = threading.Thread(target=ar.stertAuto)
    thread_auto_v1.daemon = True
    thread_auto_v1.start()
    return {"status": "start_v1" }

@app.route("/api/start-auto-v2")
def start_v2():
    ar.autoChange(True)
    thread_auto_v2 = threading.Thread(target=ar.stertAuto_v2)
    thread_auto_v2.daemon = True
    thread_auto_v2.start()
    return {"status": "start_v2" }

@app.route("/api/stop-auto")
def stop():
    ar.autoChange(False)
    return {"status": "stop" }

@app.route("/api/plots")
def get_plots():
    files = os.listdir("/home/rph3j/Magisterka/Learning/plots")
    plots = [
        f for f in files
        if f.lower().endswith((".png"))
    ]
    return jsonify(plots)

@app.route("/api/plots/<filename>")
def plot(filename):
    return send_from_directory("/home/rph3j/Magisterka/Learning/plots", filename)

#######################################
# ------ Learning endpoints ----------
#######################################

@app.route("/start-learning")
def learning_rotation():
    if lr.progres > 0 and lr.progres < 100:
        return {"success": False}
    thread_learn = threading.Thread(target=lr.learn, args=(1,1e-5,30,450))
    thread_learn.daemon = True
    thread_learn.start()
    return {"success": True}

@app.route("/start-learning-speed")
def learning_speed():
    if lr.progres > 0 and lr.progres < 100:
        return {"success": False}
    thread_learn = threading.Thread(target=lr.learn, args=(2,1e-4,10,500))
    thread_learn.daemon = True
    thread_learn.start()
    return {"success": True}

@app.route("/start-learning-v")
def learning_v():
    if lr.progres > 0 and lr.progres < 100:
        return {"success": False}
    thread_learn = threading.Thread(target=lr.learn, args=(3,1e-4,20,300))
    thread_learn.daemon = True
    thread_learn.start()
    return {"success": True}

@app.route("/learning-status")
def learning_status():
    status = {
        "progress": lr.progres,
        "message": lr.status,
        "finished": False
    }
    if lr.progres == 100:
        status["finished"] = True
    return jsonify(status)
#############################
# ------ Flask run ----------
#############################
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    thred_flask = threading.Thread(target=run_flask)
    thred_flask.daemon = True
    thred_flask.start()

    while True:
        record_data["speed"] = joy.getSpeed()
        record_data["direction"] = joy.getDirection()
        record_data["dataStatus"] = joy.getRecord()
        sleep(1)
