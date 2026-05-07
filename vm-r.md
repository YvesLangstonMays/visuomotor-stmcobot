# Visuomotor

## An STM32 Cobot (Yahboom DOFBOT-SE) Bridge

**GitHub Repository:** `visuomotor`  
**Author:** Yves-Langston Mays  
**Hardware:** Yahboom DOFBOT-SE + STM32 Nucleo F446RE

---

## Project Overview

Visuomotor is a three-layer computer vision guided robotic arm control system. A PC-side Python CV pipeline processes camera input, sends high-level commands to an STM32 F446RE middleware layer, which translates and relays motion commands to the Yahboom DOFBOT-SE's onboard STM32 servo controller.

The name reflects the neuroscience and robotics term for the system that translates visual input into motor output — exactly what this project does, and exactly what a brain machine interface does at a neural level.

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│              PC LAYER (Python)              │
│                                             │
│  USB Camera → CV Pipeline → Command Output  │
│  - Object/target detection (OpenCV)         │
│  - Coordinate calculation                   │
│  - Path planning                            │
│  - Serial command dispatch                  │
└─────────────────┬───────────────────────────┘
                  │ Serial / USB
                  ▼
┌─────────────────────────────────────────────┐
│         STM32 F446RE LAYER (C++)            │
│                                             │
│  Custom Driver — Motion Translation Layer   │
│  - Receives commands from PC over serial    │
│  - Translates to DOFBOT-SE servo protocol   │
│  - Relays motion commands to arm board      │
└─────────────────┬───────────────────────────┘
                  │ UART / Serial Bus
                  ▼
