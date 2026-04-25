# soil_analysis.py
import requests
from datetime import datetime
from typing import Dict, Any

# Nutrient Ledger (Soil & Nutrient Management)
nutrient_ledger = {
    "Zone A": {"last_treated": None, "total_nitrogen": 50.0},
    "Zone B": {"last_treated": None, "total_nitrogen": 112.5},
}


def get_soil_energy_index(lat: float, lon: float) -> Dict[str, Any]:
    """Calculate Soil Energy Index for biological activity"""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&hourly=soil_temperature_0cm,soil_moisture_0_to_1cm"
            f"&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        hourly = data.get("hourly", {})
        soil_temp = hourly.get("soil_temperature_0cm", [None])[0]
        soil_moist = hourly.get("soil_moisture_0_to_1cm", [None])[0]

        if soil_temp is None or soil_moist is None:
            return {"status": "error", "message": "Soil data unavailable"}

        temp_factor = max(0, min(1, (soil_temp + 5) / 40))
        moisture_factor = max(0, min(1, soil_moist / 0.35))
        energy_index = round(temp_factor * moisture_factor * 100, 1)

        return {
            "status": "success",
            "soil_temperature_0cm_c": round(soil_temp, 2),
            "soil_moisture_0_to_1cm": round(soil_moist, 4),
            "soil_energy_index": energy_index,
            "interpretation": "High 🌱" if energy_index > 65 else "Medium" if energy_index > 40 else "Low ❄️",
            "recommendation": "Good for nutrient application" if energy_index > 60 else "Low biological activity - consider delaying"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def record_treatment(zone_id: str, amount: float) -> str:
    """Update nutrient ledger with safety guard"""
    if zone_id not in nutrient_ledger:
        return f"❌ Error: Zone '{zone_id}' not found."

    current = nutrient_ledger[zone_id]["total_nitrogen"]
    if current + amount > 100:
        return f"⚠️ Warning: Adding {amount} exceeds limit for {zone_id} (Current: {current})!"

    nutrient_ledger[zone_id]["total_nitrogen"] += amount
    nutrient_ledger[zone_id]["last_treated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"✅ Updated {zone_id}. New total: {nutrient_ledger[zone_id]['total_nitrogen']:.1f}"