# soil_analysis.py
import requests
from datetime import datetime
from typing import Dict, Any

# ====================== NUTRIENT LEDGER ======================
nutrient_ledger = {
    "Zone A": {"last_treated": None, "total_nitrogen": 50.0, "total_phosphorus": 40.0, "total_potassium": 45.0},
    "Zone B": {"last_treated": None, "total_nitrogen": 85.0, "total_phosphorus": 55.0, "total_potassium": 60.0},
}


def get_soil_energy_index(lat: float, lon: float) -> Dict[str, Any]:
    """Calculate Soil Energy Index (Biological Activity Proxy)"""
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

        # Soil Energy Index Calculation (0-100)
        temp_factor = max(0, min(1, (soil_temp + 5) / 40))
        moisture_factor = max(0, min(1, soil_moist / 0.35))
        energy_index = round(temp_factor * moisture_factor * 100, 1)

        return {
            "status": "success",
            "soil_temperature_0cm_c": round(soil_temp, 2),
            "soil_moisture_0_to_1cm": round(soil_moist, 4),
            "soil_energy_index": energy_index,
            "interpretation": "High 🌱" if energy_index > 65 else "Medium" if energy_index > 40 else "Low ❄️",
            "biological_activity": "Good" if energy_index > 60 else "Moderate" if energy_index > 35 else "Poor"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def calculate_recovery_protocol(current_npk: dict, detected_issue: str = "unknown") -> dict:
    """
    Intelligence Layer: Calculates recovery protocol based on NPK readings 
    and Ground Car inspection results.
    """
    n = current_npk.get('N', 0)
    p = current_npk.get('P', 0)
    k = current_npk.get('K', 0)

    protocol = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "neutralizer": None,
        "starter_dose": {"N": 0, "P": 0, "K": 0},
        "target_equilibrium": {"N": 55, "P": 45, "K": 50},
        "instruction": "",
        "priority": "Medium",
        "detected_issue": detected_issue
    }

    # === ANIMAL CORPSE / HIGH ORGANIC DECOMPOSITION ===
    if detected_issue in ["Animal_Corpse", "Organic_Debris"] or n > 120:
        protocol["neutralizer"] = "Agricultural Lime + Biotic Decomposer"
        protocol["starter_dose"] = {"N": 0, "P": 12, "K": 15}
        protocol["instruction"] = "High Nitrogen from decomposition detected. Apply neutralizer immediately. Do NOT add Nitrogen."
        protocol["priority"] = "High"

    # === HIGH PHOSPHORUS ===
    elif p > 80:
        protocol["neutralizer"] = "None (Focus on balancing)"
        protocol["starter_dose"] = {"N": 10, "P": 0, "K": 12}
        protocol["instruction"] = "High Phosphorus level. Balance with Nitrogen and Potassium."
        protocol["priority"] = "Medium"

    # === HIGH POTASSIUM ===
    elif k > 90:
        protocol["neutralizer"] = "None (Focus on balancing)"
        protocol["starter_dose"] = {"N": 12, "P": 10, "K": 0}
        protocol["instruction"] = "High Potassium detected. Balance with Nitrogen and Phosphorus."
        protocol["priority"] = "Medium"

    # === MODERATE / GENERAL IMBALANCE ===
    else:
        protocol["starter_dose"] = {"N": 8, "P": 10, "K": 10}
        protocol["instruction"] = "Moderate nutrient imbalance. Apply balanced starter dose after scattering."

    return protocol


def record_treatment(zone_id: str, applied_dose: dict) -> str:
    """Update nutrient ledger after manual or automated treatment"""
    if zone_id not in nutrient_ledger:
        return f"❌ Zone {zone_id} not found in ledger."

    nutrient_ledger[zone_id]["total_nitrogen"] += applied_dose.get("N", 0)
    nutrient_ledger[zone_id]["total_phosphorus"] += applied_dose.get("P", 0)
    nutrient_ledger[zone_id]["total_potassium"] += applied_dose.get("K", 0)
    nutrient_ledger[zone_id]["last_treated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"✅ Treatment recorded for {zone_id}. Updated totals: {nutrient_ledger[zone_id]}"


def get_nutrient_ledger():
    """Return current nutrient ledger status"""
    return nutrient_ledger