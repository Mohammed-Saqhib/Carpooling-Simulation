class Car:
    def __init__(self, car_id, start_location, destination):
        self.id = car_id
        self.current_location = start_location
        self.destination = destination
        self.passengers = []
        self.capacity = 4
        self.route = self._get_route(start_location, destination)
        self.route_index = 0
        self.active = True  # Flag to control if car is active in the simulation
        self.progress = 0.0  # Progress between current location and next (0.0 to 1.0)
        
    def _get_route(self, start, end):
        # Define a fixed route between Banashankari and Attibele (30 stops)
        full_route = [
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
        
        if start == "Banashankari" and end == "Attibele":
            return full_route
        elif start == "Attibele" and end == "Banashankari":
            return list(reversed(full_route))
        else:
            # Handle custom routes
            start_idx = full_route.index(start) if start in full_route else 0
            end_idx = full_route.index(end) if end in full_route else -1
            
            if start_idx <= end_idx:
                return full_route[start_idx:end_idx+1]
            else:
                return list(reversed(full_route[end_idx:start_idx+1]))
        
    def add_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        return False
    
    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            return True
        return False
    
    def has_space(self):
        return len(self.passengers) < self.capacity
    
    def is_at_destination(self):
        return self.current_location == self.destination and self.route_index >= len(self.route) - 1
    
    def get_next_location(self):
        if self.route_index < len(self.route) - 1:
            return self.route[self.route_index + 1]
        else:
            # If at end of route, return first stop (for loop)
            return self.route[0]
    
    def move_to_next_location(self):
        if self.route_index < len(self.route) - 1:
            self.route_index += 1
            self.current_location = self.route[self.route_index]
            self.progress = 0.0  # Reset progress for new segment
            return True
        else:
            # We've reached the destination - reverse the route for continuous loop
            self.destination = self.route[0]  # First location in current route
            # Reset with swapped start/destination
            self.route = self._get_route(self.current_location, self.destination)
            self.route_index = 0
            self.progress = 0.0  # Reset progress
            return True
        return False

    def toggle_active(self):
        """Enable or disable the car from moving in the simulation"""
        self.active = not self.active
        return self.active
    
    def update_progress(self, step=0.05):
        """Update progress between current location and next location"""
        if self.progress < 1.0:
            self.progress += step
            if self.progress >= 1.0:
                self.progress = 0.0
                self.move_to_next_location()
                return True
        return False


class Passenger:
    def __init__(self, passenger_id, pickup_location, dropoff_location):
        self.id = passenger_id
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location


class Request:
    def __init__(self, request_id, pickup_location, dropoff_location):
        self.id = request_id
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.timestamp = None  # This can be set when the request is created
