# drone_controller.py
from datetime import datetime
from typing import List, Dict, Any

class PlantationDrone:
    def __init__(self, drone_id: str):
        self.id = drone_id
        self.state = "IDLE"
        self.position = (0.0, 0.0)
        self.battery = 100.0
        self.data_buffer: List[Dict] = []

    def move_to_coordinate(self, target_lat: float, target_lon: float):
        """Improved realistic movement with progress simulation"""
        print(f"🚁 Drone {self.id}: Navigating to ({target_lat:.4f}, {target_lon:.4f})")
        
        self.state = "TRANSIT"
        start_pos = self.position
        
        # Simulate movement progress
        steps = 6
        for i in range(1, steps + 1):
            progress = i / steps
            curr_lat = start_pos[0] + (target_lat - start_pos[0]) * progress
            curr_lon = start_pos[1] + (target_lon - start_pos[1]) * progress
            self.position = (round(curr_lat, 6), round(curr_lon, 6))
            
            print(f"   → Moving... {int(progress*100)}% | Pos: ({self.position[0]:.4f}, {self.position[1]:.4f})")
        
        print(f"✅ Drone {self.id}: Arrived at target location.")
        self.state = "ARRIVED"
        return True

    def take_reading(self, zone_id: str, is_verification: bool = False) -> Dict[str, Any] | None:
        """RS485 Sensor reading with Sensor Guard"""
        self.state = "SAMPLING"
        try:
            base_n = 22 if is_verification else 20
            reading = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "drone_id": self.id,
                "zone_id": zone_id,
                "position": self.position,
                "N": round(base_n + (5 * (hash(str(self.position)) % 10) / 10), 1),
                "P": round(14 + (6 * (hash(str(self.position[1])) % 10) / 10), 1),
                "K": round(42 + (8 * (hash(str(self.position)) % 10) / 10), 1),
                "is_verification": is_verification,
                "sensor_status": "OK"
            }

            self.data_buffer.append(reading)
            status = "VERIFICATION" if is_verification else "PRIMARY"
            print(f"🧪 [SENSOR OK] {status} reading for {zone_id} | N:{reading['N']} P:{reading['P']} K:{reading['K']}")
            return reading

        except Exception as e:
            print(f"❌ [SENSOR_GUARD] RS485 failed at {zone_id}: {e}")
            return None

    def perform_spatial_check(self, zone_id: str, samples: int = 3):
        """Spatial Logic - Multi-sample verification"""
        self.state = "VERIFYING"
        print(f"🧭 [SPATIAL CHECK] Performing multi-sample verification at {zone_id}")
        readings = []
        
        for i in range(samples):
            offset_lat = self.position[0] + (0.00002 * (i - 1))
            offset_lon = self.position[1] + (0.00002 * (i % 2))
            self.position = (offset_lat, offset_lon)
            
            reading = self.take_reading(zone_id, is_verification=True)
            if reading:
                readings.append(reading)

        print(f"✅ Spatial check completed ({len(readings)} samples)")
        return readings

    def return_and_sync(self) -> List[Dict]:
        self.state = "RETURN"
        print(f"🏠 Drone {self.id}: Returning to base for data sync...")
        
        if not self.data_buffer:
            print("⚠️ No data in buffer.")
            return []
        
        data = self.data_buffer.copy()
        self.data_buffer.clear()
        print(f"📤 Synced {len(data)} readings.")
        self.state = "IDLE"
        return data