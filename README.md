# 🌱 Plantation Drone System

**Intelligent Hybrid Monitoring System for Sustainable Plantations**

A modular Python system combining drones, ground support vehicles, and public APIs to enable **Precision Silviculture**, real-time soil monitoring, and ecological safety.

---

## ✨ Key Features

- PDSt (Plantation Drone Status) standardized safety code system
- Realistic drone navigation and RS485 sensor simulation
- Automatic spatial verification ("Dead Animal Filter")
- Ground Charger Car with wireless sensor charging + camera inspection
- Soil Energy Index (SEI) for biological activity assessment
- Nutrient Ledger with over-fertilization protection
- Clear separation between automation and **manual intervention**

---

## 🏗️ System Architecture

plantation-drone-system/
├── main.py                    # Mission orchestrator
├── safety_checker.py          # PDSt safety codes
├── drone_controller.py        # Drone operations
├── ground_car_controller.py   # Sensor charging + inspection
├── soil_analysis.py           # Soil Energy Index + Nutrient Ledger
├── MANUAL_PROTOCOL.md         # Human intervention procedures
└── README.md
text