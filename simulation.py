import random
import numpy as np
from sklearn.neighbors import NearestNeighbors
from models import Car, Passenger, Request
import time

class CarPoolSimulation:
    def __init__(self):
        self.cars = []
        self.pending_requests = []
        self.completed_trips = 0
        self.locations = [
            "Banashankari",
            "Jayanagar",
            "BTM Layout",
            "Silk Board",
            "HSR Layout",
            "Bommanahalli",
            "Kudlu Gate",
            "Hosa Road",
            "Electronic City Phase 1",
            "Electronic City Phase 2",
            "Neeladri Road",
            "Huskur Gate",
            "Hebbagodi",
            "Bommasandra",
            "Jigani",
            "Chandapura",
            "Hennagara",
            "Anekal",
            "Marsur",
            "Jigani Cross",
            "Sarjapur",
            "Dommasandra",
            "Carmelaram",
            "Ambedkar Nagar",
            "Kodathi",
            "Mugalur",
            "Sarjapur Circle",
            "Attibele Industrial Area",
            "Attibele Bus Stop",
            "Attibele"
        ]
        
        # Distance matrix between locations (in km) - simplified with linear distances
        self.distances = {loc1: {loc2: abs(i-j)*2 for j, loc2 in enumerate(self.locations)} 
                         for i, loc1 in enumerate(self.locations)}
        
        # Animation speed
        self.animation_step = 0.1  # Movement progress per step (0.0 to 1.0)
        
        # Initialize the ML model
        self.nn_model = None
        self.demand_threshold = 2  # Minimum number of pending requests to activate another car
        
    def initialize_cars(self):
        self.cars = []
        
        # Cars from Banashankari to Attibele
        for i in range(4):
            car = Car(f"BAN-ATT-{i+1}", "Banashankari", "Attibele")
            # First car is always active, others are initially inactive
            car.active = (i == 0)
            # Add 3 passengers with random drop-offs
            for j in range(3):
                drop_idx = random.randint(1, len(self.locations)-1)
                drop_location = self.locations[drop_idx]
                passenger = Passenger(f"P-{i}-{j}", "Banashankari", drop_location)
                car.add_passenger(passenger)
            self.cars.append(car)
            
        # Cars from Attibele to Banashankari
        for i in range(4):
            car = Car(f"ATT-BAN-{i+1}", "Attibele", "Banashankari")
            # First car is always active, others are initially inactive
            car.active = (i == 0)
            # Add 3 passengers with random pick-ups
            for j in range(3):
                pickup_idx = random.randint(0, len(self.locations)-2)
                pickup_location = self.locations[pickup_idx]
                passenger = Passenger(f"P-{i+4}-{j}", pickup_location, "Banashankari")
                car.add_passenger(passenger)
            self.cars.append(car)
        
    def generate_random_request(self):
        # Generate a random pickup and dropoff location
        pickup_idx = random.randint(0, len(self.locations)-2)
        pickup_location = self.locations[pickup_idx]
        
        dropoff_idx = random.randint(pickup_idx+1, len(self.locations)-1)
        dropoff_location = self.locations[dropoff_idx]
        
        request_id = f"REQ-{int(time.time())}"
        new_request = Request(request_id, pickup_location, dropoff_location)
        self.pending_requests.append(new_request)
        
        # Try to assign this request immediately
        self.assign_requests_to_cars()
        
        # Check if we need to activate more cars
        self.adjust_active_cars()
        
        return new_request
    
    def add_custom_request(self, name, pickup_location, dropoff_location):
        """Add a custom booking request with passenger name"""
        if pickup_location not in self.locations or dropoff_location not in self.locations:
            return None
            
        request_id = f"CUSTOM-{int(time.time())}"
        new_request = Request(request_id, pickup_location, dropoff_location, name)
        self.pending_requests.append(new_request)
        
        # Try to assign this request immediately
        self.assign_requests_to_cars()
        
        # Check if we need to activate more cars
        self.adjust_active_cars()
        
        return new_request
    
    def adjust_active_cars(self):
        """Adjust the number of active cars based on demand"""
        pending_count = len(self.pending_requests)
        active_cars_banashankari = sum(1 for car in self.cars if car.active and "BAN-ATT" in car.id)
        active_cars_attibele = sum(1 for car in self.cars if car.active and "ATT-BAN" in car.id)
        
        # Calculate demand for each direction
        banashankari_to_attibele = sum(1 for req in self.pending_requests 
                                if self.locations.index(req.pickup_location) < self.locations.index(req.dropoff_location))
        attibele_to_banashankari = len(self.pending_requests) - banashankari_to_attibele
        
        # Activate more cars if needed based on demand in each direction
        if banashankari_to_attibele >= self.demand_threshold and active_cars_banashankari < 4:
            for car in self.cars:
                if "BAN-ATT" in car.id and not car.active:
                    car.active = True
                    break
                    
        if attibele_to_banashankari >= self.demand_threshold and active_cars_attibele < 4:
            for car in self.cars:
                if "ATT-BAN" in car.id and not car.active:
                    car.active = True
                    break
        
        # Deactivate cars if demand is low (but keep at least one car active in each direction)
        if banashankari_to_attibele < 1 and active_cars_banashankari > 1:
            for car in reversed(self.cars):
                if "BAN-ATT" in car.id and car.active and len(car.passengers) <= 0:
                    car.active = False
                    break
                    
        if attibele_to_banashankari < 1 and active_cars_attibele > 1:
            for car in reversed(self.cars):
                if "ATT-BAN" in car.id and car.active and len(car.passengers) <= 0:
                    car.active = False
                    break
    
    def update(self):
        # Update car positions with smooth transitions
        for car in self.cars:
            if car.active:
                # Update progress between current location and next
                if car.update_progress(self.animation_step):
                    # Progress complete, car reached next location
                    # Check if any passenger needs to be dropped off
                    passengers_to_remove = []
                    for passenger in car.passengers:
                        if passenger.dropoff_location == car.current_location:
                            passengers_to_remove.append(passenger)
                    
                    for passenger in passengers_to_remove:
                        car.remove_passenger(passenger)
                    
        # Try to assign any pending requests
        self.assign_requests_to_cars()
        
        # Adjust active cars based on demand
        self.adjust_active_cars()
        
        # Check if we need to add a car near high demand locations
        # Do this at random intervals to make it more natural (1/3 chance each update)
        import random
        if len(self.pending_requests) > 3 and random.random() < 0.3:
            new_car = self.add_car_near_demand()
            # If a new car was added, return it so the UI can show a notification
            return new_car
        
        return None
    
    def train_model(self):
        # Create feature vectors for each car (current location encoded as distance from first stop)
        X = []
        available_cars = []
        for car in self.cars:
            if car.active and car.has_space():
                location_idx = self.locations.index(car.current_location)
                direction = 1 if car.destination == "Attibele" else -1  # Direction feature
                X.append([location_idx, direction])
                available_cars.append(car)
                
        if len(X) >= 1:  # Need at least one available car
            X = np.array(X)
            self.nn_model = NearestNeighbors(n_neighbors=min(3, len(X)), algorithm='ball_tree').fit(X)
            return True, available_cars
        return False, []
    
    def assign_requests_to_cars(self):
        if not self.pending_requests:
            return
        
        success, available_cars = self.train_model()
        if not success:
            return  # No available cars
            
        requests_to_remove = []
        
        for request in self.pending_requests:
            pickup_idx = self.locations.index(request.pickup_location)
            dropoff_idx = self.locations.index(request.dropoff_location)
            direction = 1 if dropoff_idx > pickup_idx else -1
            
            # Query features: [pickup_location_idx, direction]
            query = np.array([[pickup_idx, direction]])
            
            # Find nearest cars
            distances, indices = self.nn_model.kneighbors(query)
            
            car_assigned = False
            for idx in indices[0]:
                if idx < len(available_cars):
                    candidate_car = available_cars[idx]
                    
                    # Check if the car is going in the right direction
                    car_direction = 1 if candidate_car.destination == "Attibele" else -1
                    
                    if car_direction == direction and candidate_car.has_space():
                        # Assign passenger to this car
                        passenger = Passenger(
                            f"R-{request.id}", 
                            request.pickup_location,
                            request.dropoff_location,
                            request.name  # Include the name if it exists
                        )
                        candidate_car.add_passenger(passenger)
                        requests_to_remove.append(request)
                        car_assigned = True
                        break
            
            if not car_assigned:
                # No suitable car found for this request
                # Keep it in pending requests
                pass
                
        # Remove assigned requests
        for request in requests_to_remove:
            self.pending_requests.remove(request)
    
    def get_cars_status(self):
        return [{
            "id": car.id,
            "current_location": car.current_location,
            "next_location": car.get_next_location(),
            "destination": car.destination,
            "passenger_count": len(car.passengers),
            "capacity": car.capacity,
            "active": car.active,
            "progress": car.progress,  # Animation progress
            "passengers": [
                {"id": p.id, "name": p.name, "pickup": p.pickup_location, "dropoff": p.dropoff_location}
                for p in car.passengers
            ]
        } for car in self.cars]
    
    def get_pending_requests(self):
        return [{
            "id": req.id,
            "name": req.name,
            "pickup": req.pickup_location,
            "dropoff": req.dropoff_location
        } for req in self.pending_requests]
    
    def add_car_at_location(self, location, direction):
        """
        Add a new car at a specific location with the specified direction
        direction: "to_attibele" or "to_banashankari"
        """
        if location not in self.locations:
            return None
            
        if direction == "to_attibele":
            # Find the position in the route
            car_id = f"BAN-ATT-{len([c for c in self.cars if 'BAN-ATT' in c.id]) + 1}"
            car = Car(car_id, location, "Attibele")
        else:
            car_id = f"ATT-BAN-{len([c for c in self.cars if 'ATT-BAN' in c.id]) + 1}"
            car = Car(car_id, location, "Banashankari")
            
        car.active = True
        self.cars.append(car)
        return car

    def add_car_near_demand(self):
        """Add a car automatically near locations with high demand"""
        if not self.pending_requests:
            return None  # No pending requests, no need to add cars
            
        # Group requests by pickup location
        demand_by_location = {}
        for req in self.pending_requests:
            if req.pickup_location not in demand_by_location:
                demand_by_location[req.pickup_location] = []
            demand_by_location[req.pickup_location].append(req)
        
        # Find location with highest demand
        high_demand_locations = sorted(
            demand_by_location.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )
        
        if not high_demand_locations:
            return None
        
        highest_demand_location, requests = high_demand_locations[0]
        
        # Only add a car if there are at least 2 requests in the same location
        if len(requests) < 2:
            return None
            
        # Determine direction based on majority of requests
        to_attibele_count = sum(1 for req in requests 
                             if self.locations.index(req.pickup_location) < 
                                self.locations.index(req.dropoff_location))
        to_banashankari_count = len(requests) - to_attibele_count
        
        direction = "to_attibele" if to_attibele_count >= to_banashankari_count else "to_banashankari"
        
        # Add a car at the high demand location
        car = self.add_car_at_location(highest_demand_location, direction)
        
        if car:
            print(f"Auto-added car {car.id} at {highest_demand_location} due to high demand")
            return car
        
        return None
