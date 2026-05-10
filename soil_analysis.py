# soil_analysis.py
from datetime import datetime
from typing import Dict, Any

# Nutrient Ledger (Biological Ledger)
nutrient_ledger = {
    "Zone A": {"last_treated": None, "total_nitrogen": 50.0, "last_clean_reading": None},
    "Zone B": {"last_treated": None, "total_nitrogen": 85.0, "last_clean_reading": None},
}


def get_soil_energy_index(lat: float, lon: float) -> Dict[str, Any]:
    """
    Calculates Soil Energy Index based on soil temperature and moisture.
    Used as a biological activity indicator.
    """
    try:
        # In a real system, you would call Open-Meteo API here
        # For now, we simulate realistic values (you can replace with actual API call)
        soil_temp = 28.5 + (lat % 5)          # Simulated
        soil_moist = 0.28 + (0.05 * (lon % 3))

        temp_factor = max(0, min(1, (soil_temp + 5) / 40))
        moisture_factor = max(0, min(1, soil_moist / 0.35))
        energy_index = round(temp_factor * moisture_factor * 100, 1)

        return {
            "status": "success",
            "soil_temperature_0cm_c": round(soil_temp, 2),
            "soil_moisture_0_to_1cm": round(soil_moist, 4),
            "soil_energy_index": energy_index,
            "interpretation": "High 🌱" if energy_index > 65 else "Medium" if energy_index > 40 else "Low ❄️",
            "recommendation": "Suitable for nutrient application" if energy_index > 55 
                             else "Low biological activity - delay application"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def record_treatment(zone_id: str, amount: float, source: str = "drone") -> str:
    """Record nutrient application with safety guard"""
    if zone_id not in nutrient_ledger:
        return f"❌ Error: Zone '{zone_id}' not found in ledger."

    current = nutrient_ledger[zone_id]["total_nitrogen"]

    if current + amount > 120:   # Seasonal safety limit
        return f"⚠️ Warning: Adding {amount} would exceed nitrogen limit for {zone_id} (Current: {current})"

    nutrient_ledger[zone_id]["total_nitrogen"] += amount
    nutrient_ledger[zone_id]["last_treated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    nutrient_ledger[zone_id]["last_clean_reading"] = source

    return (f"✅ [TREATMENT_RECORDED] {zone_id} updated | "
            f"New Total N: {nutrient_ledger[zone_id]['total_nitrogen']:.1f} | "
            f"Source: {source}")


def process_clean_reading(zone_id: str, clean_npk: Dict[str, float], source: str = "ground_car"):
    """
    Process clean reading after outlier was resolved by Ground Car + Manual Labor.
    This ensures we only use reliable data for Soil Energy Index and ledger.
    """
    print(f"🧾 [CLEAN_DATA_PROCESSING] Processing verified reading for {zone_id} from {source}")

    # Record average nitrogen (you can expand this)
    avg_nitrogen = clean_npk.get("N", 0)
    result = record_treatment(zone_id, round(avg_nitrogen * 0.8, 1), source=source)  # Example conversion

    print(f"   Clean N value used: {avg_nitrogen} ppm")
    return result


def get_nutrient_status(zone_id: str) -> Dict:
    """Return current status of a zone"""
    if zone_id not in nutrient_ledger:
        return {"error": "Zone not found"}
    
    data = nutrient_ledger[zone_id]
    return {
        "zone_id": zone_id,
        "total_nitrogen": data["total_nitrogen"],
        "last_treated": data["last_treated"],
        "last_clean_reading_from": data.get("last_clean_reading", "Unknown")
    }


# For testing
if __name__ == "__main__":
    print(get_soil_energy_index(1.35, 103.8))
    print(record_treatment("Zone A", 25))
    print(get_nutrient_status("Zone A"))