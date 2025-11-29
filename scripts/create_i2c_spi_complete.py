#!/usr/bin/env python3
"""Create I2C/SPI Communication Protocols Module - Complete"""

import os
import psycopg2
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def main():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    try:
        # Step 1: Create the module
        cur.execute('''
            INSERT INTO modules (
                module_id, title, description, category, estimated_minutes,
                status, target_audience, prerequisites, related_modules, tags,
                content_source, created_at, updated_at, published_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            'avionics_i2c_spi_001',
            'I2C and SPI Communication Protocols',
            'Master the two most common serial communication protocols used in CubeSat avionics: I2C and SPI. Learn protocol fundamentals, practical implementation, debugging techniques, and real-world applications.',
            'avionics',
            75,
            'published',
            'Avionics engineers, embedded systems developers',
            json.dumps(['avionics_orientation_001']),
            json.dumps(['avionics_firmware_001']),
            json.dumps(['I2C', 'SPI', 'serial communication', 'embedded systems', 'sensors', 'avionics']),
            'CADENCE avionics documentation',
            datetime.now(),
            datetime.now(),
            datetime.now()
        ))

        module_db_id = cur.fetchone()[0]
        print(f'Module created with database ID: {module_db_id}')

        # Step 2: Add Section 1
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            1,
            'Introduction to Serial Communication',
            'reading',
            '''# Introduction to Serial Communication in CubeSats

## Why Serial Protocols Matter

In CubeSat avionics, you will work with dozens of components that need to talk to each other: sensors, memory chips, ADCs, real-time clocks, and more. Serial communication protocols like I2C and SPI are the languages these components speak.

## The Challenge

Parallel communication (sending multiple bits simultaneously) requires many wires and is not practical in space-constrained CubeSats. Serial protocols solve this by sending data one bit at a time over fewer wires, saving mass, power, and PCB space.

## I2C vs SPI: Quick Comparison

**I2C (Inter-Integrated Circuit):**
- 2 wires (SDA for data, SCL for clock)
- Multiple devices on same bus (up to 127 addresses)
- Slower (standard: 100 kHz, fast: 400 kHz, high-speed: 3.4 MHz)
- Built-in addressing and ACK/NACK
- Great for: Sensors, EEPROMs, RTCs

**SPI (Serial Peripheral Interface):**
- 4+ wires (MOSI, MISO, SCK, CS)
- Faster (can exceed 10 MHz)
- One chip select per device
- No built-in acknowledgment
- Great for: Flash memory, ADCs, displays, SD cards

## In CADENCE Missions

You will use both protocols extensively:
- **I2C**: Temperature sensors, magnetometers, gyroscopes
- **SPI**: Flash memory for data storage, high-speed ADCs

Ready to dive deep into each protocol!
''',
            600,
            datetime.now()
        ))

        # Step 3: Add Section 2
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            2,
            'I2C Protocol Deep Dive',
            'reading',
            '''# I2C (Inter-Integrated Circuit) Protocol

## Physical Layer

Two wires, pull-up resistors required:
- **SDA** (Serial Data): Bidirectional data line
- **SCL** (Serial Clock): Clock signal from master

Both lines require pull-up resistors (typically 2.2k to 10k ohms).

## How I2C Works

### 1. Start Condition
Master pulls SDA low while SCL is high

### 2. Address Frame
Master sends 7-bit device address + R/W bit
- Example: 0x68 for write, 0x69 for read
- 7-bit address allows up to 127 devices on one bus

### 3. Acknowledgment (ACK)
After each byte, the receiver pulls SDA low to acknowledge receipt

### 4. Data Transfer
Data is sent in 8-bit bytes, MSB (Most Significant Bit) first

### 5. Stop Condition
Master releases SDA (allowing it to go high) while SCL is high

## Common Sensor Addresses in CADENCE

- **MPU-6050 (IMU):** 0x68 or 0x69
- **BMP280 (Pressure):** 0x76 or 0x77
- **BME680 (Environmental):** 0x76 or 0x77
- **LIS3MDL (Magnetometer):** 0x1C or 0x1E

## Pull-up Resistor Calculation

Formula: R = (VCC - 0.4V) / (3mA × number_of_devices)

For 3.3V bus with 3 devices:
R = (3.3V - 0.4V) / (3mA × 3) = 320 ohms minimum

Typical safe values: 2.2k to 10k ohms

## Bus Speed Options

- **Standard Mode:** 100 kHz (most common)
- **Fast Mode:** 400 kHz (modern sensors)
- **High-Speed Mode:** 3.4 MHz (rare in CubeSats)

In CADENCE missions, we typically use Fast Mode (400 kHz) for balance between speed and reliability.

## Multi-Master Support

I2C supports multiple masters through:
- **Clock Stretching:** Slave can hold SCL low to pause master
- **Arbitration:** If two masters transmit simultaneously, conflicts are detected

In CADENCE, we typically use single-master architecture (flight computer controls all sensors).
''',
            900,
            datetime.now()
        ))

        # Step 4: Add Section 3
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            3,
            'SPI Protocol Deep Dive',
            'reading',
            '''# SPI (Serial Peripheral Interface) Protocol

## Physical Layer

SPI requires four wires minimum:
- **MOSI** (Master Out Slave In): Data from master to slave
- **MISO** (Master In Slave Out): Data from slave to master
- **SCK** (Serial Clock): Clock signal from master
- **CS** or **SS** (Chip Select / Slave Select): Selects which device to communicate with

For multiple slaves, you need one CS line per device.

## SPI Modes: Clock Polarity and Phase

SPI has 4 modes defined by CPOL (Clock Polarity) and CPHA (Clock Phase):

| Mode | CPOL | CPHA | Clock Idle State | Data Sampled On |
|------|------|------|------------------|-----------------|
| 0    | 0    | 0    | Low              | Rising edge     |
| 1    | 0    | 1    | Low              | Falling edge    |
| 2    | 1    | 0    | High             | Falling edge    |
| 3    | 1    | 1    | High             | Rising edge     |

**Always check your device datasheet for the correct mode!** Most flash memory uses Mode 0 or Mode 3.

## Full-Duplex Communication

Unlike I2C (half-duplex), SPI can transmit and receive simultaneously. Every time you send a byte, you also receive a byte.

This is important: even if you only want to read, you must send dummy bytes. Even if you only want to write, you will receive bytes (usually ignored).

## Multi-Slave Configuration

**Option 1: Individual CS lines (standard)**
- Each slave has its own dedicated CS line
- Only one slave can be selected at a time
- Most flexible and common approach

**Option 2: Daisy Chain**
- Slaves connected in series
- Data passes through all slaves
- Used for LED drivers, shift registers
- Rare in CubeSat applications

## Speed and Timing

SPI can be very fast:
- **Typical CubeSat speed:** 1-4 MHz
- **Maximum speed:** 10+ MHz (with careful PCB design)

Speed limitations:
- PCB trace length (keep traces short and matched!)
- Capacitance on the bus
- Slave device maximum speed
- EMI/noise considerations in space environment

## When to Use SPI vs I2C

**Use SPI for:**
- High-speed data transfer (flash memory, ADCs)
- Simple point-to-point communication
- Applications requiring full-duplex
- When you have spare GPIO pins

**Use I2C for:**
- Many devices on one bus (saves pins)
- Lower-speed sensors
- When pull-up resistors are acceptable
- Standardized sensor ecosystem
''',
            1200,
            datetime.now()
        ))

        # Step 5: Add Section 4 - Practical I2C Exercise
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            4,
            'Practical Exercise: I2C Scanner',
            'exercise',
            '''# Exercise: Build an I2C Bus Scanner

## Objective

Write code to scan the I2C bus and detect all connected devices. This is an essential debugging tool for avionics work.

## The Code

```cpp
#include <Wire.h>

void setup() {
    Serial.begin(9600);
    Wire.begin();  // Initialize I2C as master

    Serial.println("I2C Bus Scanner");
    Serial.println("Scanning...");

    uint8_t devices_found = 0;

    for (uint8_t address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        uint8_t error = Wire.endTransmission();

        if (error == 0) {
            Serial.print("Device found at 0x");
            if (address < 16) Serial.print("0");
            Serial.println(address, HEX);
            devices_found++;
        }
    }

    Serial.print("Scan complete. Found ");
    Serial.print(devices_found);
    Serial.println(" device(s).");
}

void loop() {
    // Nothing here
}
```

## What to Test

1. Connect an I2C sensor (like BMP280 or MPU-6050) to your development board
2. Run the scanner
3. Note the detected address(es)
4. Compare with the sensor datasheet

## Common Addresses to Look For

- 0x68, 0x69: MPU-6050 IMU
- 0x76, 0x77: BMP280 pressure sensor
- 0x1C, 0x1E: LIS3MDL magnetometer

## Troubleshooting

**No devices found?**
- Check your wiring (SDA, SCL, VCC, GND)
- Verify pull-up resistors are present (2.2k-10k ohms)
- Check sensor power supply voltage (3.3V or 5V?)

**Multiple devices with same address?**
- Some sensors have address select pins (AD0, SDO)
- Change the address by connecting the pin to VCC or GND

## Deliverable

Post your I2C scanner output showing at least one detected device.
''',
            900,
            datetime.now()
        ))

        # Step 6: Add Quiz Section
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            5,
            'Knowledge Check: I2C and SPI',
            'quiz',
            '''# Knowledge Check: I2C and SPI Protocols

## Question 1
How many wires does I2C require (minimum)?
- A) 1 wire
- B) 2 wires (SDA, SCL)
- C) 3 wires
- D) 4 wires

