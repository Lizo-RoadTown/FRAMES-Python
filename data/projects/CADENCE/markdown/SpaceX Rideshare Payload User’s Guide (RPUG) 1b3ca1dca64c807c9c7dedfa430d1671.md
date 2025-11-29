# SpaceX Rideshare Payload User’s Guide (RPUG)

## **Section 5 Payload Design Requirements**

5.2.3 Cable Ties

- Flight cable ties must be non-removable, Nylon 6/6 or ETFE/Tefzel and must be vibration tested.

## **Section 6 Verification**

- Where possible, verification methods have been adapted from publicly-available standards such as SMC-S-016, GSFC-STD-7000 (GEVS), and other NASA/AIAA standards. More documentation for us to read and look into.

6.1 

- Testing must be performed at the fully integrated Payload assembly level, even if the Payload consists of multiple smaller Payload Constituents. Kind of obvious, but verification/testing must be done with a fully functional flight unit or prototype flight unit with respective payloads. This is all done for the safety of co-payloads (i.e. other people’s loads) and the launch vehicle.

6.1.2        

- For all Payloads, separation detection circuits must be functionally verified before and after dynamic tests to ensure that a Payload does not inadvertently activate during ascent. Additionally, the Customer must verify that any RF emissions or deployable systems are successfully inhibited while attached to the Launch Vehicle during random vibe testing, see Section 6.7.7. The satellite needs to have a circuit/switches that controls when the satellite electronics are activated/on. Must be off/inhibited during launch/ascent, as proven from before and after vibe testing results.

6.3 

- Workmanship sensitive joints (adhesive, epoxy, brazed, welded, etc.) require a retest if they are modified after testing. This also refers to Soldering connections, electrical connections.

6.5

![image.png](image%2095.png)

- Integrated Payload unit testing must conform to the parameters shown in Table 6-1. Fully containerized CubeSat [our Satellite may not qualify for fully containerized] levels are provided in Table 6-2.  The protoflight qualification approach is preferred by SpaceX.
- Focusing on the Power Inhibit EM Compatibility requirements. As stated previously power inhibit implementation is a MUST. As for EM Compatibility, (ADVISED) a dB range established by EMISM (Electromagnetic Interference Safety Margin) is applied to these parameters. Ref Section 6.7.7; Table 4-9; Table 6-1

6.7.7

- Evidence must be provided that shows no inadvertent power-ups and that isolated systems remain isolated during random vibe. This evidence could include, for example, boot logs or oscilloscope data. No power during vibe test to simulate launch/ascent.

IMPORTANT: In order to verify that power inhibit systems function as expected, all necessary power components MUST be fully integrated and in a flight-like state. Batteries must be in their flight-like charge state and any RBF/GSE inhibits must be removed. Verification testing must show that power to the Payload and secondary devices was successfully inhibited from a mechanical separation signal, and not because of other factors such as software delays. Physical mechanical inhibit controls required?

6.7.8

- Verification:  Testing or verification by analysis is ADVISED to the electromagnetic compatibility test levels and durations defined in Table 6-1 in accordance with the environments defined in Section 4.1.7.

Verification by test may be performed in-house per MIL-STD-461 with supporting test documentation or obtained from an IEC-17025 accredited (or equivalent) test facility. Verification by analysis must provide electromagnetic circuit and wiring emissions analysis.

## Section 7 Avionics and Electrical Interfaces

7.2 

- All deployment/separation devices directly interfacing with Launch Vehicle electrical systems must have sufficient reliability to ensure safe deployment. The preferred method of achieving reliability is two independent actuators on separate circuits. 2 separate actuators on separate circuits removes redundancy and increases reliability for payload separation.
- Each deployment command sent by the Launch Vehicle can be configured in one of two ways:
1. Constant-Current Pulse: Used for low-resistance loads, this mode of operation provides up to 6 A of constant current. Specifics of the pulse duration and current setting will be specified as part of the Payload-specific ICD. 
2. Bus-Voltage Pulse: Used for high-resistance or motor-driven loads, this mode of operation will provide an unregulated voltage signal with a bus voltage of 24-36 V with a maximum current draw of 6 A. Specifics of the voltage provided to the separation device and pulse duration will be specified as part of the Payload-specific ICD. 

7.3 

- A minimum of one (1) PL-side breakwire is recommended to be used for each deployment from the Launch Vehicle.
- It is acceptable for either loopback circuits or separation switches to be used for PL-side and LV-side breakwires. The final properties of the PL-side breakwire circuit(s), including the expected transition during deployment, will be captured as part of the Payload-specific ICD.

7.4 

![image.png](image%2096.png)

The table shows examples of umbilical channels to connect the payload/satellite to the Electrical Ground Station Equipment (EGSE). No AC signals must be transmitted through these umbilical channels. 

7.6 

- Electrical interfaces will not be available during SpaceX adapter mate, encapsulation, Launch Vehicle integration, and rollout operations. The Launch Vehicle does not provide power to Rideshare Payloads during Launch operations. All payload systems, including batteries, must be powered off during the Launch phase, except for portions of the circuit used to sense battery inhibits/isolation.

7.7

![image.png](image%2097.png)

Table 7-4 shows acceptable Electrical connections during specific phases and if they are provided by SpaceX.  

![image.png](image%2098.png)