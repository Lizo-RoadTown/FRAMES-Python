"""
Agent Alpha - Create Avionics Orientation Module
"""

import psycopg2
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.agent_utils import check_in, release_resource

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Check in - creating module
check_in('alpha', 'modules/avionics/orientation', 30, 'Creating Avionics Orientation module in database')

try:
    # Create Avionics Orientation Module
    cur.execute("""
        INSERT INTO modules (
            module_id, title, description, category,
            estimated_minutes, status, tags, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        'avionics_orientation_001',
        'Avionics Orientation',
        'Introduction to CubeSat avionics systems, covering flight computers, communication systems, sensors, and firmware development workflows.',
        'avionics',
        60,
        'published',
        json.dumps({
            'subsystem': 'avionics',
            'difficulty': 'beginner',
            'prerequisites': []
        }),
        datetime.now(),
        datetime.now()
    ))

    module_db_id = cur.fetchone()[0]
    print(f'[OK] Created module {module_db_id}: Avionics Orientation')

    # Create 6 sections
    sections = [
        {
            'title': 'What is Avionics?',
            'type': 'reading',
            'content': '''Avionics (aviation electronics) encompasses all electronic systems aboard a spacecraft. For CubeSats, the avionics subsystem includes:

**Flight Computer (OBC):** The "brain" of the CubeSat - manages all onboard operations, executes mission software, and coordinates between subsystems.

**Communication Systems:** Radio transceivers for ground communication, telemetry downlink, and command uplink.

**Sensors:** Attitude determination sensors (gyroscopes, magnetometers, sun sensors), environmental sensors (temperature, radiation).

**Data Handling:** Storage systems, onboard processing, and data compression for downlink.

**Why Avionics Matters:**
The avionics subsystem is mission-critical - if the flight computer fails or communication is lost, the entire mission fails. Avionics must be extremely reliable, power-efficient, and radiation-tolerant.

**CADENCE Context:**
The CADENCE missions use commercial-off-the-shelf (COTS) flight computers with custom firmware development, balancing reliability with cost constraints.''',
            'estimated_minutes': 8
        },
        {
            'title': 'Flight Computer Architecture',
            'type': 'reading',
            'content': '''Modern CubeSat flight computers typically use ARM or RISC-V processors with specialized features for space applications.

**Key Components:**
- **Processor:** Low-power ARM Cortex-M or similar (e.g., STM32, Nordic nRF)
- **Memory:** Flash storage for firmware, RAM for runtime operations
- **Interfaces:** I2C, SPI, UART for subsystem communication
- **Watchdog Timer:** Automatically resets computer if software hangs
- **Real-Time Clock:** Maintains mission time

**Software Stack:**
Flight computers run real-time operating systems (RTOS) or bare-metal firmware:
- **F Prime (NASA JPL):** Component-based flight software framework
- **FreeRTOS:** Popular open-source RTOS
- **Bare-metal:** Direct hardware control for maximum reliability

**Redundancy:**
Many missions include dual redundant flight computers - if the primary fails, the backup takes over automatically.''',
            'estimated_minutes': 10
        },
        {
            'title': 'Communication Systems Overview',
            'type': 'reading',
            'content': '''CubeSats communicate with ground stations via radio transceivers operating in amateur radio bands (UHF, VHF, S-band).

**Radio System Components:**
- **Transceiver:** Combined transmitter/receiver module
- **Antenna:** Deployable dipole or patch antennas
- **Protocol:** AX.25 packet radio or custom protocols
- **Modulation:** GMSK, FSK, or BPSK for data encoding

**Communication Challenges:**
- **Limited power:** Typically 1-2W transmit power
- **Doppler shift:** Frequency changes as satellite moves
- **Link budget:** Calculate if signal is strong enough to reach ground
- **Ground station coordination:** Schedule passes with amateur radio network

**CADENCE Approach:**
CADENCE missions use UHF transceivers with AX.25 protocol, allowing amateur radio operators worldwide to receive telemetry.''',
            'estimated_minutes': 10
        },
        {
            'title': 'Sensor Integration',
            'type': 'reading',
            'content': '''Avionics integrates sensors from multiple subsystems to determine spacecraft state and environment.

**Attitude Determination Sensors:**
- **Magnetometer:** Measures Earth's magnetic field for orientation
- **Gyroscope:** Tracks rotation rates
- **Sun sensors:** Detect sun direction for pointing
- **Star tracker:** High-precision attitude from star field (expensive)

**Environmental Sensors:**
- **Temperature sensors:** Monitor thermal state
- **Radiation counters:** Track cumulative radiation dose
- **Current/voltage sensors:** Monitor power subsystem

**Interface Standards:**
Most sensors use I2C or SPI digital interfaces:
- **I2C:** 2-wire bus, multiple devices on same bus
- **SPI:** 4-wire bus, higher speed, point-to-point

**Calibration:**
All sensors require calibration - pre-launch testing determines sensor biases and scale factors.''',
            'estimated_minutes': 12
        },
        {
            'title': 'Firmware Development Workflow',
            'type': 'reading',
            'content': '''Developing flight software follows rigorous processes to ensure reliability.

**Development Phases:**
1. **Requirements:** Define what software must do
2. **Design:** Architecture and component interfaces
3. **Implementation:** Write code following standards
4. **Unit Testing:** Test individual components
5. **Integration Testing:** Test component interactions
6. **Flat-sat Testing:** Test on hardware replica on bench
7. **Flight Software Upload:** Load final software onto flight computer

**Tools & Environment:**
- **IDE:** STM32CubeIDE, VS Code with embedded extensions
- **Version Control:** Git for tracking all changes
- **Build System:** CMake, Makefiles
- **Debugger:** JTAG/SWD hardware debuggers
- **Simulator:** Test software before hardware available

**CADENCE Workflow:**
Teams use F Prime framework with Python scripts for ground testing, GitHub for version control, and automated testing pipelines.''',
            'estimated_minutes': 15
        },
        {
            'title': 'Knowledge Check',
            'type': 'quiz',
            'content': json.dumps({
                'questions': [
                    {
                        'question': 'What is the primary function of the flight computer (OBC)?',
                        'options': [
                            'Generate electrical power',
                            'Manage all onboard operations and coordinate subsystems',
                            'Provide propulsion',
                            'Shield from radiation'
                        ],
                        'correct': 1,
                        'explanation': 'The flight computer is the "brain" - it manages operations and coordinates all subsystems.'
                    },
                    {
                        'question': 'Why do CubeSats often use redundant flight computers?',
                        'options': [
                            'To increase computational power',
                            'To reduce power consumption',
                            'To provide backup if primary fails',
                            'To save cost'
                        ],
                        'correct': 2,
                        'explanation': 'Redundancy provides a backup computer that can take over if the primary fails, increasing mission reliability.'
                    },
                    {
                        'question': 'Which sensor is used to determine spacecraft orientation relative to Earth magnetic field?',
                        'options': [
                            'Gyroscope',
                            'Sun sensor',
                            'Magnetometer',
                            'Star tracker'
                        ],
                        'correct': 2,
                        'explanation': 'Magnetometers measure Earth magnetic field direction, enabling attitude determination.'
                    },
                    {
                        'question': 'What protocol is commonly used for CubeSat radio communication?',
                        'options': [
                            'HTTP',
                            'AX.25 packet radio',
                            'Bluetooth',
                            'Wi-Fi'
                        ],
                        'correct': 1,
                        'explanation': 'AX.25 is a packet radio protocol widely used in amateur radio and CubeSat communications.'
                    }
                ]
            }),
            'estimated_minutes': 5
        }
    ]

    # Insert all sections
    for idx, section in enumerate(sections, 1):
        cur.execute("""
            INSERT INTO module_sections (
                module_id, title, section_number, section_type,
                content, duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            module_db_id,
            section['title'],
            idx,
            section['type'],
            section['content'],
            section['estimated_minutes'] * 60,  # Convert minutes to seconds
            datetime.now()
        ))
        print(f'  [OK] Section {idx}: {section["title"]} ({section["type"]})')

    conn.commit()

    # Release resource
    release_resource('alpha', 'modules/avionics/orientation',
                    f'Created Avionics Orientation module (ID {module_db_id}) with 6 sections',
                    {'module_db_id': module_db_id, 'sections': 6})

    print(f'\n[SUCCESS] Avionics Orientation module complete!')

except Exception as e:
    conn.rollback()
    print(f'[ERROR] {e}')
    import traceback
    traceback.print_exc()
finally:
    conn.close()
