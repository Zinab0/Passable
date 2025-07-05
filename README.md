# Passable - An intelligent traffic light system with integrated incident detection and vehicle alerting

Passable is an intelligent traffic light system (ITLS) that uses real-time data collection and analysis, adaptive signal control, and vehicular communication to provide responsive actions for congestion and accidents. Salik dynamically adjusts traffic light timing using computer vision through Closed-circuit television (CCTV) cameras installed at intersections, and alerts drivers in case of congestion or accidents via wireless communication reducing wait times and enabling better driving decisions. The system includes incident detection using deep learning, green light calculation, wireless alerts, and a dashboard interface for monitoring the traffic flow by traffic department administrators.

---

## Implementation Overview

The project is organized into three main modules:

### 1. `AI Model`
Responsible for detecting the number of vehicles and identifying accidents from images using YOLOv8 AI model.

📁 **Folder:** `AI Model`

--

### 2. `Dashboard`
A web-based interface for monitoring live traffic status, alerts, and incident detection results built using Django & PowerBI.

📁 **Folder:** `traffic_light`

--

### 3. `Hardware Prototype`
Simulates a physical traffic light intersection, including traffic signals and the alert communication system built using Arduino.

📁 **Folder:** `Hardware`

------------------------------------------
## System Architecture

![fremwork-min](https://github.com/user-attachments/assets/3b255073-e1a8-41d0-ae02-eaa0fd0c4b70)


---

## Demo

### `AI Model`

* Accident detection

<img width="428" alt="Accident detection" src="https://github.com/user-attachments/assets/1ea4bfd5-4a76-4dda-9b42-8d2021a7073f" />
  
* vehicles detection

<img width="428" alt="vehicles detection" src="https://github.com/user-attachments/assets/2c25609d-5a8d-46fb-a32a-5aa00d8b8d41" />

### `Dashboard`

* Login page

<img width="664" alt="login page" src="https://github.com/user-attachments/assets/b6291262-cfc5-45bb-a0e4-3bfd49b33269" />

* Dashboard

<img width="664" alt="login page" src="https://github.com/user-attachments/assets/87a264f4-05e6-4c17-8ea1-957a6ffeb2a7"/>


### `Hardware Prototype`
<img width="664" alt="INTERSECTIONPROTOTYPE" src="https://github.com/user-attachments/assets/1b04553d-3ded-430e-9312-3af9e730cf6e" />


------------------------------------------