┌─────────────────────────────────────────────┐
│       DOFBOT-SE STM32 LAYER (Firmware)      │
│                                             │
│  Onboard Servo Controller                   │
│  - Receives motion commands                 │
│  - Drives 6x serial bus servos              │
│  - Executes arm movements                   │
└─────────────────────────────────────────────┘
```

### Why This Architecture

The intelligence lives at the top. The determinism lives at the bottom. The F446RE is the translation layer between them. This mirrors the exact architecture used in industrial cobot automation systems and neural interface devices — a smart PC-side brain talking to precise embedded controllers.

---

## Hardware Stack

| Component                        | Role                                | Cost  |
| -------------------------------- | ----------------------------------- | ----- |
| Yahboom DOFBOT-SE Superior       | 6DOF robotic arm + servo controller | $329  |
| STM32 Nucleo F446RE              | Middleware / custom driver layer    | Owned |
| USB Camera (1080p min)           | Computer vision input               | ~$70  |
| Logitech C920/C922 (recommended) | High resolution, OpenCV compatible  | ~$70  |

**Note on camera:** The included 0.3MP DOFBOT-SE camera is insufficient for wire detection. Upgrade to at least 1080p for Phase 3+. Intel RealSense D435 (~$200) adds depth sensing for Phase 4.

---

## Development Roadmap

### Phase 1 — Whiteboard Writer

**Goal:** Understand arm kinematics. Write a Python layer that plans Cartesian paths and draws letters on a whiteboard.

**What you build:**

- Establish PC → F446RE serial communication
- Write F446RE C++ driver that speaks DOFBOT-SE servo protocol
- Implement inverse kinematics — translate XYZ coordinates to joint angles
- Python path planner that generates letter strokes as coordinate sequences
- Arm executes strokes on whiteboard

**What you learn:**

- Inverse kinematics from first principles
- Custom embedded communication protocol implementation
- Serial bus servo control (half-duplex TTL)
- The same motion planning concepts JRC uses on their industrial cobot

**Milestone:** Arm writes your name on a whiteboard autonomously.

---

### Phase 2 — Write Your Own STM32 Driver

**Goal:** Bypass the stock DOFBOT-SE firmware. Write a complete C++ driver on the F446RE that directly controls the serial bus servos.

**What you build:**

- Reverse engineer or document the DOFBOT-SE servo communication protocol
- Sniff serial traffic with a logic analyzer to understand the packet structure
- Implement full C++ driver: position commands, velocity control, torque feedback
- Replace the stock control pipeline with your own

**What you learn:**

- Protocol reverse engineering
- Half-duplex serial communication in C++
- Hardware-level servo control
- The same process JRC used to write their cobot driver

**Why this matters for your resume:**  
"Wrote a custom C++ driver for a 6DOF serial bus servo robotic arm" is a direct parallel to JRC's work and a legitimate embedded systems credential.

**Milestone:** Arm operates entirely under your custom firmware with no reliance on Yahboom's stock control stack.

---

### Phase 3 — CV Guided Component Placement

**Goal:** Add computer vision. Camera detects objects on a surface. Arm picks and places them autonomously.

**What you build:**

- Integrate USB camera into Python CV pipeline
- OpenCV object detection — color detection, contour finding, or YOLO for object classes
- Camera-to-arm coordinate calibration (extrinsic calibration)
- Closed-loop pick-and-place: detect → calculate → command → execute → verify

**What you learn:**

- Camera calibration and coordinate transforms
- Real-time CV pipeline architecture
- Closed-loop robotic control
- The same CV-to-motion pipeline JRC is building for panel wiring

**Milestone:** Arm autonomously sorts colored blocks by type.

---

### Phase 4 — Wire Routing (Portfolio Centerpiece)

**Goal:** Detect wire endpoints with CV. Plan a path between them. Execute with the arm. This is the direct analog of JRC's cobot panel wiring automation.

**What you build:**

- High resolution camera setup optimized for wire detection
- CV model that detects wire endpoints, terminals, and connector positions
- Path planning from wire start to endpoint avoiding obstacles
- Arm execution with precision grip and placement
- Verification pass — CV confirms wire is correctly placed

**What you learn:**

- Fine-grained object detection for small targets
- Constrained path planning in 3D space
- Precision manipulation under vision guidance
- Production-grade CV pipeline design

**Why this is the most important project:**  
A working wire routing system in your GitHub repository is a demonstration of exactly what JRC is trying to build at industrial scale. It is also a direct proof of concept for surgical robotics and brain machine interface probe placement — the same spatial precision problem Neuralink solves.

**Milestone:** Arm autonomously routes a wire between two terminals on a practice board.

---

## Technology Stack

### PC Layer (Python)

- `opencv-python` — computer vision pipeline
- `pyserial` — serial communication to F446RE
- `numpy` — coordinate math and transforms
- `torch` / `ultralytics` — YOLO for Phase 3-4 object detection
- `matplotlib` — visualization and debugging
- `ikpy` — inverse kinematics solver
- ROS2 — robot control system (built into DOFBOT-SE, learn alongside)

### Kinematics Strategy

Rather than depending on Yahboom's virtual machine environment (Windows only, not supported on Mac), port the DOFBOT-SE's URDF robot description files and feed them directly into `ikpy`. This gives you an accurate kinematic model — joint limits, link lengths, axis orientations — without any VM dependency. One line loads the entire arm model:

```python
import ikpy.chain
arm = ikpy.chain.Chain.from_urdf_file("dofbot_se.urdf")
```

From here, `arm.inverse_kinematics(target_position)` returns the joint angles needed to reach any XYZ coordinate. Your CV pipeline calculates the target. ikpy solves the math. Your F446RE driver executes the motion. The VM is never needed.

The URDF files can be extracted from Yahboom's VM image, sourced from their GitHub if published, or reconstructed by physically measuring the arm's link lengths and joint geometry.

### F446RE Layer (C++)

- PlatformIO — development environment
- STM32 HAL — hardware abstraction
- Custom UART driver — serial communication both directions
- Custom servo protocol implementation

### Tools

- Logic analyzer — protocol sniffing for Phase 2
- Oscilloscope — signal debugging
- Camera calibration target (checkerboard)

---

## Connection to Career Roadmap

### Why This Project Specifically

| Visuomotor Teaches      | JRC Scientific Needs       | Neuralink Needs             |
| ----------------------- | -------------------------- | --------------------------- |
| Custom cobot driver     | Custom cobot driver        | Embedded firmware           |
| CV-guided manipulation  | CV-guided panel wiring     | Neural signal decoding      |
| PC ↔ STM32 architecture | Industrial control systems | Device ↔ cloud architecture |
| Serial bus protocols    | Industrial protocols       | Neural data protocols       |
| Real-time CV pipeline   | Automation intelligence    | Real-time signal processing |

### The Larger Roadmap

```
NOW
├── CHIP-8 Emulator (CPU architecture fundamentals)
├── JRC Scientific Internship (real industrial embedded work)
└── Visuomotor Phase 1-2 (driver writing, kinematics)

