# trusted-notifications
 # 🛡️ Trusted Notification Engine (HDFC Bank Problem Statement)

A resilient, multi-channel notification ecosystem designed to solve **Delivery Failures** and **Phishing Risks** in banking alerts.

![Status](https://img.shields.io/badge/Status-Prototype-green) ![Stack](https://img.shields.io/badge/Tech-FastAPI%20%7C%20Celery%20%7C%20Redis-blue) ![Python](https://img.shields.io/badge/Language-Python_3.10+-yellow)

## 📌 The Problem
In today's digital banking ecosystem, two major gaps exist:
1.  **Reliability:** Critical OTPs and alerts often fail due to network congestion or carrier issues.
2.  **Trust:** Users cannot easily distinguish between a genuine bank SMS and a phishing attempt (spoofing).

## 💡 The Solution
I have built a **Centralized Notification Engine** that acts as a "Smart Brain" for all banking communications. It ensures:
* **Smart Fallback Logic:** If a Push Notification fails (or isn't acknowledged in 5s), the system automatically retries via SMS/Email.
* **Anti-Spoofing Protocol:** A cryptographic "Green Shield" verification ensures users only trust signed alerts.
* **High-Volume Simulation:** Capable of ingesting bulk event data (`events.csv`) to simulate real-world scale.

---

## 🏗️ How It Was Built (Architecture)

The system follows an **Event-Driven Microservices Architecture**:

1.  **API Layer (FastAPI):** Ingests requests from Core Banking and validates the payload.
2.  **Queue Management (Redis):** Acts as the message broker to decouple the API from the sending logic, ensuring no data loss during spikes.
3.  **Worker Nodes (Celery):** Background workers that handle the heavy lifting:
    * *Routing:* Decides the best channel (Push vs. SMS).
    * *Retries:* Handles the "Smart Fallback" logic if a channel fails.
4.  **Frontend (HTML/JS):** A Mobile Simulator that visualizes the "Trusted" vs. "Fraud" UI in real-time.

### 🛠️ Tech Stack
* **Backend:** Python (FastAPI)
* **Async Task Queue:** Celery
* **Message Broker:** Redis
* **Data Processing:** Pandas (for processing `events.csv` & `stats.csv`)
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js for analytics)

---

## 🧪 How to Evaluate & Run

Follow these steps to deploy the system locally on Windows/Linux.

### 1. Prerequisites
* Python 3.8+ installed.
* **Redis** installed and running (via Docker or Memurai for Windows).

### 2. Installation
```bash



