# Cygnet Hardware/Software Plan

# Board to Board Communication

- [ ]  Cygnet Payload Computer transmits messages to FC Board v5b via UART0
- [ ]  Message from Payload Computer to FC Board v5b is sent to another FC Board via radio communication
- [ ]  Figure out why boards don’t communicate to each other during certain times

# Cosmic Watch Muon Detections

- [ ]  Initialize ADC on RP2040
- [ ]  Read values from ADC
- [ ]  Establish a baseline value from ADC as origin or “0”
- [ ]  Set a conversion rate between ADC values to Voltage values
    - Must be the reproduce the same waveform as seen on the oscilloscope
- [ ]  Set a trigger threshold for the software to know what level is a particle detection

# GPS & Other Sensors Data

- [ ]  Verify that GPS is using external antenna via protocol commands stated in the datasheet
    - It does say in the website that it automatically does switch over but just want to make sure
- [ ]  Ensure GPS is soldered correctly
- [ ]  Check for compatible Antennas
- [ ]  Change I2C Addresses of sensors