# ground_car_controller.py
from datetime import datetime
from typing import Dict, Any

class GroundChargerCar:
    def __init__(self, car_id: str):
        self.id = car_id
        self.battery = 100.0
        self.state = "IDLE"
        self.inspection_log: Dict = {}

    def charge_sensor_node(self, node_id: str) -> bool:
        """Charge low-capacity ground sensors only"""
        if self.battery < 3.0:
            print(f"⚠️ [CAR_LOW_POWER] Cannot charge sensor {node_id}")
            return False

        self.state = "CHARGING_NODE"
        print(f"⚡ Charging Sensor Node '{node_id}'...")
        self.battery -= 2.5
        self.state = "IDLE"
        print(f"✅ Sensor {node_id} charged. Car battery: {self.battery:.1f}%")
        return True

    def inspect_anomaly(self, lat: float, lon: float, zone_id: str) -> Dict[str, Any]:
        """Camera inspection to confirm outliers (e.g. dead animal)"""
        self.state = "INSPECTING"
        print(f"📷 [CAMERA_INSPECTION] Ground Car inspecting {zone_id}...")

        inspection = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "zone_id": zone_id,
            "position": (lat, lon),
            "visual_findings": "organic_debris_detected",
            "needs_manual_cleanup": True,
            "recommended_action": "Manual labor: Remove debris and re-sample area",
            "confidence": 0.85
        }

        self.inspection_log[f"{lat:.5f}_{lon:.5f}"] = inspection
        self.state = "IDLE"
        return inspection