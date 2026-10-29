# 🚀 Autonomic robot
*A rover based on Raspberry Pi and a convolutional neural network presented by Nvidia*
<br><br>
<img width="4096" height="2304" alt="Robot Bok" src="https://github.com/user-attachments/assets/4d19ef24-eb17-4a68-93d7-2c3ac38a5c51" />
<br><br>
This project was developed as a diploma thesis. It covered topics such as the construction of a rover, the implementation of manual control, and the creation of a convolutional neural network for autonomous control.
The network parameters were adjusted several times, and the impact of these changes was analyzed within the thesis.

---

## 💻 Tech Stack

* **Frontend:** HTML, CSS, JS
* **Backend:** python, flask, opencv, pygame
* **Narzędzia:** Visual Studio Code, Raspberry Pi 4B

---

## ✨ Features

* 🕹️ Manual control
* 🖥️ Autonomous control
* 📊 Data charts and statistics
* 🌐 Web interface

---

## 📸 Example of driving

* **Automatic:** [Video](https://drive.google.com/file/d/1ojI53CssZzEqKuqkNf_sni5ghOMMItK_/view?usp=sharing)
* **Off road manual driving:** [Video](https://drive.google.com/file/d/1Qsrp4eSzuT1jIFJga-0Q-j_k12xcO-Hj/view?usp=drive_link)


---

## 🛠️ How run this project?

### Prerequisites
* Rasberry Pi min ver. 4 (I run project on this version! I haven't test code on version bellow 4 and don't know if there is some modules problems)
* Python ver 3.11 wich pygame, opencv, picamera, keras and flask.
* Working XBOX or similar pad plugged to Raspberry pi

### Installation

1. Copy repository:
   ```bash
   git clone https://github.com/rph3j/autonomic_robot
   ```
2. Go to project folder:
   ```bash
   cd autonomic_robot
   ```
3. Create venv environment:
   *Important note: * picamera2 library requires installation via system package manager. Make sure you open your venv to system package!
   ```bash
   python -m venv --system-site-packages .venv
   source .venv/bin/activate
   ```

4. Install all dependencies:
   ```bash
   python -m pip install flask keras pygame opencv-python
   sudo apt install python3-picamera2
   
   ```
5. Starting WWW interface:
    ```bash
    python3 main.py
    ```
7. Starting machine learning section:<br>
   ***Important note:** make sure you check this file and comment unnesesery line!*
      ```bash
      cd Learning
      python3 learning.py  
      ```
---
## 🖥️ WWW Interface and what you can do with it!

### Manual Driving
W tej sekcji dostępny jest podgląd z kamery w czasie rzeczywistym; możesz tu również sterować robotem (sprawdź instrukcję obsługi kontrolera poniżej).
Dwa suwaki po lewej stronie służą do ustawienia stałej prędkości lub całkowitego zablokowania ruchu robota. This feature is using meanlu to better collecting learning data.
<img width="1895" height="834" alt="Manual" src="https://github.com/user-attachments/assets/c14cfcbb-5100-490a-8773-01821d131438" />

### Automatic Driving
In this section wy have view to learning charts, and buttons for two variant of models. You can change used model in autoRunMain.py file.
<img width="1808" height="652" alt="Auto" src="https://github.com/user-attachments/assets/1f469390-f48f-42eb-96f0-38ce97c01c90" />

### Machine Learning
This section wos designet to visualize learning proces but is more convenient to use your command line, like i mension before.
<img width="1882" height="632" alt="Learn" src="https://github.com/user-attachments/assets/1ee2ae19-2a24-4c1c-8cde-882655705de4" />

## 🕹️ Controller manual
* Right trigger - this trigger is usage to apply speed to engine. The further it is pressed, the greater the percentage of engine power that is applied
* Left joystick - use for detecting a percentage change and applying this change to the vehicle's steering.
* Right joystick - It is used to detect omnidirectional motion and transmit this change to the vehicle's steering system.
* B - Starting and stopping collecting data for self driving. This button collect only turn data.
* A nad X - Starting and stopping collecting data for self driving. This buttons collect data for speed and omnidirectional motios.

## 👤 Autor

* Stworzone przez: **Piotr (rph3j) Wyrwas**
* Kontakt mailowy: *1piotr.wyrwas.DEV@gmail.com*
