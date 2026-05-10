# main.py
from safety_checker import check_drone_mission
from drone_controller import PlantationDrone
from ground_car_controller import GroundChargerCar
from soil_analysis import get_soil_energy_index, process_clean_reading, record_treatment, get_nutrient_status

def main():
    print("=" * 60)
    print("🌿 PLANTATION DRONE + GROUND CAR SYSTEM")
    print("=" * 60)

    # Initialize systems
    drone = PlantationDrone("DRONE-01")
    ground_car = GroundChargerCar("CAR-01")

    # Test coordinates (change as needed)
    lat, lon = 1.3521, 103.8198
    battery = 88
    zone_id = "Zone A"

    print(f"\n📍 Mission Target: {zone_id} ({lat}, {lon})\n")

    # 1. Safety Check (PDSt Codes)
    code, can_proceed, msg = check_drone_mission(lat, lon, battery)
    print(f"[{code}] {msg}")

    if not can_proceed:
        print("❌ Mission aborted due to safety constraints.")
        return

    # 2. Drone Movement
    print("\n" + "-"*40)
    drone.move_to_coordinate(lat, lon)

    # 3. Primary Reading
    print("\n" + "-"*40)
    primary_reading = drone.take_reading(zone_id)

    # 4. Outlier Detection + Spatial Check
    print("\n" + "-"*40)
    if primary_reading and primary_reading["N"] > 70:   # Threshold for extreme outlier
        print(f"⚠️ HIGH NUTRIENT SURGE DETECTED (N = {primary_reading['N']})")
        print("Initiating Spatial Verification...")

        drone.perform_spatial_check(zone_id, samples=3)

        # Dispatch Ground Car for visual inspection
        print("\n📡 Dispatching Ground Car for camera inspection...")
        inspection = ground_car.inspect_anomaly(lat, lon, zone_id)

        if inspection["needs_manual_cleanup"]:
            print("\n👷 MANUAL LABOR REQUIRED:")
            print(f"   Action: {inspection['recommended_action']}")
            print("   → After cleanup, take clean reading.")

            # Simulate clean reading after manual labor
            clean_reading = {"N": 21.5, "P": 14.8, "K": 42.0}
            process_clean_reading(zone_id, clean_reading, source="ground_car + manual")

    else:
        print("✅ Reading within normal range.")

    # 5. Soil Energy Index
    print("\n" + "-"*40)
    print("🌱 Calculating Soil Energy Index...")
    sei_data = get_soil_energy_index(lat, lon)
    print(f"Soil Energy Index : {sei_data.get('soil_energy_index')}/100")
    print(f"Interpretation    : {sei_data.get('interpretation')}")
    print(f"Recommendation    : {sei_data.get('recommendation')}")

    # 6. Return & Sync + Nutrient Ledger
    print("\n" + "-"*40)
    drone.return_and_sync()

    print("\n📊 Final Nutrient Ledger Status:")
    print(get_nutrient_status(zone_id))

    print("\n" + "="*60)
    print("✅ MISSION COMPLETED SUCCESSFULLY")
    print("="*60)


if __name__ == "__main__":
    main()