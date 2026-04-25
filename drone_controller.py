# drone_controller.py
from datetime import datetime

class PlantationDrone:
    def __init__(self, drone_id: str):
        self.id = drone_id
        self.state = "IDLE"
        self.position = (0.0, 0.0)

    def takeoff(self, target_lat: float, target_lon: float):
        print(f"🚀 Drone {self.id}: Taking off to {target_lat}, {target_lon}")
        self.position = (target_lat, target_lon)
        self.state = "TRANSIT"

    def hover_and_sample(self):
        self.state = "SAMPLING"
        print(f"🛸 Drone {self.id}: Hovering and sampling NPK sensor...")
        # Simulated sensor reading (replace with real RS485 later)
        nitrogen = round(18 + (25 * (0.3 + 0.7 * (self.position[0] % 1))), 1)
        return {"nitrogen_ppm": nitrogen, "timestamp": datetime.now().strftime("%H:%M:%S")}

    def perform_spatial_check(self):
        self.state = "VERIFYING"
        print(f"🧭 Drone {self.id}: Performing spatial verification...")
        return [21, 23, 19, 22]   # Simulated readings from 4 spots

    def land(self):
        self.state = "IDLE"
        print(f"🛬 Drone {self.id}: Landing. Mission complete.")