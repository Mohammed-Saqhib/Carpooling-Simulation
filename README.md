# 🚗 Carpooling Simulation System 🚗

![Carpooling Banner](https://img.shields.io/badge/Carpooling-Simulation-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-lightblue)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)

Welcome to the **Carpooling Simulation System**! This project creates an intelligent carpooling experience by utilizing AI algorithms to optimize ride-sharing between Madiwala and Attibele in Bangalore. The system employs machine learning to match passengers with the most suitable drivers based on location, direction, and available space.

## ✨ Features

- **🤖 AI-Powered Matching**: Uses scikit-learn's Nearest Neighbors algorithm to assign pickup requests to the most suitable car
- **🚌 Real-Time Simulation**: Live simulation with real-time car movement and request processing
- **🗺️ Dynamic Routing**: Cars move along predefined routes between Madiwala and Attibele
- **👥 Capacity Management**: Each car has 4 seats with intelligent passenger assignment
- **🔄 Interactive Interface**: Web-based UI to visualize and control the simulation
- **📱 Custom Bookings**: Create named passenger requests with specific pickup and dropoff points
- **🔍 Location Awareness**: Car assignment based on proximity and direction of travel

## 🛠️ Technologies Used

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: scikit-learn (Nearest Neighbors), NumPy
- **Real-time Processing**: Threading for simulation updates
- **Data Structures**: Custom car, passenger and request models

---

## 🚗 Carpooling Simulation – Smart AI Ride Matching

Welcome to the **Carpooling Simulation**! This project is designed to showcase the future of urban mobility by leveraging advanced **AI-driven matching algorithms** and **machine learning** to optimize carpooling between Banashankari and Attibele in Bangalore.

With a focus on seamless user experience and backend intelligence, this simulation demonstrates how technology can make ride-sharing smarter, greener, and more efficient.

---

## ✨ Features

- **AI Carpool Matching:** Assigns ride requests to the most suitable car using ML-based nearest neighbor algorithms.
- **Dynamic Simulation:** Real-time car movement, passenger pick-up/drop-off, and live demand visualization.
- **Interactive Web Interface:** Modern, responsive UI with map integration and live statistics.
- **Custom & Emergency Bookings:** Users can create custom bookings or trigger emergency requests.
- **Automatic Fleet Scaling:** System auto-activates cars based on demand hotspots.
- **Traffic Visualization:** Simulated traffic overlays for realistic routing.

---

## 🗂️ Project Structure

```
.
├── app.py                   # Flask backend server
├── simulation.py            # Core simulation logic
├── models.py                # Data models for Car, Passenger, Request
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html           # Main web interface
├── static/
│   ├── styles.css           # Main styles
│   ├── css/map-styles.css   # Map-specific styles
│   └── js/map-integration.js# Map and UI logic
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/your-username/carpooling-simulation.git
cd carpooling-simulation
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the application**
```bash
python app.py
```

**4. Open your browser**
```
http://127.0.0.1:5000/
```

---

## 🛠️ Technologies Used

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript, Leaflet.js
- **Machine Learning:** scikit-learn (Nearest Neighbors)
- **Visualization:** OpenStreetMap, Leaflet

---

## 🧠 How It Works

1. **Simulation Initialization:** 8 cars (4 each direction) are created with initial passengers.
2. **Live Movement:** Cars move along a real Bangalore route, picking up and dropping off passengers.
3. **AI Matching:** New ride requests are assigned to the nearest available car going in the right direction.
4. **Demand Response:** If requests spike at a location, the system auto-adds cars to meet demand.
5. **Custom & Emergency Requests:** Users can book rides with their name or trigger urgent pickups.

---

## 🗺️ Route Map

The simulation covers these real Bangalore locations:

- Banashankari
- Jayanagar
- BTM Layout
- Silk Board
- HSR Layout
- Bommanahalli
- Kudlu Gate
- Hosa Road
- Electronic City Phase 1 & 2
- Neeladri Road
- Huskur Gate
- Hebbagodi
- Bommasandra
- Jigani
- Chandapura
- Hennagara
- Anekal
- Marsur
- Jigani Cross
- Sarjapur
- Dommasandra
- Carmelaram
- Ambedkar Nagar
- Kodathi
- Mugalur
- Sarjapur Circle
- Attibele Industrial Area
- Attibele Bus Stop
- Attibele

---

## 🤝 Contributing

We welcome contributions! To add features or fix bugs:

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push to your branch
5. Open a pull request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 📬 Contact

Questions or suggestions?  
Email: msaqhib76@gmail.com

---

## 🌐 Demo

A live demo will be available soon! Stay tuned.

---

## 🙏 Acknowledgements

Special thanks to all contributors and the open-source community.  
Powered by Python, Flask, scikit-learn, and OpenStreetMap.

---

**Enjoy smarter, greener, and faster carpooling with Carpooling Simulation! 🚗💚**
