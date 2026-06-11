# ADS-B and Synthetic Occurrence Fusion Design

## Motivation

Air Traffic Management research faces a structural asymmetry:
- **Aircraft state data** (position, speed, altitude) is publicly
  available via ADS-B sources such as the OpenSky Network.
- **ATS occurrence data** (Loss of Separation, ATCO workload, cyber-
  safety incidents) remains locked in ANSPs' local records due to
  national sovereignty, competitive positioning, and regulatory
  data-protection obligations.

CDSA-ATM bridges this asymmetry through **real-time fusion**: open
ADS-B streams are combined with synthetically injected ATS
occurrences parameterised over a fifteen-class typology.

## Data Source: OpenSky Network

**Source:** [https://opensky-network.org](https://opensky-network.org)
**Coverage:** ~15,000 aircraft in real time, ~90% European airspace
sensor coverage.
**Refresh rate:** 10–15 seconds.
**Licence:** Free for academic use.

OpenSky Python client: `opensky-api`. REST API also available.

## Synthetic Occurrence Injection

The synthetic engine generates occurrences according to the 15-class
typology (see `ats_occurrence_taxonomy.md`).

**Engine properties:**
- Deterministic template-based generation
- Byte-reproducible (fixed random seed)
- Parameters derived from ESARR 2 statistical averages
- Optionally country-specific distributions (DHMİ, DFS, ENAIRE)

## Fusion Pipeline

```
┌─────────────────────┐    ┌──────────────────────┐
│  OpenSky Network    │    │  Synthetic ATS       │
│  REST API           │    │  Occurrence Engine   │
│  (10s refresh)      │    │  (parameter file)    │
└──────────┬──────────┘    └──────────┬───────────┘
           │                          │
           └──────────┬───────────────┘
                      ▼
              ┌───────────────┐
              │  Fusion       │
              │  Layer        │
              │  (timestamp   │
              │   alignment)  │
              └───────┬───────┘
                      ▼
       ┌──────────────────────────────┐
       │  Federated PPO Observation   │
       │  Space                       │
       │   - aircraft density (open)  │
       │   - occurrence flags (synth) │
       │   - cyber alerts (synth)     │
       └──────────────────────────────┘
```

## Privacy Guarantee

The fusion architecture **eliminates the need to access local ATS
occurrence records held by ANSPs**. Synthetic injection is performed
locally at each federated client; only model gradients are shared
with the federated coordinator.

This design respects EU Regulation 2017/373 ATM/ANS Common
Requirements and EUROCONTROL ESARR 2 reporting structures while
preserving operational data sovereignty.
