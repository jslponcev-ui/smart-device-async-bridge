# Smart Device Async Bridge 🌉⚡

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An asynchronous event-driven Python library designed to bridge raw hardware protocol telemetry (UART/Serial) into structured, validated data payloads for home automation and IoT ecosystems.

---

## 🎯 Key Features

- **Non-blocking Asynchronous I/O:** Built on top of Python's `asyncio` loop for high-throughput telemetry ingestion.
- **Strict Data Validation:** Utilizes `Pydantic v2` to parse, validate, and enforce type safety on incoming hardware data.
- **Event-Driven Architecture:** Decoupled observer pattern allowing multiple downstream application entities to subscribe to telemetry events.
- **Graceful Resource Shutdown:** Handles task cancellation cleanly, ensuring hardware interfaces close gracefully.

---

## 🏗️ Architecture Overview

```text
[ Physical Peripheral / Serial Driver ]
               │
               ▼ (Async Stream Generator)
     [ AsyncDeviceBridge ]
               │
      (Validation & Parsing)
               ▼
   [ Event Subscribers / Callbacks ]