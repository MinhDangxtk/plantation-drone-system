# MANUAL PROTOCOL (MIP)

**Manual Intervention Protocol**  
**Plantation Drone + Ground Car System**

While the PDSt (Plantation Drone Status) system handles detection, safety checks, sensor charging, and preliminary mitigation, **human expertise remains essential** for physical and biological restoration tasks.

---

## Core Human Intervention Tasks

### 1. Scattering
**Description**:  
Breaking up and evenly distributing concentrated "masses" such as clumps of dead leaves, organic debris, or fertilizer piles.

**Objective**:  
Prevent soil suffocation (anaerobic conditions), improve oxygen penetration, and ensure uniform nutrient distribution across the affected zone.

**When Required**:  
- After Ground Car confirms clumping during camera inspection  
- Following detection of extreme nutrient outliers

**Procedure**:
- Use rake or manual spreader to break apart and redistribute clumps
- Aim for even coverage without over-compacting the soil
- Document before and after condition (photos recommended)

---

### 2. Precision Re-fertilizing
**Description**:  
Applying a controlled and precise amount of specific nutrients to restore balance in the affected area.

**Objective**:  
"Reset" the soil nutrient profile based on verified clean data while avoiding secondary over-fertilization.

**When Required**:  
- After Scattering and/or Ground Car verification  
- When Soil Energy Index and nutrient ledger indicate an imbalance

**Procedure**:
- Refer to the latest report from `soil_analysis.py`
- Apply only the recommended quantity and type of nutrient
- Use targeted application methods (spot treatment preferred)
- Record the exact amount applied in the nutrient ledger

---

## General Guidelines for All Manual Tasks

- Always check the latest **PDSt code** and Ground Car inspection report before starting work.
- Wear appropriate PPE (gloves, mask, boots) especially when handling biomass or concentrated fertilizer.
- Take geo-tagged photos before and after intervention.
- Update the system (via mobile app or dashboard) after completing the task.
- Prioritize safety and ecological sensitivity — especially near buffer zones and wildlife corridors.

---

**Next Tasks to be added:**
- Biomass Removal (Animal Carcass / Heavy Debris)
- Ground Sensor Maintenance
- Final Area Verification

---

**System Philosophy**  
> *Automate what can be measured and monitored — Reserve human judgment and physical care for restoration and final quality control.*

---

**File maintained as part of the Plantation Intelligent Monitoring System**