**Answer: B**

## Question 2
What is the purpose of pull-up resistors on I2C lines?
- A) Increase signal strength
- B) Allow multiple devices to release the bus (open-drain)
- C) Reduce power consumption
- D) Filter noise

**Answer: B** - I2C uses open-drain outputs, so pull-up resistors are needed to pull the lines high when no device is driving them low.

## Question 3
In SPI, what does MOSI stand for?
- A) Master Output Slave Input
- B) Master Out Slave In
- C) Multiple Output Single Input
- D) Master Only Slave Isolated

**Answer: B** - Master Out Slave In (data from master to slave)

## Question 4
Which protocol can communicate with more devices using fewer wires?
- A) SPI (uses addressing)
- B) I2C (can address up to 127 devices on 2 wires)
- C) Both are equivalent
- D) Neither supports multiple devices

**Answer: B** - I2C can have up to 127 devices on just 2 wires. SPI needs a separate CS line for each device.

## Question 5
A BMP280 sensor datasheet specifies "I2C Fast Mode." What speed does this indicate?
- A) 100 kHz
- B) 400 kHz
- C) 1 MHz
- D) 3.4 MHz

**Answer: B** - Fast Mode is 400 kHz. Standard Mode is 100 kHz, and High-Speed Mode is 3.4 MHz.

