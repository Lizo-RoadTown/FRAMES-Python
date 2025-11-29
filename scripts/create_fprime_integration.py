"""
Agent Alpha - Create F Prime Integration Module
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
check_in('alpha', 'modules/avionics/fprime_integration', 30, 'Creating F Prime Integration module in database')

try:
    # Create F Prime Integration Module
    cur.execute("""
        INSERT INTO modules (
            module_id, title, description, category,
            estimated_minutes, status, tags, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        'avionics_fprime_001',
        'F Prime Framework Integration',
        'Learn NASA JPL F Prime framework for flight software development. Covers component-based architecture, building deployments, creating custom components, and testing.',
        'avionics',
        90,
        'published',
        json.dumps({
            'subsystem': 'avionics',
            'difficulty': 'advanced',
            'prerequisites': ['avionics_orientation_001', 'avionics_firmware_001']
        }),
        datetime.now(),
        datetime.now()
    ))

    module_db_id = cur.fetchone()[0]
    print(f'[OK] Created module {module_db_id}: F Prime Framework Integration')

    # Create 9 sections
    sections = [
        {
            'title': 'Introduction to F Prime',
            'type': 'reading',
            'content': '''F Prime (F') is a component-based flight software framework developed by NASA's Jet Propulsion Laboratory (JPL) and used on multiple space missions.

**What is F Prime?**
F Prime is an open-source framework that provides:
- **Component-based architecture:** Modular building blocks for flight software
- **Auto-code generation:** Generates C++ code from XML specifications
- **Built-in telemetry/commanding:** Ground communication infrastructure
- **Testing framework:** Unit tests, integration tests, ground testing tools
- **Cross-platform:** Runs on embedded hardware and desktop for development

**Why Use F Prime?**
- **Heritage:** Used on Mars Helicopter (Ingenuity), multiple CubeSats, and JPL missions
- **Reusability:** Components can be reused across projects
- **Testability:** Ground testing infrastructure reduces flight risks
- **Open Source:** Free to use, active community support

**F Prime vs. Custom Flight Software:**
- **Custom:** Full control, but you build everything from scratch (OS abstraction, telemetry, commanding, logging)
- **F Prime:** Pre-built infrastructure, focus on mission-specific components

**CADENCE Context:**
CADENCE missions use F Prime to accelerate development and leverage NASA-proven flight software patterns. The framework handles communication, logging, and health monitoring, allowing teams to focus on mission payloads.

**Components in F Prime:**
F Prime applications are built from components:
- **Active Components:** Have their own thread, can run autonomously
- **Passive Components:** Called by other components, no thread
- **Queued Components:** Have message queue for asynchronous communication

Example components: command dispatcher, telemetry packetizer, sensor driver, power manager.''',
            'estimated_minutes': 12
        },
        {
            'title': 'F Prime Architecture Overview',
            'type': 'reading',
            'content': '''Understanding F Prime's architecture is key to building effective flight software.

**Core Concepts:**

**1. Components:**
Self-contained modules with defined interfaces (ports). Think of them as software "black boxes" that communicate via well-defined connections.

**2. Ports:**
Typed interfaces for component communication:
- **Input Ports:** Receive data/commands from other components
- **Output Ports:** Send data/commands to other components
- **Port Types:** Command, Telemetry, Event, Parameter, Data

**3. Topology:**
Defines how components are connected. The topology file specifies:
- Which components exist in the system
- How their ports are connected
- What runs on which threads

**Example Topology:**
```
CmdDispatcher.CmdOut -> PowerManager.CmdIn
PowerManager.TlmOut -> TlmPacketizer.TlmIn
SensorDriver.DataOut -> PowerManager.SensorDataIn
```

**4. Auto-Generation:**
F Prime uses XML/FPP files to define components and ports, then auto-generates:
- C++ class headers and implementation stubs
- Port serialization/deserialization code
- Telemetry dictionaries for ground systems
- Documentation

**Development Flow:**
1. Define component interfaces in XML/FPP
2. Run auto-code generator (fprime-util)
3. Implement component logic in C++ (fill in stubs)
4. Define topology connecting components
5. Build deployment
6. Test on ground system (GDS)
7. Flash to hardware

**File Structure:**
```
MyProject/
  Components/          # Custom components
    PowerManager/
      PowerManager.fpp  # Component definition
      PowerManager.cpp  # Implementation
  Top/                 # Topology
    topology.fpp       # System architecture
  build/               # Generated code + binaries
```

**Key Insight:**
F Prime separates interface definition (FPP/XML) from implementation (C++). This enables auto-code generation and ensures type-safe component communication.''',
            'estimated_minutes': 15
        },
        {
            'title': 'Setting Up F Prime Development Environment',
            'type': 'exercise',
            'content': '''Let's set up F Prime on your development machine and create your first deployment.

**Prerequisites:**
- Linux, macOS, or WSL2 on Windows
- Python 3.7+ with pip
- CMake 3.16+
- C++ compiler (gcc/clang)
- Git

**Step 1: Install F Prime Tools**
```bash
# Install fprime-tools via pip
pip install fprime-tools

# Verify installation
fprime-util --version
```

**Step 2: Clone F Prime Repository**
```bash
# Clone F Prime framework
git clone https://github.com/nasa/fprime.git
cd fprime

# Checkout latest stable release
git checkout v3.4.0
```

**Step 3: Create a New Project**
```bash
# Create project using fprime template
fprime-util new --project

# Follow prompts:
# Project name: MyCubeSat
# Directory: ./MyCubeSat

cd MyCubeSat
```

**Step 4: Generate a Reference Deployment**
```bash
# Generate reference topology
fprime-util generate

# Build the deployment
fprime-util build
```

**Step 5: Run Ground Data System (GDS)**
```bash
# Launch GDS web interface
fprime-gds -n

# Open browser to http://localhost:5000
# You should see the F Prime ground station interface
```

**Step 6: Run Your First Application**
```bash
# In another terminal, run the deployment
fprime-util run

# In GDS web interface:
# - Navigate to "Commanding" tab
# - Send command "cmdDisp.CMD_NO_OP"
# - Check "Events" tab for confirmation
```

**Success Criteria:**
- Build completes with no errors
- GDS launches and connects to deployment
- You can send commands and see telemetry

**Exercise:**
1. Build the Ref (reference) deployment included in F Prime
2. Launch GDS and send 5 different commands
3. Observe telemetry and events in GDS interface

**Troubleshooting:**
- Build errors: Ensure CMake version is 3.16+
- GDS won't connect: Check firewall, try different port with `--port`
- Import errors: Activate Python virtual environment''',
            'estimated_minutes': 25
        },
        {
            'title': 'Creating Your First Component',
            'type': 'exercise',
            'content': '''Let's create a custom F Prime component that reads a temperature sensor and reports telemetry.

**Component Specification:**
- **Name:** TempSensor
- **Type:** Active (has thread, polls sensor periodically)
- **Inputs:** Command port (start/stop polling)
- **Outputs:** Telemetry port (temperature readings), Event port (status messages)

**Step 1: Generate Component Template**
```bash
cd MyCubeSat/Components

# Generate new active component
fprime-util new --component

# Follow prompts:
# Component name: TempSensor
# Component kind: active
# Component namespace: MyCubeSat
```

**Step 2: Define Component Interface (FPP)**
Edit `TempSensor/TempSensor.fpp`:

```fpp
module MyCubeSat {

  @ Temperature sensor component
  active component TempSensor {

    # Commands
    async command START_POLLING()
    async command STOP_POLLING()

    # Telemetry
    telemetry TEMP_READING: F32 id 0
    telemetry SAMPLE_COUNT: U32 id 1

    # Events
    event PollingStarted() severity activity high
    event PollingStopped() severity activity high
    event TempRead(temp: F32) severity diagnostic

    # Parameters
    param POLL_INTERVAL_MS: U32 default 1000

    # Standard ports
    include "Components/Common/fprime-ports.fpp"
  }
}
```

**Step 3: Auto-Generate C++ Code**
```bash
cd TempSensor
fprime-util impl

# This creates TempSensor.hpp, TempSensor.cpp with stubs
```

**Step 4: Implement Component Logic**
Edit `TempSensor.cpp`:

```cpp
void TempSensor::START_POLLING_cmdHandler(
    FwOpcodeType opCode,
    U32 cmdSeq
) {
    this->m_polling = true;
    this->log_ACTIVITY_HI_PollingStarted();
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

void TempSensor::STOP_POLLING_cmdHandler(
    FwOpcodeType opCode,
    U32 cmdSeq
) {
    this->m_polling = false;
    this->log_ACTIVITY_HI_PollingStopped();
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

// Run method called periodically by active component thread
void TempSensor::schedIn_handler(NATIVE_INT_TYPE portNum, U32 context) {
    if (this->m_polling) {
        // Read sensor (stubbed for now)
        F32 temp = this->readSensor();

        // Send telemetry
        this->tlmWrite_TEMP_READING(temp);
        this->tlmWrite_SAMPLE_COUNT(++this->m_sampleCount);

        // Log event
        this->log_DIAGNOSTIC_TempRead(temp);
    }
}

F32 TempSensor::readSensor() {
    // TODO: Replace with actual I2C sensor read
    return 25.0 + (rand() % 10); // Simulated temperature
}
```

**Step 5: Add Component to Topology**
Edit `Top/topology.fpp` to instantiate and connect TempSensor.

**Step 6: Build and Test**
```bash
cd ../..
fprime-util build
fprime-gds -n
```

**Exercise:**
1. Create the TempSensor component following the steps above
2. Build successfully
3. Send START_POLLING command via GDS
4. Observe TEMP_READING telemetry updating
5. Send STOP_POLLING and verify telemetry stops

**Success Criteria:**
- Component builds without errors
- Commands execute successfully
- Telemetry appears in GDS
- Events logged correctly''',
            'estimated_minutes': 30
        },
        {
            'title': 'Component Communication and Ports',
            'type': 'reading',
            'content': '''Understanding how F Prime components communicate is critical for building complex systems.

**Port Types:**

**1. Command Ports:**
Receive commands from command dispatcher or other components.
- **Async Commands:** Queued, processed by component thread
- **Sync Commands:** Executed immediately by caller's thread
- **Guarded Commands:** Thread-safe synchronous commands

**2. Telemetry Ports:**
Send telemetry data to telemetry packetizer for downlink.
- Typed channels (F32, U32, string, etc.)
- Automatic timestamping
- Configurable update rates

**3. Event Ports:**
Log significant events (errors, warnings, diagnostics).
- Severity levels: FATAL, WARNING_HI, WARNING_LO, ACTIVITY_HI, ACTIVITY_LO, DIAGNOSTIC
- Auto-generated event IDs
- Downlinked to ground for monitoring

**4. Parameter Ports:**
Get/set configuration parameters.
- Persistent storage (survives reboots)
- Ground-updatable
- Type-safe

**5. Data Ports (Custom):**
User-defined data structures for component-to-component communication.

**Port Connections in Topology:**
Connections are defined in `topology.fpp`:

```fpp
connections Connections {
  # Command path
  cmdDisp.compCmdSend -> tempSensor.cmdIn

  # Telemetry path
  tempSensor.tlmOut -> tlmPacketizer.tlmRecv

  # Event path
  tempSensor.eventOut -> eventLogger.eventRecv

  # Custom data port
  tempSensor.tempDataOut -> powerMgr.tempDataIn
}
```

**Synchronous vs. Asynchronous:**
- **Sync ports:** Direct function call, executes in caller's context
- **Async ports:** Message queued, processed by receiver's thread
- Active components typically use async ports to avoid blocking

**Rate Groups:**
Components can be scheduled at different rates:
```fpp
instance rateGroup1Hz: Svc.ActiveRateGroup base id 0x200
instance rateGroup10Hz: Svc.ActiveRateGroup base id 0x300

rateGroup1Hz.RateGroupMemberOut[0] -> tempSensor.schedIn
rateGroup10Hz.RateGroupMemberOut[0] -> imuDriver.schedIn
```

This schedules tempSensor at 1 Hz and imuDriver at 10 Hz.

**Best Practice:**
Design components with minimal coupling - use ports for all communication, never access another component's internal state directly.''',
            'estimated_minutes': 18
        },
        {
            'title': 'Building and Deploying F Prime Applications',
            'type': 'reading',
            'content': '''Deploying F Prime software to flight hardware requires understanding the build system and cross-compilation.

**Build System Overview:**
F Prime uses CMake for build configuration and supports multiple targets:
- **Native:** Builds for your development machine (Linux/macOS)
- **ARM:** Cross-compile for ARM processors (Cortex-M, Cortex-A)
- **Linux-ARM:** For single-board computers (Raspberry Pi, BeagleBone)

**Build Commands:**

**Development Build (Native):**
```bash
fprime-util build
# Output: build-artifacts/Linux/bin/MyDeployment
```

**ARM Cross-Compile:**
```bash
# Specify toolchain
fprime-util build --toolchain arm-linux-gnueabihf

# Output: build-artifacts/arm-linux-gnueabihf/bin/MyDeployment
```

**Deployment Structure:**
An F Prime deployment is an executable that includes:
- Component implementations
- Topology (component instances and connections)
- Main entry point
- OS abstraction layer

**Creating a Deployment:**
```bash
fprime-util new --deployment

# Deployment name: FlightComputer
# This creates FlightComputer/Top/ directory
```

**Deployment Configuration:**

Edit `FlightComputer/Top/CMakeLists.txt`:
```cmake
set(SOURCE_FILES
  "${CMAKE_CURRENT_LIST_DIR}/topology.fpp"
  "${CMAKE_CURRENT_LIST_DIR}/Main.cpp"
)

add_fprime_deployment(FlightComputer ${SOURCE_FILES})
```

**Cross-Compilation for STM32:**

Create `cmake/toolchain/stm32.cmake`:
```cmake
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

Build with:
```bash
fprime-util build --toolchain cmake/toolchain/stm32.cmake
```

**Flashing to Hardware:**
After cross-compiling, flash binary to flight computer:
```bash
# Convert ELF to BIN
arm-none-eabi-objcopy -O binary FlightComputer.elf FlightComputer.bin

# Flash with OpenOCD (example for STM32)
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program FlightComputer.bin verify reset exit 0x08000000"
```

**Verification:**
1. Check binary size fits in flash memory
2. Verify all symbols resolved (no undefined references)
3. Test deployment on hardware development board before flight unit

**CADENCE Deployment:**
Typical CADENCE deployment includes:
- Command dispatcher
- Telemetry packetizer
- UHF radio driver
- Sensor drivers (IMU, magnetometer, sun sensors)
- Power manager
- Mission-specific payload components''',
            'estimated_minutes': 20
        },
        {
            'title': 'Testing F Prime Components',
            'type': 'reading',
            'content': '''Rigorous testing is essential for flight software. F Prime provides multiple testing frameworks.

**Testing Levels:**

**1. Unit Tests:**
Test individual components in isolation using auto-generated test harness.

**Generate Unit Test:**
```bash
cd Components/TempSensor
fprime-util impl --ut

# Creates TempSensorTestMain.cpp, TempSensorTester.cpp
```

**Example Unit Test:**
```cpp
void TempSensorTester::testStartPolling() {
    // Send START_POLLING command
    this->sendCmd_START_POLLING(0, 0);
    this->component.doDispatch();

    // Verify command response OK
    ASSERT_EVENTS_PollingStarted_SIZE(1);
    ASSERT_CMD_RESPONSE_SIZE(1);
    ASSERT_CMD_RESPONSE(0, TempSensor::OPCODE_START_POLLING,
                        0, Fw::CmdResponse::OK);
}
```

**Run Unit Tests:**
```bash
fprime-util check
```

**2. Integration Tests:**
Test component interactions in full topology.

**Ground Data System (GDS) Testing:**
- Launch deployment with GDS
- Manually send commands and verify telemetry
- Script test sequences with Python

**Python Integration Test:**
```python
from fprime_gds.common.testing import integration_test

class TestTempSensor(integration_test.IntegrationTest):
    def test_polling(self):
        # Send START_POLLING command
        self.send_command("tempSensor.START_POLLING")

        # Wait for telemetry
        tlm = self.await_telemetry("tempSensor.TEMP_READING", timeout=5.0)
        self.assertIsNotNone(tlm)

        # Verify temperature in valid range
        self.assertGreater(tlm.value, -50.0)
        self.assertLess(tlm.value, 150.0)
```

**3. Hardware-in-Loop (HIL) Testing:**
Run F Prime deployment on actual flight hardware with sensor/actuator connections:
- Verify sensor readings are correct
- Test actuator commands (reaction wheels, magnetorquers)
- Validate timing constraints met

**4. Flat-Sat Testing:**
Full spacecraft replica on the bench:
- All subsystems connected
- Simulate mission scenarios (eclipse, ground pass, payload operations)
- Validate end-to-end behavior

**Test Coverage:**
F Prime supports code coverage analysis:
```bash
fprime-util build --coverage
fprime-util check
fprime-util coverage

# Generates HTML report in build-artifacts/coverage/
```

**Continuous Integration:**
Automate testing in CI/CD pipeline:
```yaml
# .github/workflows/test.yml
name: F Prime CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install fprime-tools
      - run: fprime-util generate
      - run: fprime-util build
      - run: fprime-util check
```

**Best Practice:**
Aim for >80% code coverage with unit tests. Integration tests catch interaction bugs. HIL testing validates hardware assumptions.''',
            'estimated_minutes': 18
        },
        {
            'title': 'F Prime Ground Data System',
            'type': 'reading',
            'content': '''The Ground Data System (GDS) is F Prime's interface for monitoring and commanding the spacecraft.

**GDS Features:**
- **Commanding:** Send commands to spacecraft
- **Telemetry:** View real-time and historical telemetry
- **Events:** Monitor system events and alerts
- **Sequences:** Upload command sequences for autonomous operations
- **Uplink/Downlink:** File transfer to/from spacecraft

**Starting GDS:**
```bash
# Launch web-based GDS
fprime-gds -n

# Connect to remote deployment
fprime-gds -n --ip 192.168.1.100 --port 50000
```

**GDS Web Interface Tabs:**

**1. Commanding:**
- Browse available commands by component
- Fill in command arguments
- Send immediately or add to sequence
- View command history

**2. Telemetry:**
- Real-time plots of telemetry channels
- Tabular view with latest values
- Historical data download
- Custom dashboards

**3. Events:**
- Color-coded by severity (red=fatal, yellow=warning, white=diagnostic)
- Filter by component or severity
- Search event history
- Export logs

**4. Channels:**
- All telemetry channels listed
- Search/filter capabilities
- Set custom limits for alerts

**5. Sequences:**
- Upload command sequences (CSV or JSON format)
- Validate before uplink
- Track execution status

**Custom Dashboards:**
Create custom visualization dashboards:
```python
# dashboard_config.py
from fprime_gds.common.gds_cli.dashboard import Dashboard

dashboard = Dashboard()
dashboard.add_plot("Temperature", ["tempSensor.TEMP_READING"])
dashboard.add_plot("Power", ["eps.BATTERY_VOLTAGE", "eps.BUS_CURRENT"])
dashboard.add_gauge("Battery %", "eps.BATTERY_SOC", min=0, max=100)
```

**Scripting with GDS:**
Automate operations with Python API:
```python
from fprime_gds.common.gds_cli import GdsApi

gds = GdsApi()

# Send command
gds.send_command("tempSensor.START_POLLING")

# Wait for event
event = gds.await_event("tempSensor.PollingStarted", timeout=5.0)

# Get telemetry
temp = gds.get_telemetry("tempSensor.TEMP_READING")
print(f"Current temperature: {temp.value} C")
```

**Radio Integration:**
GDS can connect to spacecraft via radio link:
- Configure radio adapter (serial port, TCP/IP)
- GDS handles packetization/depacketization
- Supports AX.25, CCSDS protocols

**Mission Operations:**
During actual mission:
1. Ground station receives radio downlink
2. GDS processes telemetry packets
3. Operators monitor dashboards for anomalies
4. Commands uplinked in response to events
5. All activities logged for mission archive

**CADENCE Ground Operations:**
CADENCE teams use GDS for:
- Daily health checks via scheduled ground passes
- Uploading mission timelines
- Debugging anomalies
- Student training on ground systems''',
            'estimated_minutes': 15
        },
        {
            'title': 'Knowledge Check',
            'type': 'quiz',
            'content': json.dumps({
                'questions': [
                    {
                        'question': 'What is the primary benefit of F Prime\'s component-based architecture?',
                        'options': [
                            'Faster execution speed',
                            'Smaller binary size',
                            'Reusability and modularity of flight software components',
                            'Easier to learn than C'
                        ],
                        'correct': 2,
                        'explanation': 'F Prime components are reusable modules that can be shared across projects, reducing development time and increasing reliability.'
                    },
                    {
                        'question': 'What language is used to define F Prime component interfaces?',
                        'options': [
                            'Python',
                            'FPP (F Prime Prime) or XML',
                            'JavaScript',
                            'MATLAB'
                        ],
                        'correct': 1,
                        'explanation': 'F Prime uses FPP or XML to define component interfaces, which are then auto-generated into C++ code.'
                    },
                    {
                        'question': 'Which F Prime port type is used to send telemetry data to the ground?',
                        'options': [
                            'Command port',
                            'Event port',
                            'Telemetry port',
                            'Data port'
                        ],
                        'correct': 2,
                        'explanation': 'Telemetry ports are specifically designed to send typed data channels to the telemetry packetizer for downlink.'
                    },
                    {
                        'question': 'What is the purpose of the Ground Data System (GDS)?',
                        'options': [
                            'Compile F Prime code',
                            'Monitor and command the spacecraft from the ground',
                            'Flash firmware to the flight computer',
                            'Simulate orbital mechanics'
                        ],
                        'correct': 1,
                        'explanation': 'GDS provides a web interface for ground operators to send commands, monitor telemetry, and view events from the spacecraft.'
                    },
                    {
                        'question': 'In F Prime, what does the topology define?',
                        'options': [
                            'The physical layout of circuit boards',
                            'How components are instantiated and connected',
                            'The radio frequency bands used',
                            'The power budget'
                        ],
                        'correct': 1,
                        'explanation': 'The topology file defines which component instances exist and how their ports are connected to form the complete system.'
                    },
                    {
                        'question': 'Why is unit testing important for F Prime components?',
                        'options': [
                            'It makes the code run faster',
                            'It reduces memory usage',
                            'It validates component behavior before integration and flight',
                            'It is only needed for Python code'
                        ],
                        'correct': 2,
                        'explanation': 'Unit tests validate individual component behavior in isolation, catching bugs early before they reach integration or flight testing.'
                    }
                ]
            }),
            'estimated_minutes': 7
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
    release_resource('alpha', 'modules/avionics/fprime_integration',
                    f'Created F Prime Integration module (ID {module_db_id}) with 9 sections',
                    {'module_db_id': module_db_id, 'sections': 9})

    print(f'\n[SUCCESS] F Prime Integration module complete!')

except Exception as e:
    conn.rollback()
    print(f'[ERROR] {e}')
    import traceback
    traceback.print_exc()
finally:
    conn.close()
