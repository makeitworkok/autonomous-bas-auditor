# Project Overview

## What this project is
Autonomous BAS Auditor is an edge-to-cloud building automation audit system created for ClawComp.

It ingests BAS telemetry (BACnet/IP first), detects operational and energy inefficiencies, estimates potential financial impact, and surfaces likely incentive pathways.

## Problem statement
Most buildings have inefficiencies hidden in controls behavior. Manual audits are expensive, infrequent, and hard to scale.

## Proposed solution
- Collect BAS data from the building network at the edge
- Send structured payloads to a cloud API
- Normalize and tag points
- Run deterministic fault rules
- Estimate ROI and suggest incentive categories
- Orchestrate the full workflow through OpenClaw

## Current status snapshot
- Cloud API ingest path is running in Lightsail
- Bearer auth is enabled for ingest
- Raw payload storage is enabled
- Edge Collector Phase 2 MVP (fake payload + retry/spool) is implemented

## Scope (current)
- Single-site prototype workflow
- BACnet/IP first
- File-backed raw payload storage

## Scope (later)
- Multi-site support
- Advanced historical analytics
- Extended incentive data sources
- Production UI/reporting layer
