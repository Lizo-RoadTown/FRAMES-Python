# Orbit Simulations #1 - Targetting SMA

Notes: Ran altitudes 220 - 450
Person: Jordy Samaniego

| **Updates** | **Notes** |  |
| --- | --- | --- |
| Simulation Running | Ran at 10:48AM 09/16 |  |
|  |  |  |

<aside>
💡

Initial SMA data collection for identifying optimal orbital parameters

</aside>

**Simulation Setup:**

<aside>
💡

All values are set to be the same with only SMA differing as to see the affects of the changes of SAA

**Initial hypothesis:**

The effect will not be as significant as the change in INC and RAAN will give as we are working in LEO with a circular orbit

</aside>

- Outer Region:
    
    These values fully contain the SAA 
    
    - MinLat = -70
    - MaxLat = 30
    - MinLon = -150
    - MaxLon = 60
- Set SMA intervals targeting SAA altitudes of 200 - 800 km
    - intervals of 50 km will be used
    - Reminder: altitude = SMA - R_e
        - R_e = radius of earth = 6371 (avg radius of earth)
    - SMA(1) = 6591.13
        - alt = 220.13
            - started at 220 because of errors with JacchiaRoberts model
                - **note:** that altitudes lower than this were giving model errors
    - SMA(2) = 6621.13
        - 250.13
    - SMA(3) = 6671.13
        - 300.13
    - SMA(4) = 6721.13
        - 350.13
    - SMA(5) = 6771.13
        - 400.13
    - SMA(6) = 6821.13
        - 450.13
- All Inclination values were set to the center latitude of the SAA
    - INC = 22
    - Note:
        - this might not get full access of the SAA, only to center mass of the region
- All ecc values were set to the same value
    - ECC = 0.0001
        - showing an essentially circular orbit
        - did not make it 0 because 0 can be too idealistic
- RAAN
    - set to 130 for all values
    - this targets the longitude of 50 degrees West of the SAA
        - 130 + 180 = 310 → 50 deg W