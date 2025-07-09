from flask import Flask, render_template, request, jsonify
from simulation import CarPoolSimulation
import threading
import time

app = Flask(__name__)

# Initialize our simulation
simulation = CarPoolSimulation()
simulation_running = False
last_auto_car_added = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    global simulation_running, last_auto_car_added
    if not simulation_running:
        simulation_running = True
        simulation.initialize_cars()
        last_auto_car_added = None  # Track last auto-added car
        
        # Start the simulation in a separate thread
        def run_sim():
            global last_auto_car_added
            while simulation_running:
                # Update might return a car if one was auto-added
                new_car = simulation.update()
                if new_car:
                    last_auto_car_added = {
                        "id": new_car.id,
                        "location": new_car.current_location,
                        "timestamp": time.time()
                    }
                time.sleep(2)  # Update every 2 seconds
        
        sim_thread = threading.Thread(target=run_sim)
        sim_thread.daemon = True
        sim_thread.start()
        
        return jsonify({"status": "Simulation started"})
    return jsonify({"status": "Simulation already running"})

@app.route('/stop_simulation', methods=['POST'])
def stop_simulation():
    global simulation_running
    simulation_running = False
    return jsonify({"status": "Simulation stopped"})

@app.route('/simulation_status', methods=['GET'])
def get_status():
    global last_auto_car_added
    cars = simulation.get_cars_status()
    requests = simulation.get_pending_requests()
    
    # Check if there's a recent auto-added car to report
    auto_added_car = None
    if last_auto_car_added and time.time() - last_auto_car_added["timestamp"] < 10:  # Within last 10 seconds
        auto_added_car = last_auto_car_added
        last_auto_car_added = None  # Reset so we only show it once
    
    return jsonify({
        "cars": cars,
        "requests": requests,
        "auto_added_car": auto_added_car
    })

@app.route('/add_random_request', methods=['POST'])
def add_random_request():
    request = simulation.generate_random_request()
    return jsonify({
        "status": "Random request added", 
        "request": {
            "id": request.id,
            "pickup": request.pickup_location,
            "dropoff": request.dropoff_location
        }
    })

@app.route('/add_car', methods=['POST'])
def add_car():
    data = request.json
    location = data.get('location')
    direction = data.get('direction')
    
    if not location or not direction:
        return jsonify({"error": "Location and direction are required"}), 400
        
    car = simulation.add_car_at_location(location, direction)
    if car:
        return jsonify({
            "status": "Car added successfully", 
            "car": {
                "id": car.id,
                "location": car.current_location,
                "destination": car.destination
            }
        })
    else:
        return jsonify({"error": "Failed to add car"}), 400

@app.route('/add_custom_request', methods=['POST'])
def add_custom_request():
    data = request.json
    name = data.get('name')
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    
    if not name or not pickup or not dropoff:
        return jsonify({"error": "Name, pickup and dropoff are required"}), 400
    
    # Limit name length for UI display purposes
    if len(name) > 15:
        name = name[:15] + "..."
    
    # Add custom request to the simulation
    custom_request = simulation.add_custom_request(name, pickup, dropoff)
    
    if custom_request:
        return jsonify({
            "status": "Custom booking added successfully", 
            "request": {
                "id": custom_request.id,
                "name": custom_request.name,
                "pickup": custom_request.pickup_location,
                "dropoff": custom_request.dropoff_location
            }
        })
    else:
        return jsonify({"error": "Failed to create booking"}), 400

if __name__ == '__main__':
    app.run(debug=True)
