# 🚗 Carpooling Simulation 🚗

Welcome to the **Carpooling Simulation**! This project aims to revolutionize the carpooling experience by utilizing cutting-edge **matching algorithms** and **machine learning models** to create smarter, more efficient, and environmentally friendly ride-sharing solutions.  
With a strong focus on user experience and backend optimization, this system offers a seamless interface for carpool users while ensuring optimal route matching and predictions.

---

## 🔥 Features

- **Carpool Matching Algorithm**: An intelligent matching algorithm that connects users based on their travel routes and preferences, optimizing carpooling efficiency.
- **Machine Learning Integration**: Powerful ML models that enhance carpool prediction accuracy, ensuring that the most optimal routes and ride-sharing opportunities are provided.
- **Web Interface**: A responsive and user-friendly interface built with *Flask* for Python backend.
- **Simulation Environment**: Test out different carpooling scenarios with the simulation scripts to optimize and assess the performance of carpooling solutions in various conditions.
- **Real-time Updates**: Live simulation with real-time car movement and request processing.
- **AI-based Assignment**: Uses scikit-learn's Nearest Neighbors algorithm for optimal car-passenger matching.

---

## 🌍 Project Structure

The repository is structured for easy navigation and scalability:

```
.
├── app.py                # Main Flask application file
├── simulation.py         # Carpooling simulation script
├── README.md             # Project documentation (this file)
├── requirements.txt      # Python dependencies
├── static                # Static files (images, stylesheets, etc.)
├── templates             # HTML templates for the frontend
└── __pycache__           # Compiled Python files
```

---

## 📦 Installation

To set up the **Carpool Project (Phase 3)** on your local machine:

1. **Clone the repository**  
   `git clone https://github.com/your-username/carpool-project-phase-3.git`  
   `cd "Inhance carpool-project (phase 3)"`

2. **Install Python dependencies**  
   `pip install -r requirements.txt`

3. **Run the application**

   - Start the **Flask** server:  
     `python app.py`

4. **Access the app**  
   Visit the app in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🛠️ Technologies Used

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Python (scikit-learn, NumPy)
- **Real-time Processing**: Threading for simulation updates

---

## 🚀 How It Works

1. The simulation creates 8 cars with 3 passengers each
2. Cars move along predefined routes between Madiwala and Attibele
3. Random pickup requests can be added during the simulation
4. The ML model assigns requests to the nearest available car going in the correct direction
5. Passengers are picked up and dropped off at their specified locations

## 🎯 AI/ML Component

The project uses scikit-learn's Nearest Neighbors algorithm to assign pickup requests to the most suitable car based on:
- Current location
- Direction of travel
- Available space

## 🗺️ Routes

The simulation includes the following locations along the route:
- Madiwala
- Bommanahalli
- Singasandra
- Electronic City
- Huskur Gate
- Chandapura
- Heelalige
- Attibele

---

## 🤝 Contributing

We welcome contributions from the community! Feel free to fork the repository, create your own branch, and submit pull requests with bug fixes, new features, or enhancements.

How to contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Submit a pull request.

---

## 📝 License

This project is licensed under the **MIT License**. See the LICENSE file for more details.

---

## 📬 Contact

For any questions or inquiries, feel free to reach out to us at:  
msaqhib76@gmail.com

---

## 📊 Demo

Check out the live demo of the project in action:  
[Live Demo](https://your-demo-link.com)

---

## 👥 Acknowledgements

We would like to thank the contributors and community members for their invaluable input into this project. Special thanks to the open-source libraries and tools that made this project possible.

---

Enjoy carpooling smarter, greener, and faster with Carpooling Simulation! 🚗💚
