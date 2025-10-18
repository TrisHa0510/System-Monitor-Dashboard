# 🖥️ System Monitoring Dashboard (Flask + psutil)

A **complete web-based system monitoring dashboard** built using **Flask** and **psutil**.  
It helps visualize CPU, Memory, Disk, and System statistics of your **Virtual Machine (VM)** or **local computer** through a clean, interactive interface.  

This project is part of a **VM Provisioning and Monitoring** task — focusing on learning how to collect, display, and understand real-time system metrics.

---

## 📖 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [Project Structure](#-project-structure)
4. [Technologies Used](#-technologies-used)
5. [Setup Instructions](#️-setup-instructions)
6. [How It Works](#-how-it-works)
7. [Example Routes](#-example-routes)
8. [Screenshots](#-screenshots)
9. [Future Enhancements](#-future-enhancements)
10. [Author](#-author)
11. [License](#-license)

---

## 🧩 Overview

The **System Monitoring Dashboard** acts as a mini control panel that provides insights into your system’s resource usage in real time.  
Using **psutil**, it extracts system data such as:
- CPU usage and core info
- Memory consumption
- Disk space usage
- Network and battery information
- Uptime and system details  

The data is served dynamically through a **Flask backend**, with HTML templates displaying metrics neatly formatted using cards, progress bars, and **Chart.js** graphs.

---

## 🚀 Features

### 🧠 System Information
- OS, processor name, architecture
- Uptime (time since boot)
- IP address and hostname
- Battery percentage and power status

### ⚙️ CPU Monitoring
- Live CPU usage in %
- Logical and physical cores
- CPU frequency (min, max, current)
- Visualized with **doughnut or gauge charts**

### 💾 Memory Insights
- Total, used, and free RAM
- Swap memory details
- Color-coded bars for better visualization

### 💽 Disk Usage
- Monitors storage partitions
- Shows used/free space
- Percentage-based progress visualization

### ⚡ Interactive Web Interface
- Simple and responsive HTML/CSS design
- Animated progress bars
- Alerts for high usage (>80%)
- Navigation between pages for CPU, Memory, Disk

---
