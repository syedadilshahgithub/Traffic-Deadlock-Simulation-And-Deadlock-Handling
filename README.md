# 🚦 Traffic Deadlock Simulation & Deadlock Handling (Python + Pygame)

This project demonstrates a classic **traffic intersection deadlock problem** and its **solution using deadlock avoidance techniques**, implemented with **Python and Pygame**.

It visually shows how deadlock can occur when multiple processes (cars) wait for shared resources (the intersection), and how introducing scheduling and priority rules can prevent it.

---

## 📂 Project Structure

```
├── deadlock.py              # Demonstrates deadlock occurrence
├── deadlock_handled.py      # Demonstrates deadlock avoidance using priority
├── car_red.png
├── car_blue.png
├── car_yellow.png
├── car_green.png
└── README.md
```

---

## 🔹 Features

### 🔴 Deadlock Simulation (`deadlock.py`)

* Four cars approach an intersection from four directions
* Each car blocks the next, creating a circular wait condition
* When all cars are stopped, the system detects a deadlock
* Displays **"DEADLOCK OCCURRED"** on the screen

### 🟢 Deadlock Avoidance (`deadlock_handled.py`)

* Uses a **priority-based scheduling algorithm**
* Only one car is allowed inside the intersection at a time
* Waiting cars are highlighted in **red**
* Currently moving car is highlighted in **green**
* Displays **"DEADLOCK AVOIDED"** once all cars cross safely
* Shows real-time movement status on screen

---

## 🛠 Technologies Used

* Python 3
* Pygame
* Object-Oriented Programming (OOP)
* Deadlock detection and avoidance concepts from Operating Systems

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

Make sure Python 3 is installed, then install Pygame:

```bash
pip install pygame
```

---

### 2️⃣ Prepare Image Files

Ensure the following image files are in the same directory as the Python scripts:

* `car_red.png`
* `car_blue.png`
* `car_yellow.png`
* `car_green.png`

---

### 3️⃣ Run the Simulations

#### Run Deadlock Version:

```bash
python deadlock.py
```

#### Run Deadlock Avoidance Version:

```bash
python deadlock_handled.py
```

---

## 🎯 Educational Purpose

This project is ideal for:

* Operating Systems students
* Learning **deadlock conditions** (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait)
* Understanding **deadlock detection vs. deadlock avoidance**
* Visualizing synchronization and scheduling problems in an interactive way

---

## 📌 Future Improvements

* Add traffic lights or signal timers
* Allow multiple cars per lane
* Implement more scheduling algorithms (FIFO, Round Robin, Fair Scheduling)
* Display performance metrics such as waiting time and throughput
* Add sound effects and better animations

---

## 👨‍💻 Author

Developed as a learning project to demonstrate concurrency problems and solutions in a simple traffic simulation environment.

---

## 📜 License

This project is open-source and available for educational use. You are free to modify and improve it for learning purposes.
