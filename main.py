# main.py
"""
Plantation Intelligent Monitoring System
Main Orchestrator
"""

from drone_controller import PlantationDrone
from ground_car_controller import GroundChargerCar
from safety_checker import check_drone_mission
from soil_analysis import (
    get_soil_energy_index, 
    calculate_recovery_protocol, 
    record_treatment
)

def main():
    print("="*75)
    print("🌱 PLANTATION INTELLIGENT MONITORING SYSTEM")
    print("="*75 + "\n")

    # Initialize agents
    drone = PlantationDrone("DRONE-01")
    car = GroundChargerCar("CAR-01")

    # Mission parameters
    lat = 1.3521
    lon = 103.8198
    zone_id = "Zone_B"
    battery = 78

    print(f"📍 Mission Target → Zone: {zone_id} | Location: {lat:.4f}, {lon:.4f}\n")

    # ====================== 1. SAFETY LAYER ======================
    print("🔒 1. SAFETY LAYER (Pre-flight Check)")
    safety_code, can_proceed, safety_msg = check_drone_mission(lat, lon, battery)
    print(f"   → {safety_code} | {safety_msg}\n")

    if not can_proceed:
        print("❌ Mission aborted due to safety constraints.")
        return

    # ====================== 2. SENSING LAYER (Drone) ======================
    print("🚁 2. SENSING LAYER - Drone Operation")
    
    # Proper flow: Move first → Then sample
    drone.move_to_coordinate(lat, lon)
    
    # Take primary reading
    primary_reading = drone.take_reading(zone_id)
    
    print(f"   Primary NPK Reading → N:{primary_reading['N']}, P:{primary_reading['P']}, K:{primary_reading['K']}\n")

    # ====================== 3. VERIFICATION LAYER (Ground Car) ======================
    print("🔍 3. VERIFICATION LAYER - Ground Car Deployed")
    audit = car.perform_camera_inspection(lat, lon, zone_id)
    print(f"   Visual Detection: {audit.get('visual_detection', 'Unknown')}\n")

    # ====================== 4. INTELLIGENCE LAYER ======================
    print("🧠 4. INTELLIGENCE LAYER - Recovery Protocol")
    soil_data = get_soil_energy_index(lat, lon)
    recovery = calculate_recovery_protocol(primary_reading, audit.get('visual_detection', 'unknown'))

    if soil_data.get("status") == "success":
        print(f"   Soil Energy Index : {soil_data['soil_energy_index']}/100 → {soil_data['interpretation']}")

    print(f"   Priority          : {recovery['priority']}")
    print(f"   Instruction       : {recovery['instruction']}")
    print(f"   Recommended Dose  : {recovery['starter_dose']}\n")

    # ====================== 5. EXECUTION LAYER - WORK ORDER ======================
    print("📋 5. MANUAL INTERVENTION WORK ORDER (MIP)")
    print("-" * 65)
    print(f"Zone ID          : {zone_id}")
    print(f"Location         : {lat:.4f}, {lon:.4f}")
    print(f"Detected         : {audit.get('visual_detection', 'Unknown')}")
    print(f"Instruction      : {recovery['instruction']}")
    print(f"Starter Dose     : {recovery['starter_dose']}")
    print("-" * 65)
    print("👷 Human Specialist Required:")
    print("   • Perform Scattering of organic clumps")
    print("   • Apply neutralizer / starter dose as instructed")
    print("   • Update system after completion")
    print("-" * 65)

    # Optional: Record treatment
    print("\n💾 Recording treatment after manual work...")
    print(record_treatment(zone_id, recovery['starter_dose']))

    print("\n✅ Full Mission Cycle Completed!\n")


if __name__ == "__main__":
    main()