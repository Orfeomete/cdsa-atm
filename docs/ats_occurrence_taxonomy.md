# Fifteen-Class ATS Occurrence Typology

CDSA-ATM uses a fifteen-class typology to classify Air Traffic
Service (ATS) occurrences: five classical operational classes
cross-aligned with EUROCONTROL ESARR 2 and ten cyber-safety
extension classes mapped to the MITRE ATT&CK framework.

## Classical Operational Classes (5)

| # | Class | ESARR 2 | Annex 11 | Doc 4444 |
|---|-------|---------|----------|----------|
| 1 | Loss of Separation (LOS) | A | ✓ | ✓ |
| 2 | Runway Incursion | A | ✓ | ✓ |
| 3 | Airspace Infringement | B | ✓ | ✓ |
| 4 | Frequency Congestion | C | ✓ | — |
| 5 | TCAS Resolution Advisory | A | ✓ | ✓ |

## Cyber-Safety Extension Classes (10)

| # | Class | ESARR 2 | MITRE ATT&CK |
|---|-------|---------|--------------|
| 6 | GNSS Spoofing | B | T1565 |
| 7 | GNSS Jamming | B | T1499 |
| 8 | ADS-B Injection | B | T1565.002 |
| 9 | Datalink Interruption | B | T1499 |
| 10 | Surveillance Data Loss | A | T1499 |
| 11 | ATM System Intrusion | A | T1190 |
| 12 | Voice Channel Spoofing | B | T1566 |
| 13 | NOTAM Tampering | B | T1565 |
| 14 | Time Synchronisation Attack | B | T1565 |
| 15 | Position Falsification | A | T1565 |

## Detailed Descriptions

### 1. Loss of Separation (LOS)
Violation of ICAO separation standards between two aircraft.
**Common scenarios:** TCAS RA triggering, controller error, weather
avoidance.

### 2. Runway Incursion
Unauthorised presence on a runway by aircraft, vehicle, or person.
Reference: ICAO Doc 9870 Manual on the Prevention of Runway
Incursions.

### 3. Airspace Infringement
Unauthorised entry into controlled airspace, often by general
aviation.

### 4. Frequency Congestion
Overload of a VHF frequency causing ATCO–pilot communication delay.

### 5. TCAS Resolution Advisory
Emergency resolution advisory issued by the collision avoidance
system.

### 6. GNSS Spoofing
Manipulation of aircraft position via fake GNSS signals.

### 7. GNSS Jamming
Artificial obstruction of GNSS signals causing position uncertainty.

### 8. ADS-B Injection
Fake ADS-B messages creating ghost aircraft on surveillance displays.

### 9. Datalink Interruption
Interruption of CPDLC datalink communication.

### 10. Surveillance Data Loss
Loss of radar or ADS-B surveillance feeds.

### 11. ATM System Intrusion
Unauthorised access to ATM centre systems (Exploit Public-Facing
Application).

### 12. Voice Channel Spoofing
Fake message broadcast on ATC voice frequency.

### 13. NOTAM Tampering
Forgery of NOTAM messages.

### 14. Time Synchronisation Attack
Disruption of system clock synchronisation, affecting surveillance
and datalink.

### 15. Position Falsification
Falsification of ADS-B or FMS position data.

## Severity Distribution (ESARR 2)

| Severity | Count | Proportion |
|----------|-------|------------|
| A (high) | 6 | 40% |
| B (medium) | 8 | 53% |
| C (low) | 1 | 7% |

## Cyber-Safety Coverage

Cyber-safety classes (10/15 = **67%** of the typology) reflect the
emerging threat landscape that exceeds classical ATM safety
literature. This is a key novel contribution of CDSA-ATM.
