#!/usr/bin/env python3
"""Create Sensor Driver Development Module - Complete"""

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
        # Create the module
        cur.execute('''
            INSERT INTO modules (
                module_id, title, description, category, estimated_minutes,
                status, target_audience, prerequisites, related_modules, tags,
                content_source, created_at, updated_at, published_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            'avionics_sensors_001',
            'Sensor Driver Development for CubeSats',
            'Learn to write robust, efficient sensor drivers for spacecraft avionics. Cover driver architecture, register mapping, calibration, error handling, and real-world integration of IMUs, magnetometers, and environmental sensors.',
            'avionics',
            90,
            'published',
            'Avionics engineers, embedded software developers',
            json.dumps(['avionics_i2c_spi_001', 'avionics_firmware_001']),
            json.dumps(['avionics_orientation_001']),
            json.dumps(['sensors', 'drivers', 'embedded software', 'IMU', 'magnetometer', 'avionics', 'I2C', 'calibration']),
            'CADENCE avionics documentation',
            datetime.now(),
            datetime.now(),
            datetime.now()
        ))

        module_db_id = cur.fetchone()[0]
        print(f'Module created with database ID: {module_db_id}')

        # Section 1: Driver Architecture
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            1,
            'Sensor Driver Architecture',
            'reading',
            '''# Sensor Driver Architecture for CubeSats

## What is a Sensor Driver?

A sensor driver is software that:
1. **Initializes** the sensor hardware
2. **Configures** sensor settings (range, resolution, sample rate)
3. **Reads** raw data from sensor registers
4. **Converts** raw data to engineering units
5. **Calibrates** measurements
6. **Handles errors** gracefully

## Why Good Drivers Matter in Space

In CADENCE CubeSats, sensor drivers must be:
- **Reliable**: No crashes from bad I2C transactions
- **Efficient**: Minimize power consumption
- **Deterministic**: Predictable timing for real-time systems
- **Testable**: Easy to validate on the ground

A bad driver can:
- Drain the battery (excessive polling)
- Crash the flight computer (unchecked errors)
- Provide incorrect data (bad calibration)
- Miss critical events (poor interrupt handling)

## Layered Driver Architecture

```
┌─────────────────────────────────────┐
│   Application Layer                 │
│   (Navigation, attitude control)    │
├─────────────────────────────────────┤
│   Sensor API Layer                  │
│   getAcceleration(), getMag(), etc  │
├─────────────────────────────────────┤
│   Hardware Abstraction Layer (HAL)  │
│   readRegister(), writeRegister()   │
├─────────────────────────────────────┤
│   Communication Protocol (I2C/SPI)  │
└─────────────────────────────────────┘
```

**Application Layer** calls high-level functions like `getAcceleration()` without knowing anything about registers.

**Sensor API Layer** implements sensor-specific logic (calibration, unit conversion).

**HAL** provides generic register read/write functions.

**Protocol Layer** handles the actual I2C or SPI transactions.

## Common Sensors in CADENCE

- **IMU (MPU-6050, LSM6DS3)**: 3-axis accelerometer + gyroscope
- **Magnetometer (LIS3MDL, HMC5883L)**: 3-axis magnetic field
- **Environmental (BMP280, BME680)**: Pressure, temperature, humidity
- **Star Tracker Camera**: Attitude determination
- **Solar Panels**: Current/voltage sensors for power

Each sensor type needs a driver!

## Key Design Principles

1. **Non-blocking I/O**: Never use `delay()` in a driver
2. **Error codes**: Return status codes, not exceptions
3. **Configurable**: Allow application to set ranges, rates
4. **Stateless where possible**: Minimize global variables
5. **Documented registers**: Comment every register address and bit field
''',
            900,
            datetime.now()
        ))

        # Section 2: Register Mapping and Datasheet Reading
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            2,
            'Reading Datasheets and Register Mapping',
            'reading',
            '''# Reading Datasheets and Register Mapping

## Anatomy of a Sensor Datasheet

Every sensor datasheet has these sections:
1. **Features** - Capabilities and specifications
2. **Electrical Characteristics** - Voltage, current, temperature range
3. **Pin Description** - SDA, SCL, VCC, GND, interrupt pins
4. **Register Map** - THE MOST IMPORTANT SECTION
5. **Application Notes** - Usage examples

## Example: MPU-6050 Register Map

From the MPU-6050 datasheet:

| Register | Address | Description | Access |
|----------|---------|-------------|--------|
| WHO_AM_I | 0x75    | Device ID (should return 0x68) | R |
| PWR_MGMT_1 | 0x6B  | Power management | R/W |
| ACCEL_XOUT_H | 0x3B | Accel X-axis high byte | R |
| ACCEL_XOUT_L | 0x3C | Accel X-axis low byte | R |
| GYRO_CONFIG | 0x1B | Gyro full scale select | R/W |
| ACCEL_CONFIG | 0x1C | Accel full scale select | R/W |

## How to Map Registers in Code

```cpp
// MPU-6050 Register Addresses
#define MPU6050_ADDR 0x68
#define MPU6050_WHO_AM_I 0x75
#define MPU6050_PWR_MGMT_1 0x6B
#define MPU6050_ACCEL_CONFIG 0x1C
#define MPU6050_GYRO_CONFIG 0x1B
#define MPU6050_ACCEL_XOUT_H 0x3B

// Power Management Bits
#define PWR_MGMT_1_RESET 0x80
#define PWR_MGMT_1_SLEEP 0x40

// Accelerometer Range Settings
#define ACCEL_RANGE_2G 0x00
#define ACCEL_RANGE_4G 0x08
#define ACCEL_RANGE_8G 0x10
#define ACCEL_RANGE_16G 0x18
```

**Always use #define, not magic numbers!**

## Bit Fields and Masks

Registers often contain multiple settings packed into one byte.

Example: ACCEL_CONFIG register (0x1C)
```
Bit 7-5: XA_ST, YA_ST, ZA_ST (self-test bits)
Bit 4-3: AFS_SEL (full scale range)
Bit 2-0: Reserved
```

To set range to +/-8g without changing other bits:
```cpp
uint8_t config = readRegister(MPU6050_ACCEL_CONFIG);
config &= 0xE7;  // Clear bits 4:3
config |= ACCEL_RANGE_8G;  // Set bits 4:3 to 10
writeRegister(MPU6050_ACCEL_CONFIG, config);
```

## Multi-Byte Registers

Sensor values are often 16-bit (two bytes):
```cpp
int16_t readAccelX() {
    uint8_t high = readRegister(MPU6050_ACCEL_XOUT_H);
    uint8_t low = readRegister(MPU6050_ACCEL_XOUT_L);
    return (int16_t)((high << 8) | low);
}
```

**Always read high byte first!** Some sensors latch the low byte when you read the high byte to prevent inconsistent readings.

## Datasheet Reading Checklist

When starting a new sensor driver:
- [ ] Find the default I2C/SPI address
- [ ] Identify the WHO_AM_I register (device ID)
- [ ] Map all configuration registers
- [ ] Map all data output registers
- [ ] Document all bit fields
- [ ] Note any special initialization sequences
- [ ] Check for errata (known bugs in the sensor)
''',
            1200,
            datetime.now()
        ))

        # Section 3: Initialization and Configuration
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            3,
            'Sensor Initialization and Configuration',
            'reading',
            '''# Sensor Initialization and Configuration

## The Initialization Sequence

Every sensor driver needs an `init()` function that:
1. Verifies the sensor is present (check WHO_AM_I)
2. Resets the sensor to known state
3. Configures measurement ranges
4. Sets sample rates and filters
5. Enables outputs
6. Returns success/failure status

## Example: MPU-6050 Initialization

```cpp
#include <Wire.h>

class MPU6050 {
public:
    enum AccelRange {
        RANGE_2G = 0,
        RANGE_4G = 1,
        RANGE_8G = 2,
        RANGE_16G = 3
    };

    bool init(AccelRange range = RANGE_2G) {
        // Step 1: Verify device ID
        uint8_t who_am_i = readRegister(MPU6050_WHO_AM_I);
        if (who_am_i != 0x68) {
            return false;  // Wrong device or not connected
        }

        // Step 2: Wake up sensor (default is sleep mode)
        writeRegister(MPU6050_PWR_MGMT_1, 0x00);
        delay(100);  // Wait for sensor to wake up

        // Step 3: Set accelerometer range
        setAccelRange(range);

        // Step 4: Set gyro range to +/-250 deg/s
        writeRegister(MPU6050_GYRO_CONFIG, 0x00);

        // Step 5: Configure low-pass filter (optional but recommended)
        writeRegister(MPU6050_CONFIG, 0x03);  // 44 Hz LPF

        return true;
    }

    void setAccelRange(AccelRange range) {
        uint8_t config = readRegister(MPU6050_ACCEL_CONFIG);
        config &= 0xE7;  // Clear bits 4:3
        config |= (range << 3);
        writeRegister(MPU6050_ACCEL_CONFIG, config);

        // Update scale factor for later conversions
        switch (range) {
            case RANGE_2G:  accel_scale = 16384.0; break;
            case RANGE_4G:  accel_scale = 8192.0; break;
            case RANGE_8G:  accel_scale = 4096.0; break;
            case RANGE_16G: accel_scale = 2048.0; break;
        }
    }

private:
    float accel_scale;

    uint8_t readRegister(uint8_t reg) {
        Wire.beginTransmission(MPU6050_ADDR);
        Wire.write(reg);
        Wire.endTransmission(false);
        Wire.requestFrom(MPU6050_ADDR, 1);
        return Wire.read();
    }

    void writeRegister(uint8_t reg, uint8_t value) {
        Wire.beginTransmission(MPU6050_ADDR);
        Wire.write(reg);
        Wire.write(value);
        Wire.endTransmission();
    }
};
```

## Configuration Best Practices

**For CADENCE CubeSats:**
- Use +/-2g or +/-4g for accelerometer (typical spacecraft acceleration is small)
- Use +/-250 deg/s for gyro (slow rotation in orbit)
- Enable low-pass filters to reduce noise
- Set sample rate to match control loop (typically 10-100 Hz)

**Power Considerations:**
- Higher sample rates = more power
- Disable axes you do not need
- Use interrupts instead of polling when possible

## Error Handling in Init

Always return a status code:
```cpp
enum SensorStatus {
    SENSOR_OK = 0,
    SENSOR_NOT_FOUND = 1,
    SENSOR_COMM_ERROR = 2,
    SENSOR_INIT_FAILED = 3
};
```

Application code can then handle failures gracefully:
```cpp
if (imu.init() != SENSOR_OK) {
    // Fallback: Use safe mode navigation
    // OR retry initialization
    // OR alert ground station
}
```
''',
            1200,
            datetime.now()
        ))

        # Section 4: Data Reading and Conversion
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            4,
            'Data Reading and Unit Conversion',
            'reading',
            '''# Data Reading and Unit Conversion

## Reading Sensor Data

Most sensors store data in 16-bit two's complement format across two registers (high byte and low byte).

## Example: Reading MPU-6050 Acceleration

```cpp
struct Vector3D {
    float x, y, z;
};

Vector3D getAcceleration() {
    Vector3D accel;

    // Read all 6 bytes at once (more efficient)
    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(MPU6050_ACCEL_XOUT_H);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU6050_ADDR, 6);

    int16_t raw_x = (Wire.read() << 8) | Wire.read();
    int16_t raw_y = (Wire.read() << 8) | Wire.read();
    int16_t raw_z = (Wire.read() << 8) | Wire.read();

    // Convert to g (gravitational acceleration)
    accel.x = raw_x / accel_scale;
    accel.y = raw_y / accel_scale;
    accel.z = raw_z / accel_scale;

    return accel;
}
```

## Understanding Scale Factors

The MPU-6050 datasheet specifies:
- +/-2g range: 16384 LSB/g
- +/-4g range: 8192 LSB/g
- +/-8g range: 4096 LSB/g
- +/-16g range: 2048 LSB/g

**LSB = Least Significant Bit (the raw integer value from the sensor)**

To convert raw value to physical units:
```
acceleration (g) = raw_value / LSB_per_g
```

## Two's Complement Conversion

16-bit two's complement range:
- Positive: 0 to 32767 (0x0000 to 0x7FFF)
- Negative: -32768 to -1 (0x8000 to 0xFFFF)

C/C++ `int16_t` handles this automatically:
```cpp
int16_t raw = (high_byte << 8) | low_byte;
// raw is already in correct signed format
```

## Efficiency: Burst Reads

Reading one byte at a time is slow. Most sensors support burst reads:

**Inefficient:**
```cpp
uint8_t ax_h = readRegister(0x3B);
uint8_t ax_l = readRegister(0x3C);
uint8_t ay_h = readRegister(0x3D);
uint8_t ay_l = readRegister(0x3E);
uint8_t az_h = readRegister(0x3F);
uint8_t az_l = readRegister(0x40);
// 6 separate I2C transactions
```

**Efficient:**
```cpp
Wire.requestFrom(MPU6050_ADDR, 6);  // Read 6 bytes starting at 0x3B
// 1 I2C transaction
```

This is 6x faster and uses less power!

## Unit Conversions Reference

| Sensor Type | Raw Data | Conversion | Output Unit |
|-------------|----------|------------|-------------|
| Accelerometer | LSB | raw / scale_factor | g or m/s² |
| Gyroscope | LSB | raw / scale_factor | deg/s or rad/s |
| Magnetometer | LSB | raw / scale_factor | gauss or µT |
| Pressure | LSB | (raw / scale) + offset | hPa or Pa |
| Temperature | LSB | (raw / scale) + offset | °C or K |

Always document your output units in comments!
''',
            1080,
            datetime.now()
        ))

        # Section 5: Hands-on Exercise
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            5,
            'Hands-On: Write a Complete IMU Driver',
            'exercise',
            '''# Exercise: Write a Complete MPU-6050 IMU Driver

## Objective

Implement a complete sensor driver for the MPU-6050 IMU with proper initialization, data reading, and error handling.

## Starter Code

```cpp
#include <Wire.h>

#define MPU6050_ADDR 0x68
#define MPU6050_WHO_AM_I 0x75
#define MPU6050_PWR_MGMT_1 0x6B
#define MPU6050_ACCEL_CONFIG 0x1C
#define MPU6050_ACCEL_XOUT_H 0x3B

class MPU6050_Driver {
public:
    struct IMU_Data {
        float accel_x, accel_y, accel_z;  // in g
        float gyro_x, gyro_y, gyro_z;     // in deg/s
    };

    bool init() {
        // TODO: Implement initialization
        // 1. Check WHO_AM_I (should be 0x68)
        // 2. Wake up sensor (write 0x00 to PWR_MGMT_1)
        // 3. Set accelerometer to +/-4g range
        // Return true if successful, false otherwise
        return false;  // Replace this
    }

    IMU_Data read() {
        // TODO: Implement data reading
        // 1. Read 14 bytes starting at 0x3B
        //    (accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z)
        // 2. Convert raw values to engineering units
        // 3. Return IMU_Data struct
        IMU_Data data = {0};
        return data;  // Replace this
    }

private:
    uint8_t readRegister(uint8_t reg) {
        Wire.beginTransmission(MPU6050_ADDR);
        Wire.write(reg);
        Wire.endTransmission(false);
        Wire.requestFrom(MPU6050_ADDR, 1);
        return Wire.read();
    }

    void writeRegister(uint8_t reg, uint8_t value) {
        Wire.beginTransmission(MPU6050_ADDR);
        Wire.write(reg);
        Wire.write(value);
        Wire.endTransmission();
    }
};

MPU6050_Driver imu;

void setup() {
    Serial.begin(9600);
    Wire.begin();

    if (imu.init()) {
        Serial.println("IMU initialized successfully");
    } else {
        Serial.println("IMU initialization failed");
    }
}

void loop() {
    auto data = imu.read();
    Serial.print("Accel: ");
    Serial.print(data.accel_x);
    Serial.print(", ");
    Serial.print(data.accel_y);
    Serial.print(", ");
    Serial.println(data.accel_z);
    delay(100);
}
```

## Requirements

1. **Initialization must:**
   - Verify WHO_AM_I register returns 0x68
   - Wake sensor from sleep mode
   - Configure accelerometer to +/-4g range (scale factor: 8192 LSB/g)
   - Configure gyroscope to +/-250 deg/s range (scale factor: 131 LSB/(deg/s))

2. **Data reading must:**
   - Use burst read (1 I2C transaction, not 14)
   - Convert raw int16 values to floats with correct units
   - Handle all 6 axes (3 accel + 3 gyro)

## Expected Output

When sitting still on a table, Z-axis acceleration should be approximately 1.0g (gravity). X and Y should be near 0.0g. All gyro axes should be near 0 deg/s.

```
IMU initialized successfully
Accel: 0.02, -0.01, 0.98
Accel: 0.01, -0.02, 1.00
Accel: 0.03, 0.00, 0.99
```

## Deliverable

Post your complete driver code and sensor output showing valid readings.
''',
            1800,
            datetime.now()
        ))

        # Section 6: Quiz
        cur.execute('''
            INSERT INTO module_sections (
                module_id, section_number, title, section_type, content,
                duration_seconds, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            module_db_id,
            6,
            'Knowledge Check: Sensor Drivers',
            'quiz',
            '''# Knowledge Check: Sensor Driver Development

## Question 1
What is the purpose of reading the WHO_AM_I register during initialization?
- A) To configure the sensor
- B) To verify the correct sensor is connected
- C) To wake up the sensor
- D) To read sensor data

**Answer: B** - WHO_AM_I returns a fixed device ID that lets you verify you are talking to the correct sensor.

## Question 2
The MPU-6050 accelerometer in +/-2g range has a scale factor of 16384 LSB/g. If you read a raw value of 8192, what is the acceleration?
- A) 0.5 g
- B) 1.0 g
- C) 2.0 g
- D) 8192 g

**Answer: A** - acceleration = 8192 / 16384 = 0.5 g

## Question 3
Why should sensor drivers use burst reads instead of reading one byte at a time?
- A) Burst reads are required by I2C protocol
- B) Burst reads are faster and use less power
- C) Burst reads provide more accurate data
- D) There is no difference

**Answer: B** - Burst reads complete in one I2C transaction instead of multiple, saving time and power.

## Question 4
A sensor's datasheet says a register uses "16-bit two's complement" format. The raw value is 0xFFFF. What is the signed integer value?
- A) 65535
- B) 0
- C) -1
- D) -65535

**Answer: C** - In two's complement, 0xFFFF represents -1.

## Question 5
Your sensor driver should use delay() during data reads to wait for sensor conversions. True or False?
- A) True - delays ensure accurate data
- B) False - use non-blocking status checks or interrupts

**Answer: B** - Blocking delays prevent the CPU from doing other work and violate real-time system requirements. Use status registers or interrupts instead.

## Question 6
You read the MPU-6050 Z-axis acceleration while the sensor is sitting still on a table. What value do you expect?
- A) 0 g (no movement)
- B) 1 g (sensing Earth's gravity)
- C) -1 g
- D) 9.8 g

**Answer: B** - The sensor measures proper acceleration, which includes gravity. A stationary sensor on Earth experiences 1g upward acceleration.
''',
            600,
            datetime.now()
        ))

        conn.commit()
        print(f'\nModule created successfully!')
        print(f'  Database ID: {module_db_id}')
        print(f'  Module ID: avionics_sensors_001')
        print(f'  Sections: 6 (4 reading, 1 exercise, 1 quiz)')
        print(f'  Total time: 90 minutes')

        return module_db_id

    except Exception as e:
        conn.rollback()
        print(f'Error: {e}')
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
