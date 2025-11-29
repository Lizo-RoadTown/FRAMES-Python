#!/usr/bin/env python3
"""
Create I2C/SPI Communication Protocols Module
Agent Alpha - Avionics Module Creation
"""

import os
import psycopg2
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_i2c_spi_module():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    try:
        # Create the I2C/SPI module
        module_data = {
            'module_id': 'avionics_i2c_spi_001',
            'title': 'I2C and SPI Communication Protocols',
            'description': 'Master the two most common serial communication protocols used in CubeSat avionics: I2C (Inter-Integrated Circuit) and SPI (Serial Peripheral Interface). Learn protocol fundamentals, practical implementation, debugging techniques, and real-world applications in satellite systems.',
            'category': 'avionics',
            'estimated_minutes': 75,
            'status': 'published',
            'target_audience': 'Avionics engineers, embedded systems developers',
            'prerequisites': json.dumps(['avionics_orientation_001']),
            'related_modules': json.dumps(['avionics_firmware_001', 'avionics_sensors_001']),
            'tags': json.dumps(['I2C', 'SPI', 'serial communication', 'embedded systems', 'sensors', 'protocol', 'avionics', 'bus', 'debugging']),
            'content_source': 'CADENCE avionics documentation'
        }

        cur.execute('''
            INSERT INTO modules (
                module_id, title, description, category, estimated_minutes,
                status, target_audience, prerequisites, related_modules, tags,
                content_source, created_at, updated_at, published_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            module_data['module_id'],
            module_data['title'],
            module_data['description'],
            module_data['category'],
            module_data['estimated_minutes'],
            module_data['status'],
            module_data['target_audience'],
            module_data['prerequisites'],
            module_data['related_modules'],
            module_data['tags'],
            module_data['content_source'],
            datetime.now(),
            datetime.now(),
            datetime.now()
        ))

        module_id = cur.fetchone()[0]
        print(f'Module created with ID: {module_id}')

        # Create module sections
        sections = [
            {
                'section_number': 1,
                'title': 'Introduction to Serial Communication',
                'content_type': 'reading',
                'content': '''# Introduction to Serial Communication in CubeSats

## Why Serial Protocols Matter

In CubeSat avionics, you'll work with dozens of components that need to talk to each other: sensors, memory chips, ADCs, real-time clocks, and more. Serial communication protocols like I2C and SPI are the languages these components speak.

## The Challenge

Parallel communication (sending multiple bits simultaneously) requires many wires and isn't practical in space-constrained CubeSats. Serial protocols solve this by sending data one bit at a time over fewer wires, saving mass, power, and PCB space.

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

You'll use both protocols extensively:
- **I2C**: Temperature sensors, magnetometers, gyroscopes
- **SPI**: Flash memory for data storage, high-speed ADCs

Ready to dive deep into each protocol!
''',
                'estimated_minutes': 10
            },
            {
                'section_number': 2,
                'title': 'I2C Protocol Deep Dive',
                'content_type': 'reading',
                'content': '''# I2C (Inter-Integrated Circuit) Protocol

## Physical Layer

Two wires, pull-up resistors required:
- SDA (Serial Data)
- SCL (Serial Clock)

## How I2C Works

### 1. Start Condition
Master pulls SDA low while SCL is high

### 2. Address Frame
Master sends 7-bit address + R/W bit
- Example: 0x68 << 1 | 0 for write to device 0x68

### 3. Acknowledgment
Slave pulls SDA low after each byte

### 4. Data Transfer
8-bit bytes, MSB first

### 5. Stop Condition
SDA rises while SCL is high

## Addressing

**7-bit address space:** 0x00 to 0x7F (127 devices max)

Common sensor addresses in CADENCE:
- MPU-6050 (IMU): 0x68 or 0x69
- BMP280 (Pressure): 0x76 or 0x77
- BME680 (Environmental): 0x76 or 0x77

## Pull-up Resistor Calculation

Formula: R = (VCC - 0.4V) / (3mA × number_of_devices)

For 3.3V bus with 3 devices:
R = (3.3V - 0.4V) / (3mA × 3) = 320Ω minimum

Typical values: 2.2kΩ to 10kΩ

## Multi-Master Scenarios

I2C supports multiple masters through clock stretching and arbitration. In CADENCE, typically one master (flight computer) controls all sensors.
''',
                'estimated_minutes': 15
            },
            {
                'section_number': 3,
                'title': 'SPI Protocol Deep Dive',
                'content_type': 'reading',
                'content': '''# SPI (Serial Peripheral Interface) Protocol

## Physical Layer

Four wires minimum:
- MOSI (Master Out Slave In)
- MISO (Master In Slave Out)
- SCK (Serial Clock)
- CS (Chip Select)

## SPI Modes (Clock Polarity & Phase)

| Mode | CPOL | CPHA | Clock Idle | Data Capture |
|------|------|------|------------|--------------|
| 0    | 0    | 0    | Low        | Rising edge  |
| 1    | 0    | 1    | Low        | Falling edge |
| 2    | 1    | 0    | High       | Falling edge |
| 3    | 1    | 1    | High       | Rising edge  |

**Always check your device datasheet!**

## Full-Duplex Communication

Unlike I2C, SPI can send and receive simultaneously. Every time you write a byte, you also read a byte.

## Multi-Slave Configuration

**Option 1: Individual CS lines (preferred)**
Each slave has its own chip select line.

**Option 2: Daisy chain (rare)**
Used for specific applications like LED drivers.

## Speed Considerations

SPI clock can be very fast (10+ MHz), but:
- PCB trace length matters (keep short!)
- Decoupling capacitors essential
- Ground plane critical

CADENCE missions: Typically 1-4 MHz for robustness
''',
                'estimated_minutes': 15
            }
        ]

        # Insert all sections
        for section in sections:
            cur.execute('''
                INSERT INTO module_sections (
                    module_id, section_number, title, content_type, content,
                    estimated_minutes, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                module_id,
                section['section_number'],
                section['title'],
                section['content_type'],
                section['content'],
                section['estimated_minutes'],
                datetime.now()
            ))

        conn.commit()
        print(f'Created {len(sections)} sections for module {module_id}')
        print(f'Module "{module_data["title"]}" published successfully!')

        return module_id

    except Exception as e:
        conn.rollback()
        print(f'Error creating module: {e}')
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    module_id = create_i2c_spi_module()
    print(f'\nModule ID: {module_id}')
    print('Total estimated time: 75 minutes')
    print('Sections: 3 (reading)')
