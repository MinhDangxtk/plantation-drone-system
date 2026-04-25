# safety_checker.py
import requests
from typing import Tuple

def check_drone_mission(lat: float, lon: float, battery: int) -> Tuple[str, bool, str]:
    """
    Standardized Safety Checker for Plantation Drone Missions
    
    Returns: (PDSt_code, can_proceed: bool, human_readable_message)
    
    PDSt Code Mapping (Plantation Drone Status):
    PDSt01 = All Clear → Proceed with mission
    PDSt05 = Low Battery → Abort mission
    PDSt07 = Moderate Wind → Adaptive Mode (Proceed with caution)
    PDSt09 = High Wind → Abort mission
    PDSt11 = Biodiversity Alert → Manual ecological review required
    PDSt99 = System / API Error → Abort
    """

    # 1. Mechanical Guard - Battery Check
    if battery < 25:
        return ("PDSt05", False, "Critical: Low Battery - Mission Aborted")

    try:
        # 2. Weather Guard (Open-Meteo API)
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url, timeout=10).json()
        wind_speed = weather_data['current_weather']['windspeed']

        if wind_speed > 20:
            return ("PDSt09", False, f"High Wind ({wind_speed:.1f} km/h) - Mission Aborted")
        elif 15 <= wind_speed <= 20:
            return ("PDSt07", True, f"Moderate Wind ({wind_speed:.1f} km/h) - Adaptive Mission Mode")

    except Exception as e:
        return ("PDSt99", False, f"Weather API Error: {str(e)}")

    try:
        # 3. Biodiversity Guard (Restoration Ecology)
        gbif_url = (
            f"https://api.gbif.org/v1/occurrence/search"
            f"?decimalLatitude={lat}&decimalLongitude={lon}"
            f"&radius=2000&year=2023,2026&hasCoordinate=true&limit=0"
        )
        gbif_data = requests.get(gbif_url, timeout=12).json()
        count = gbif_data.get('count', 0)

        if count > 8:
            return ("PDSt11", False, f"Biodiversity Alert ({count} recent records nearby) - Manual review required for buffer zones / corridors")

    except Exception:
        pass  # Biodiversity check failure is non-critical

    # Default: All Clear
    return ("PDSt01", True, "All Systems Clear - Mission Approved")


# Quick test when running this file directly
if __name__ == "__main__":
    code, can_proceed, message = check_drone_mission(lat=1.35, lon=103.8, battery=88)
    print(f"PDSt Code   : {code}")
    print(f"Can Proceed : {can_proceed}")
    print(f"Message     : {message}")