6-12 MONTHS
├── Game Boy Emulator + APU (applied DSP, timing precision)
├── JRC Full Time after graduation (Fall 2026)
└── Visuomotor Phase 3-4 (CV-guided wire routing)

12-24 MONTHS
├── DSP Study: "Scientist and Engineer's Guide to DSP" - Steven Smith
├── OpenBCI EEG Acquisition Project (biosignal pipeline)
└── Real-time mental state classifier (Python + STM32)

24-36 MONTHS
├── Brain Computer Interface project (EEG → cursor control)
├── Neuralink / BMI company application
└── Resume: JRC + Visuomotor + EEG + BCI = complete profile

35-37 (TARGET)
└── $300k — Senior Embedded/ML Engineer, BMI company
    └── Jupiter return in 2nd house, 2030-2031
```

---

## DSP Parallel Study Plan

Running alongside Visuomotor:

**Phase 1 (Now):** Read "The Scientist and Engineer's Guide to Digital Signal Processing" by Steven Smith (free online). 30 minutes, 2-3x per week. No pressure to apply yet.

**Phase 2 (Game Boy period):** Implement the Game Boy APU (audio processing unit) fully. Square waves, noise generation, envelope control, sampling rates — this is DSP through emulation.

**Phase 3 (Year 2):** Build an EEG biosignal acquisition system:

- Hardware: OpenBCI Ganglion (~$200) or Cyton (~$500)
- Firmware: STM32 reading biosignals over SPI
- Pipeline: Python bandpass filtering, notch filter (60Hz), FFT frequency band extraction
- ML: Classify mental states (relaxed, focused, motor imagery)

**Phase 4 (Year 2-3):** Extend to a working BCI:

- Train model on delta/theta/alpha/beta/gamma band features
- Map classified mental states to computer inputs in real time
- This is functionally what Neuralink does — different electrodes, same pipeline

---

## Neuralink Internship Requirements — Gap Analysis

| Requirement                        | Status After Visuomotor + JRC              |
| ---------------------------------- | ------------------------------------------ |
| 2+ years embedded experience       | ✅ JRC provides this                       |
| Proficient C/C++ and Python        | ✅ Already have, deepened at JRC           |
| MCU architectures and peripherals  | ✅ STM32 F446RE + JRC hardware             |
| Reading schematics and datasheets  | ✅ JRC on-the-job                          |
| Embedded toolchains and workflow   | ✅ PlatformIO → JRC professional tools     |
| Strong EE & DSP fundamentals       | ⚠️ Close gap with DSP study plan above     |
| HW/SW debugging with lab equipment | ✅ JRC + Visuomotor Phase 2 logic analysis |
| ARM core embedded stacks           | ✅ STM32 is ARM Cortex-M4                  |
| Safety-critical systems            | ✅ Industrial panel wiring at JRC          |
| RF, BLE, TCP/IP embedded           | ⚠️ JRC wireless projects will help         |
| FPGA development                   | ❌ Address with Arty A7 board in Year 2    |

---

## Repository Structure (Suggested)

```
visuomotor/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── servo-protocol.md        # reverse engineered DOFBOT-SE protocol
│   └── calibration.md
├── firmware/                    # STM32 F446RE C++ (PlatformIO)
│   ├── platformio.ini
│   └── src/
│       ├── main.cpp
│       ├── serial_bridge.cpp    # PC communication
│       ├── servo_driver.cpp     # DOFBOT-SE protocol
│       └── kinematics.cpp       # joint angle math
├── vision/                      # PC-side Python
│   ├── pipeline.py              # main CV loop
│   ├── detector.py              # object detection
│   ├── calibration.py           # camera calibration
│   ├── planner.py               # path planning
│   └── serial_commander.py      # F446RE communication
├── phases/
│   ├── 01_whiteboard/
│   ├── 02_custom_driver/
│   ├── 03_pick_and_place/
│   └── 04_wire_routing/
└── tests/
```

---

_Document generated May 2026_  
_Part of the Yves-Langston Mays embedded systems and BMI career roadmap_
