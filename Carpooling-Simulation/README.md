# Carpool System with AI Driver Assignment

This project simulates a carpool system between Madiwala and Attibele in Bangalore, using AI to assign random pickup requests to the nearest available car.

## Features

- Simulation of 8 cars (4 from Madiwala to Attibele, 4 from Attibele to Madiwala)
- Each car has 3 initial passengers with 1 empty seat
- Random pickup requests are generated and assigned to nearby drivers
- AI-based assignment using Nearest Neighbors algorithm
- Interactive web interface to visualize the simulation

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open http://127.0.0.1:5000/ in your browser

## How It Works

1. The simulation creates 8 cars with 3 passengers each
2. Cars move along predefined routes between Madiwala and Attibele
3. Random pickup requests can be added during the simulation
4. The ML model assigns requests to the nearest available car going in the correct direction
5. Passengers are picked up and dropped off at their specified locations

## AI/ML Component

The project uses scikit-learn's Nearest Neighbors algorithm to assign pickup requests to the most suitable car based on:
- Current location
- Direction of travel
- Available space

## Routes

The simulation includes the following locations along the route:
- Madiwala
- Bommanahalli
- Singasandra
- Electronic City
- Huskur Gate
- Chandapura
- Heelalige
- Attibele
