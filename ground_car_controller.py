# ground_car_controller.py
from datetime import datetime
from typing import Dict, Any, Optional

class GroundChargerCar:
    def __init__(self, car_id: str):
        self.id = car_id
        self.battery = 100.0
        self.state = "IDLE"
        self.inspection_log: Dict = {}   # Store visual inspection results

    def charge_sensor_node(self, node_id: str) -> bool:
        """Wireless charging for low-capacity ground soil sensors only"""
        if self.battery < 3.0:
            print(f"⚠️ [CAR_LOW_POWER] Ground Car {self.id} battery too low to charge sensor {node_id}")
            return False

        self.state = "CHARGING_NODE"
        print(f"⚡ [WIRELESS_CHARGING] Charging Sensor Node '{node_id}'...")
        self.battery -= 2.5
        self.state = "IDLE"

        print(f"✅ Sensor {node_id} successfully charged. Car battery: {self.battery:.1f}%")
        return True

    def inspect_anomaly(self, lat: float, lon: float, zone_id: str, suspected_issue: str = "high_nutrient_spike") -> Dict[str, Any]:
        """
        Use camera to visually inspect the area and confirm whether the outlier 
        is caused by contamination (e.g. dead animal, organic debris, etc.).
        
        Returns inspection result to help decide if manual labor is needed.
        """
        self.state = "INSPECTING"
        print(f"📷 [CAMERA_INSPECTION] Ground Car {self.id} inspecting {zone_id} at ({lat:.4f}, {lon:.4f}) for {suspected_issue}...")

        # Simulate camera-based detection (in reality: computer vision model)
        inspection_result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "GroundCar_Camera",
            "zone_id": zone_id,
            "position": (round(lat, 6), round(lon, 6)),
            "suspected_issue": suspected_issue,
            "visual_findings": "organic_debris_detected",   # or "dead_animal", "normal", "fertilizer_clump"
            "confidence": 0.87,
            "needs_manual_cleanup": True,                   # Most important output
            "recommended_action": "Dispatch manual labor to remove debris and re-sample",
            "clean_reading_suggested": True
        }

        # Log the inspection
        key = f"{lat:.5f}_{lon:.5f}"
        self.inspection_log[key] = inspection_result

        self.state = "IDLE"
        print(f"📸 [INSPECTION_COMPLETE] Visual findings: {inspection_result['visual_findings']}")
        print(f"   → Needs manual cleanup: {inspection_result['needs_manual_cleanup']}")
        
        return inspection_result

    def get_battery_level(self) -> float:
        return round(self.battery, 1)

    def get_state(self) -> str:
        return self.state