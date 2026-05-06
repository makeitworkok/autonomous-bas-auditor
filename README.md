# Autonomous BAS Auditor

An edge-to-cloud system that ingests building automation data (BACnet/Modbus), identifies the top operational and energy inefficiencies, and generates a financial audit with actionable recommendations.

## Architecture

- Edge collector (Raspberry Pi) performs BACnet discovery
- Data is sent to a cloud API
- Audit engine detects faults and estimates ROI
- OpenClaw agent orchestrates the audit workflow

## Goals

- Automate building system diagnostics
- Quantify energy waste
- Generate actionable, financially justified recommendations

## Status

Early prototype (ClawComp build)

## Documentation

- Full docs package: [docs/README.md](docs/README.md)
- ClawComp notes: [docs/clawcomp-submission-notes.md](docs/clawcomp-submission-notes.md)
