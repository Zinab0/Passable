# Salik - Smart traffic light management system
![Salik logo](https://github.com/user-attachments/assets/550b496f-fe23-48c5-bdfd-3cde4706bc30)

Traffic management systems are vital infrastructures in modern cities that playa crucial role in ensuring the safety of road users, reducing congestion, and maintaining smooth traffic flow. However, with the growth of urban populations and vehicle ownership rates, managing traffic efficiently has become increasingly challenging. 

Traditional Traffic light systems rely on fixed-time cycles, which do not take into consideration the current status of congestion and the presence of any incidents on the roads. Therefore, intelligent transportation systems that use real-time data collection and analysis, adaptive signal control, and vehicular communication have emerged as a new paradigm in smart cities. 

These systems help in enabling safe driving, intelligent navigation, and timely emergency response. Most of the proposed solutions for adaptive traffic light control focus only onetype of road incidents, either congestion or accidents. Furthermore, drivers, uninformed about road conditions, often become confused, potentially disrupting traffic flow. 

To address these limitations of current traffic control systems, our proposed system, Salik, provides real-time detection and responsive actions for congestion and accidents. Salik utilizes computer vision via Closed-circuit television (CCTV) cameras installed at traffic lights to dynamically adjust traffic light timing. It overrides the green light timer and alerts drivers in the event of congestion or accidents. Thus, it aids in reducing drivers’ wait times at traffic lights and provides them with information to make better driving decisions, such as changing lanes or adjusting their speed, to prevent accidents. Salik has three phases: detection of road incidents from images using deep learning, calculating green light time, and alerting vehicles via wireless communication about the detected road incident. Salik also provides a dashboard interface for administrators at the traffic department, which presents the status and statistics about the monitored intersections. This interface includes information about accidents and congested areas. The provision of such information facilitates decision-making and enables the authorities to monitor Salik’s positive impact.

------------------------------------------
### Implementation Details

This project can be broken down into 3 modules:

1. `AI Model` - This module is responsible for detecting the number of vehicles in the image received as input from the camera. More specifically, it will provide as output the number of vehicles and if there is an accident detected.

2. `Dashboard` - Dashboard interface provides a comprehensive overview of the traffic condition status.

3. `Hardware Prototype` - A simulation of traffic light intersection to simulate traffic signals and the alert system.
------------------------------------------
### Demo

* `AI Model`
  
Accident detection

<img width="437" alt="Accident detection" src="https://github.com/user-attachments/assets/1ea4bfd5-4a76-4dda-9b42-8d2021a7073f" />
  
vehicles detection

<img width="428" alt="vehicles detection" src="https://github.com/user-attachments/assets/2c25609d-5a8d-46fb-a32a-5aa00d8b8d41" />

* `Dashboard`

Login page

<img width="1102" alt="login page" src="https://github.com/user-attachments/assets/b6291262-cfc5-45bb-a0e4-3bfd49b33269" />

Dashboard

![Dashboard](https://github.com/user-attachments/assets/87a264f4-05e6-4c17-8ea1-957a6ffeb2a7)


* `Hardware Prototype`

<img width="664" alt="INTERSECTIONPROTOTYPE" src="https://github.com/user-attachments/assets/050b805a-74fb-40bb-847a-3f8b9a00a593" />

![LCDOnPrototype](https://github.com/user-attachments/assets/bebcd144-b9dc-43d1-9bed-5d473e55d2a2)


------------------------------------------
### Installation


------------------------------------------
### Contributors

Zinab Alsaggaf - [Zinab0](https://github.com/Zinab0)

Reema Almalki - [ReemmaMalki](https://github.com/ReemmaMalki)

Rawan Alghamdi - [RawanAlghamdii](https://github.com/RawanAlghamdii)

------------------------------------------

