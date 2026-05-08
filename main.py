# main.py
"""
Plantation Intelligent Monitoring System
Main Orchestrator - Ties all layers together
"""

from drone_controller import PlantationDrone
from ground_car_controller import GroundChargerCar
from safety_checker import check_drone_mission
from soil_analysis import (
    get_soil_energy_index, 
    calculate_recovery_protocol, 
    record_treatment,
    get_nutrient_ledger
)

def main():
    print("="*70)
    print("🌱 PLANTATION INTELLIGENT MONITORING SYSTEM")
    print("="*70 + "\n")

    # Initialize agents
    drone = PlantationDrone("DRONE-01")
    car = GroundChargerCar("CAR-01")

    # Test location (Change to your plantation coordinates)
    lat = 1.3521
    lon = 103.8198
    zone_id = "Zone_B"
    battery = 78

    print(f"📍 Mission Target → Zone: {zone_id} | Location: {lat:.4f}, {lon:.4f}\n")

    # ====================== 1. SAFETY LAYER ======================
    print("🔒 SAFETY LAYER (Pre-flight Check)")
    safety_code, can_proceed, safety_msg = check_drone_mission(lat, lon, battery)
    print(f"   → {safety_code} | {safety_msg}\n")

    if not can_proceed:
        print("❌ Mission aborted due to safety constraints.")
        return

    # ====================== 2. SENSING LAYER (Drone) ======================
    print("🚁 SENSING LAYER - Drone Operation")
    drone.move_to_coordinate(lat, lon)
    
    # Simulate high nutrient spike detection
    current_npk = {"N": 148, "P": 32, "K": 28}
    print(f"   Detected NPK Reading: N={current_npk['N']}, P={current_npk['P']}, K={current_npk['K']}\n")

    # ====================== 3. VERIFICATION LAYER (Ground Car) ======================
    print("🔍 VERIFICATION LAYER - Ground Car Deployed")
    audit = car.perform_camera_inspection(lat, lon, zone_id)
    print(f"   Visual Detection: {audit.get('visual_detection', 'Unknown')}\n")

    # ====================== 4. INTELLIGENCE LAYER ======================
    print("🧠 INTELLIGENCE LAYER - Recovery Protocol")
    soil_data = get_soil_energy_index(lat, lon)
    recovery = calculate_recovery_protocol(current_npk, audit.get('visual_detection', 'unknown'))

    if soil_data.get("status") == "success":
        print(f"   Soil Energy Index : {soil_data['soil_energy_index']}/100 → {soil_data['interpretation']}")

    print(f"   Priority          : {recovery['priority']}")
    print(f"   Instruction       : {recovery['instruction']}")
    print(f"   Starter Dose      : {recovery['starter_dose']}")
    print(f"   Neutralizer       : {recovery.get('neutralizer', 'None')}\n")

    # ====================== 5. EXECUTION LAYER - WORK ORDER ======================
    print("📋 MANUAL INTERVENTION WORK ORDER (MIP)")
    print("-" * 60)
    print(f"Zone ID          : {zone_id}")
    print(f"Location         : {lat:.4f}, {lon:.4f}")
    print(f"Detected Issue   : {audit.get('visual_detection', 'Unknown')}")
    print(f"Recommended Dose : {recovery['starter_dose']}")
    print(f"Action Required  : {recovery['instruction']}")
    print("-" * 60)
    print("👷 Human Specialist Tasks:")
    print("   • Perform Scattering of organic clumps")
    print("   • Apply recommended neutralizer / starter dose")
    print("   • Update system after completion")
    print("-" * 60)

    # Record treatment (after human completes the job)
    print("\n💾 Recording treatment after manual intervention...")
    print(record_treatment(zone_id, recovery['starter_dose']))

    print("\n✅ Mission Cycle Completed Successfully!")


if __name__ == "__main__":
    main()