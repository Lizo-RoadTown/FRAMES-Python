"""
Agent Alpha - Create Firmware Flashing Module
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
check_in('alpha', 'modules/avionics/firmware_flashing', 30, 'Creating Firmware Flashing module in database')

try:
    # Create Firmware Flashing Module
    cur.execute("""
        INSERT INTO modules (
            module_id, title, description, category,
            estimated_minutes, status, tags, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        'avionics_firmware_001',
        'Firmware Flashing Fundamentals',
        'Learn how to flash firmware onto CubeSat flight computers, covering tools, interfaces, step-by-step procedures, verification, and troubleshooting.',
        'avionics',
        75,
        'published',
        json.dumps({
            'subsystem': 'avionics',
            'difficulty': 'intermediate',
            'prerequisites': ['avionics_orientation_001']
        }),
        datetime.now(),
        datetime.now()
    ))

    module_db_id = cur.fetchone()[0]
    print(f'[OK] Created module {module_db_id}: Firmware Flashing Fundamentals')

    # Create 8 sections
    sections = [
        {
            'title': 'Firmware vs. Software: What\'s the Difference?',
            'type': 'reading',
            'content': '''Before diving into flashing, it's important to understand what firmware is and how it differs from regular software.

**Software:** Programs that run on top of an operating system (like apps on your phone or programs on your computer). Can be installed, updated, or removed easily.

**Firmware:** Low-level software that directly controls hardware. Stored in non-volatile memory (flash, ROM) and persists even when power is removed. Acts as the "permanent software" for a device.

**For CubeSats:**
The flight computer's firmware includes:
- **Bootloader:** First code that runs on power-up, allows firmware updates
- **Operating system or RTOS:** Manages tasks, memory, and hardware resources
- **Application code:** Mission-specific software (F Prime components, custom tasks)
- **Hardware drivers:** Code that directly controls sensors, radios, actuators

**Why Flashing Matters:**
"Flashing" is the process of writing firmware to the flight computer's non-volatile memory. You'll flash firmware to:
- Upload initial flight software before launch
- Fix bugs discovered during testing
- Update mission parameters
- Recover from software failures

Getting this right is critical - a bad flash can brick the flight computer.''',
            'estimated_minutes': 10
        },
        {
            'title': 'Hardware Interfaces for Flashing',
            'type': 'reading',
            'content': '''Flight computers expose debug/programming interfaces for firmware flashing. Understanding these interfaces is essential.

**Common Interfaces:**

**1. JTAG (Joint Test Action Group):**
- Industry standard debug interface (IEEE 1149.1)
- 5+ pins: TDI, TDO, TCK, TMS, TRST, GND
- Allows full debugging: breakpoints, memory inspection, step-through
- Slower than SWD but more universal

**2. SWD (Serial Wire Debug):**
- ARM-specific 2-wire interface (SWDIO, SWCLK + GND, power)
- Faster than JTAG, fewer pins (saves PCB space)
- Used on STM32, Nordic nRF, most ARM Cortex-M processors
- Also supports debugging features

**3. UART/Serial Bootloader:**
- Uses standard serial port (TX, RX, GND)
- Built-in bootloader on most microcontrollers
- Requires specific boot pin configuration
- Slower, no debugging capability

**Programmer Hardware:**
To flash via JTAG/SWD, you need a programmer (also called debugger or probe):
- **ST-Link:** For STM32 microcontrollers (~$25)
- **J-Link (Segger):** Professional tool, supports many architectures (~$400)
- **Black Magic Probe:** Open-source ARM debugger (~$70)

**CADENCE Context:**
Most CADENCE flight computers use ARM processors with SWD interfaces and ST-Link programmers for development.''',
            'estimated_minutes': 12
        },
        {
            'title': 'Flashing Tools and Software',
            'type': 'reading',
            'content': '''Different manufacturers provide tools for flashing firmware onto their microcontrollers.

**ARM/STM32 Tools:**
- **STM32CubeProgrammer:** Official ST tool, GUI and CLI, supports ST-Link
- **OpenOCD:** Open-source tool, supports JTAG/SWD, integrates with GDB debugger
- **pyOCD:** Python-based tool for ARM Cortex-M, good for automation

**AVR/Arduino:**
- **avrdude:** Command-line tool for AVR microcontrollers
- **Arduino IDE:** Built-in uploader for Arduino boards

**Command-Line Example (OpenOCD):**
```bash
# Flash firmware.bin to STM32 via ST-Link
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program firmware.bin verify reset exit 0x08000000"
```

**Build Systems Integration:**
Modern workflows integrate flashing into build systems:
- **PlatformIO:** `pio run -t upload`
- **CMake + OpenOCD:** `make flash`
- **F Prime:** `fprime-util build --deploy`

**Verification:**
Always verify the flash succeeded:
- Read back memory and compare to original binary
- Check CRC checksums
- Most tools have built-in `verify` commands

**CADENCE Workflow:**
Teams typically use STM32CubeProgrammer during development and OpenOCD for automated testing in CI/CD pipelines.''',
            'estimated_minutes': 12
        },
        {
            'title': 'Step-by-Step: Flashing Your First Firmware',
            'type': 'exercise',
            'content': '''Follow this step-by-step procedure to flash firmware onto a flight computer development board.

**Prerequisites:**
- Flight computer dev board (e.g., STM32 Nucleo, Arduino)
- Programmer (ST-Link, J-Link, or USB cable for Arduino)
- Firmware binary file (.bin, .hex, or .elf)
- Flashing tool installed (STM32CubeProgrammer, Arduino IDE, or OpenOCD)

**Step 1: Connect Hardware**
1. Connect programmer to flight computer's debug header
2. Ensure correct pin mapping (SWDIO, SWCLK, GND, VCC)
3. Power the board (via programmer or external supply)
4. Verify power LED is on

**Step 2: Prepare Firmware**
1. Locate your compiled firmware file (e.g., `firmware.bin`)
2. Note the flash address (typically 0x08000000 for STM32)
3. Ensure file is not corrupted (check file size matches expected)

**Step 3: Launch Flashing Tool**
- **STM32CubeProgrammer:** Launch GUI, select ST-Link, click "Connect"
- **Arduino IDE:** Select board and port, click "Upload"
- **OpenOCD:** Run command-line with correct config files

**Step 4: Erase Flash (if needed)**
Some tools auto-erase, others require manual step:
- In STM32CubeProgrammer: Click "Full Chip Erase"
- OpenOCD: Include `flash erase_sector` command

**Step 5: Program Flash**
- Browse to firmware file and select flash address
- Click "Start Programming" or run CLI command
- Wait for progress bar to complete (typically 10-60 seconds)

**Step 6: Verify**
- Enable "Verify after programming" option
- Tool reads back flash memory and compares to file
- Look for "Verification...OK" message

**Step 7: Reset and Run**
- Disconnect programmer (or leave connected for debugging)
- Reset the board (press reset button or power cycle)
- Verify firmware is running (LEDs blink, serial output, etc.)

**Success Criteria:**
- No errors during programming
- Verification passed
- Board executes firmware correctly after reset

**Exercise:**
Flash a simple "blink LED" firmware to your dev board and verify it runs.''',
            'estimated_minutes': 20
        },
        {
            'title': 'Bootloaders and Remote Updates',
            'type': 'reading',
            'content': '''For deployed CubeSats, you can't physically connect a programmer. Bootloaders enable remote firmware updates.

**What is a Bootloader?**
A bootloader is a small program stored in protected flash memory that:
1. Runs first when the microcontroller powers on
2. Checks if new firmware is available (via radio, SD card, etc.)
3. If yes: writes new firmware to application flash region
4. If no: jumps to application code and runs normally

**Bootloader Architecture:**
Flash memory is partitioned:
```
0x08000000: [Bootloader] (16 KB, protected)
0x08004000: [Application] (remaining flash)
```

**Remote Update Process:**
1. **Ground station** uploads new firmware via radio in small packets
2. **Flight computer** stores packets in temporary buffer (RAM or SD card)
3. **Bootloader** verifies checksum, then overwrites application flash
4. **Bootloader** marks new firmware as valid and reboots
5. **Application** runs new firmware

**Safety Features:**
- **Dual-bank flash:** Keep old firmware as backup
- **CRC verification:** Reject corrupted firmware
- **Watchdog timer:** Auto-revert if new firmware crashes
- **Rollback mechanism:** Command to restore previous version

**CADENCE Approach:**
CubeSats typically have bootloaders for ground-commanded updates during the mission. Critical for fixing bugs discovered post-launch.

**Development vs. Flight:**
- **Development:** Use JTAG/SWD for fast iteration
- **Flight:** Use bootloader for updates (JTAG not accessible in orbit)''',
            'estimated_minutes': 10
        },
        {
            'title': 'Common Flashing Issues and Troubleshooting',
            'type': 'reading',
            'content': '''Even experienced engineers encounter flashing issues. Here's how to diagnose and fix common problems.

**Issue 1: Programmer Not Detected**
- **Symptoms:** Tool says "No device connected" or "ST-Link not found"
- **Causes:**
  - USB cable disconnected or faulty
  - Driver not installed
  - Programmer hardware failure
- **Fixes:**
  - Check USB connection, try different cable/port
  - Reinstall drivers (ST-Link drivers for STM32)
  - Test programmer on known-good board

**Issue 2: Cannot Connect to Target**
- **Symptoms:** Tool detects programmer but can't communicate with microcontroller
- **Causes:**
  - Wrong debug interface selected (JTAG vs SWD)
  - Incorrect wiring (SWDIO/SWCLK swapped)
  - Target not powered
  - Target held in reset
  - NRST pin conflict
- **Fixes:**
  - Verify SWD wiring with multimeter
  - Check target power supply (should be 3.3V)
  - Try "Connect under reset" mode
  - Disable hardware reset in tool settings

**Issue 3: Flash Protected / Locked**
- **Symptoms:** "Flash is read-protected" or "Device is locked"
- **Causes:**
  - Read/write protection enabled in option bytes
  - Security features enabled
- **Fixes:**
  - Disable read protection (WARNING: erases chip)
  - Use manufacturer's unlock procedure
  - For STM32: Use STM32CubeProgrammer "Option Bytes" menu

**Issue 4: Verification Failed**
- **Symptoms:** Programming succeeds but verification fails
- **Causes:**
  - Wrong flash address
  - File corrupted
  - Hardware issue (bad flash memory)
- **Fixes:**
  - Verify flash address matches linker script
  - Re-download firmware file
  - Try slower programming speed
  - Test with different programmer

**Issue 5: Firmware Doesn't Run After Flash**
- **Symptoms:** Programming successful, but LED doesn't blink / no serial output
- **Causes:**
  - Wrong firmware for this board
  - Clock configuration incorrect
  - Peripheral initialization failure
- **Fixes:**
  - Verify correct firmware version
  - Check with debugger: set breakpoint in main()
  - Review serial output for error messages
  - Test with minimal "blink LED" firmware

**Pro Tip: Use Verbose Mode**
Most tools have verbose/debug output mode - enable it to see detailed logs when troubleshooting.''',
            'estimated_minutes': 15
        },
        {
            'title': 'Best Practices for Flight Software',
            'type': 'reading',
            'content': '''When flashing firmware for actual flight hardware, follow these best practices to avoid catastrophic failures.

**Pre-Flight Checklist:**
1. **Version Control:** Tag firmware version in Git before flashing
2. **Code Review:** Have another engineer review code changes
3. **Unit Tests:** Run all unit tests and verify 100% pass
4. **Static Analysis:** Use tools like cppcheck, Coverity to find bugs
5. **Hardware-in-Loop Testing:** Test on dev board first, then engineering model

**Flashing Procedure:**
1. **Backup:** Read and save existing flash contents before overwriting
2. **Document:** Log exactly what firmware version is flashed, when, and by whom
3. **Verify:** Always verify flash contents match binary file
4. **Functional Test:** Power cycle and verify basic functionality before closing up spacecraft

**Redundancy:**
- Flash redundant flight computers with identical firmware
- Keep spare programmed boards as backups
- Have rollback plan if new firmware fails in testing

**Change Management:**
Never flash flight hardware without:
- Written change request documenting what and why
- Approval from lead engineer or project manager
- Test results showing firmware passed qualification

**Post-Launch:**
Once in orbit, firmware updates must be:
- Thoroughly tested on ground replica ("flat-sat")
- Uploaded in small, verified packets
- Validated with CRC before bootloader accepts
- Reversible (keep previous firmware as backup)

**Horror Story Prevention:**
Real incident: Team flashed wrong firmware to flight computer, bricked it 2 weeks before launch. Lesson: ALWAYS label firmware files clearly and double-check before flashing.

**CADENCE Philosophy:**
"Measure twice, flash once" - take your time, verify everything, and never rush firmware updates on flight hardware.''',
            'estimated_minutes': 10
        },
        {
            'title': 'Knowledge Check',
            'type': 'quiz',
            'content': json.dumps({
                'questions': [
                    {
                        'question': 'What is the main difference between firmware and software?',
                        'options': [
                            'Firmware is always written in C, software in Python',
                            'Firmware directly controls hardware and persists in non-volatile memory',
                            'Software is faster than firmware',
                            'Firmware cannot be updated'
                        ],
                        'correct': 1,
                        'explanation': 'Firmware is low-level code that directly controls hardware and is stored in non-volatile memory like flash or ROM.'
                    },
                    {
                        'question': 'Which interface is most commonly used for flashing ARM Cortex-M flight computers?',
                        'options': [
                            'USB',
                            'Ethernet',
                            'SWD (Serial Wire Debug)',
                            'Bluetooth'
                        ],
                        'correct': 2,
                        'explanation': 'SWD is a 2-wire ARM-specific interface widely used for debugging and flashing ARM Cortex-M processors.'
                    },
                    {
                        'question': 'Why do CubeSats use bootloaders?',
                        'options': [
                            'To make the satellite boot faster',
                            'To enable remote firmware updates after launch',
                            'To reduce power consumption',
                            'To compress firmware files'
                        ],
                        'correct': 1,
                        'explanation': 'Bootloaders enable firmware updates via radio commands after the CubeSat is deployed, since physical access is impossible.'
                    },
                    {
                        'question': 'What should you ALWAYS do after flashing firmware?',
                        'options': [
                            'Immediately power off the board',
                            'Verify the flash contents match the binary file',
                            'Delete the firmware file',
                            'Flash it again to be sure'
                        ],
                        'correct': 1,
                        'explanation': 'Verification ensures the firmware was written correctly and matches the original binary - critical for mission success.'
                    },
                    {
                        'question': 'If you encounter "Cannot connect to target" when flashing, what is a likely cause?',
                        'options': [
                            'Wrong firmware file',
                            'Incorrect wiring of debug interface (SWDIO/SWCLK)',
                            'Firmware too large',
                            'Computer needs to be restarted'
                        ],
                        'correct': 1,
                        'explanation': 'Connection issues often stem from incorrect wiring of the debug interface or target not being powered.'
                    }
                ]
            }),
            'estimated_minutes': 6
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
    release_resource('alpha', 'modules/avionics/firmware_flashing',
                    f'Created Firmware Flashing module (ID {module_db_id}) with 8 sections',
                    {'module_db_id': module_db_id, 'sections': 8})

    print(f'\n[SUCCESS] Firmware Flashing module complete!')

except Exception as e:
    conn.rollback()
    print(f'[ERROR] {e}')
    import traceback
    traceback.print_exc()
finally:
    conn.close()
