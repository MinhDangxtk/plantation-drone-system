# main.py
from drone_controller import PlantationDrone
from safety_checker import check_drone_mission
from soil_analysis import get_soil_energy_index, record_treatment

def run_full_mission():
    drone = PlantationDrone("DRONE-01")
    lat, lon = 1.35, 103.8      # Change to your plantation coordinates
    battery = 88

    print("=== Plantation Drone Mission System ===\n")

    # 1. Safety Check
    safety = check_drone_mission(lat, lon, battery)
    print(f"Safety Check: {safety}")
    if "Aborted" in safety or "Halted" in safety:
        return

    # 2. Soil Analysis
    print("\nSoil Analysis:")
    soil_data = get_soil_energy_index(lat, lon)
    print(f"  Energy Index : {soil_data.get('soil_energy_index')}/100")
    print(f"  Status       : {soil_data.get('interpretation')}")
    print(f"  Recommendation: {soil_data.get('recommendation')}")

    # 3. Execute Drone Mission
    print("\nDrone Operations:")
    drone.takeoff(lat, lon)
    sample = drone.hover_and_sample()
    print(f"  Nitrogen Reading: {sample['nitrogen_ppm']} ppm")

    spatial = drone.perform_spatial_check()
    print(f"  Spatial Readings: {spatial}")

    drone.land()

    # Optional: Record nutrient treatment
    print("\nNutrient Ledger Update:")
    print(record_treatment("Zone A", 25))

if __name__ == "__main__":
    run_full_mission()