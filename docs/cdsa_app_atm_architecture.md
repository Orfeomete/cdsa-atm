# cdsa.app/atm Live Demonstration Platform Architecture

## Overview

The cdsa.app/atm platform provides a publicly accessible real-time
flow simulation that fuses OpenSky Network open ADS-B data with
synthetic ATS occurrence injection. The trained federated PPO
global policy performs real-time inference on this fused data
stream; every scenario referenced in the companion manuscript is
independently reproducible via `/reproduce/[scenario-id]` endpoints.

## Three-Layer Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 3 — Visualization (Frontend)                          │
│  - Leaflet.js 2D map (live aircraft positions)               │
│  - 15-class occurrence flag panel                            │
│  - KPI dashboard (aircraft count, occurrence rate)           │
│  - Live federated policy decision display                    │
├──────────────────────────────────────────────────────────────┤
│  Layer 2 — Inference (Backend)                               │
│  - Pre-trained MA-FedPPO global policy (PyTorch checkpoint)  │
│  - Real-time inference engine (FastAPI + WebSocket)          │
│  - /reproduce/[scenario-id] scenario player                  │
├──────────────────────────────────────────────────────────────┤
│  Layer 1 — Data (Ingestion)                                  │
│  - OpenSky Network REST API ingestion (10s refresh)          │
│  - Synthetic ATS occurrence injection engine                 │
│  - Timestamp-aligned fusion stream                           │
└──────────────────────────────────────────────────────────────┘
```

## Real-Time Components

| Component | Real-time? | Source |
|-----------|------------|--------|
| Open ADS-B data | **Live** | OpenSky Network |
| Synthetic ATS occurrence injection | **Live** | Local engine |
| 2D map aircraft positions | **Live** | Leaflet + WebSocket |
| 15-class occurrence panel | **Live** | Fusion layer |
| KPI dashboard | **Live** | Server-Sent Events |
| **MA-FedPPO global policy** | **Live inference** | Pre-trained checkpoint |
| KPI dashboard | **Live** | SSE push |
| **Federated training** | **Offline** | Pre-deployment |
| FedAvg vs FedProx comparison | **Static graph** | Offline result |

## Academic Honesty Note

The federated training itself is conducted offline. The resulting
global policy checkpoint is loaded into the live inference server.
This is the standard pattern for RL deployments — model training is
offline; real-time inference is online. This is explicitly stated
in the companion manuscript Section 4.3.

## Endpoints

### Public Live Endpoints
- `GET /atm` — Live simulation dashboard
- `GET /atm/api/v1/aircraft/live` — Current OpenSky aircraft snapshot
- `GET /atm/api/v1/occurrences/live` — Live synthetic occurrence stream

### Reproducibility Endpoints
- `GET /atm/reproduce/section-4-2` — Federated vs centralised comparison
- `GET /atm/reproduce/section-4-3` — Live simulation walkthrough
- `GET /atm/reproduce/[scenario-id]` — Generic scenario player

## Deployment

- **Backend**: Python FastAPI + Uvicorn
- **Frontend**: HTML + vanilla JavaScript + Leaflet.js
- **WebSocket**: Real-time data push
- **Hosting**: DigitalOcean droplet (1GB RAM, ~$6/month)
- **Domain**: cdsa.app (existing)
- **SSL**: Let's Encrypt (free)
- **Monitoring**: UptimeRobot

## Repository Connection

This platform's source code is included in the `src/` directory of
this repository. The pre-trained policy checkpoint will be released
via Zenodo in v1.1.
