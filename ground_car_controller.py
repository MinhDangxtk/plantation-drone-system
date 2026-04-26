# ground_car_controller.py
from datetime import datetime
from typing import Dict, Any

class GroundChargerCar:
    def __init__(self, car_id: str):
        self.id = car_id
        self.state = "IDLE"
        self.battery = 100.0
        self.current_zone = "BASE"
        self.inspection_history = {}

    def wireless_charge_sensor(self, node_id: str) -> bool:
        """Job 1: Wireless inductive charging for low-capacity ground sensors"""
        if self.battery < 5.0:
            print(f"⚠️ [PDSt_LOW_CAR_BATTERY] Ground Car {self.id} battery too low to charge sensor.")
            return False

        self.state = "CHARGING"
        print(f"⚡ [PDSt_CHARGE] Car {self.id}: Inductive charging started for Sensor Node '{node_id}'...")

        # Simulate charging cost
        self.battery -= 4.5
        self.state = "IDLE"

        print(f"✅ [PDSt_CHARGE_COMPLETE] Sensor {node_id} charged. Car battery remaining: {self.battery:.1f}%")
        return True

    def perform_camera_inspection(self, lat: float, lon: float, zone_id: str, suspected_issue: str = "high_nutrient_spike") -> Dict[str, Any]:
        """
        Job 2: High-resolution camera inspection to verify anomalies detected by drone.
        Used when PDSt11 (Biodiversity Alert) or nutrient outlier is flagged.
        """
        self.state = "AUDITING"
        print(f"📸 [PDSt_AUDIT] Ground Car {self.id} performing camera inspection at {zone_id} ({lat:.4f}, {lon:.4f})")
        print(f"   Suspected issue: {suspected_issue}")

        # Simulate realistic computer vision detection (random but weighted)
        possible_findings = [
            "Normal_Soil",
            "Organic_Debris",
            "Fertilizer_Clump",
            "Animal_Corpse",
            "Weed_Infestation"
        ]
        
        # Higher chance of finding something when called after anomaly
        if suspected_issue == "high_nutrient_spike":
            found = "Animal_Corpse" if hash(str(lat + lon)) % 3 == 0 else "Organic_Debris"
        else:
            found = possible_findings[hash(str(lat)) % len(possible_findings)]

        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "car_id": self.id,
            "zone_id": zone_id,
            "position": (round(lat, 6), round(lon, 6)),
            "suspected_issue": suspected_issue,
            "visual_detection": found,
            "confidence": round(0.75 + (0.2 * (hash(str(lat)) % 10) / 10), 2),
            "action_required": "Manual_Labor_Cleaning" if found in ["Animal_Corpse", "Organic_Debris", "Fertilizer_Clump"] else "No_Action",
            "recommendation": "Dispatch worker to remove debris and re-sample area" 
                             if found in ["Animal_Corpse", "Organic_Debris"] else "Area appears clean - proceed with normal sampling",
            "clean_data_recommended": True
        }

        # Save to history
        key = f"{lat:.5f}_{lon:.5f}"
        self.inspection_history[key] = result

        self.state = "IDLE"
        print(f"📸 [PDSt_AUDIT_COMPLETE] Detection: {found} | Action: {result['action_required']}")
        
        return result

    def get_battery_level(self) -> float:
        return round(self.battery, 1)

    def get_state(self) -> str:
        return self.state