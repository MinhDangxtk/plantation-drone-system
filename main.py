# main.py
from safety_checker import check_drone_mission
from drone_controller import PlantationDrone
from ground_car_controller import GroundChargerCar
from soil_analysis import get_soil_energy_index

def main():
    print("=== Plantation Drone + Ground Car System ===\n")
    
    drone = PlantationDrone("DRONE-01")
    ground_car = GroundChargerCar("CAR-01")
    
    lat, lon = 1.35, 103.8   # Change to your test coordinates
    battery = 88
    zone_id = "Zone A"

    # 1. Safety Check
    code, can_proceed, msg = check_drone_mission(lat, lon, battery)
    print(f"[{code}] {msg}\n")

    if not can_proceed:
        print("Mission aborted.")
        return

    # 2. Move to location
    drone.move_to_coordinate(lat, lon)

    # 3. Primary Reading
    reading = drone.take_reading(zone_id)

    # 4. Outlier Detection + Spatial Check
    if reading and reading["N"] > 80:   # Extreme outlier example
        print(f"\n⚠️ High nutrient surge detected (N={reading['N']})! Running spatial check...")
        drone.perform_spatial_check(zone_id)

        print("\n🔍 Dispatching Ground Car for visual inspection...")
        inspection = ground_car.inspect_anomaly(lat, lon, zone_id)
        print(f"Ground Car Result: Needs manual cleanup = {inspection['needs_manual_cleanup']}")

    # 5. Soil Energy Index (using last good reading)
    soil_data = get_soil_energy_index(lat, lon)
    print(f"\n🌱 Soil Energy Index: {soil_data.get('soil_energy_index', 'N/A')}/100")

    # 6. Return & Sync
    drone.return_and_sync()

    print("\n=== Mission Completed ===\n")

if __name__ == "__main__":
    main()