## Question 6
You are selecting between I2C and SPI for a high-speed data logger that will write to flash memory at 8 MB/s. Which protocol should you choose?
- A) I2C (simpler, fewer wires)
- B) SPI (faster, can exceed 10 MHz clock)
- C) Either works equally well
- D) Neither can support 8 MB/s

**Answer: B** - SPI is much faster and commonly used for flash memory. I2C typically maxes out around 400 kHz (50 KB/s), far too slow for this application.

## Question 7
In your CubeSat, you have 5 sensors that all use I2C address 0x76. How can you use all 5 sensors?
- A) Connect them all to the same bus (they will work)
- B) Use an I2C multiplexer (e.g., TCA9548A) to select one at a time
- C) Change the I2C protocol to allow duplicate addresses
- D) You must replace the sensors with different models

**Answer: B** - An I2C multiplexer allows you to switch between multiple devices with the same address by selecting different bus channels.

## Question 8
You are debugging an SPI flash chip that is not responding. The CS line is held LOW continuously. What is likely wrong?
- A) Correct - CS should be LOW during communication
- B) CS should idle HIGH and only go LOW when you want to communicate
- C) CS polarity does not matter for SPI
- D) CS is not used in SPI

**Answer: B** - Chip Select should idle HIGH and only go LOW when you are actively communicating with that specific device.
''',
            600,
            datetime.now()
        ))

        conn.commit()
        print(f'\nModule created successfully!')
        print(f'  Database ID: {module_db_id}')
        print(f'  Module ID: avionics_i2c_spi_001')
        print(f'  Sections: 5 (3 reading, 1 exercise, 1 quiz)')
        print(f'  Total time: 75 minutes')

        return module_db_id

    except Exception as e:
        conn.rollback()
        print(f'Error: {e}')
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
