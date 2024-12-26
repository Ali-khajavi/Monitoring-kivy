# Monitoring Software Configuration Tool

This project is designed for monitoring IoT or IIoT systems. The software is built using Python with the Kivy platform for the GUI. Below are the key features of the software:

## Features

- **Customer and Device Management:**  
  Create and manage a list of customers and their devices that need to be monitored by the software.
  
- **Unique Device Codes:**  
  Create a list of devices for each customer separately, with a unique code for each device.

- **Customer Search:**  
  Find customers by filtering their names.

- **Monitor Multiple Devices:**  
  Monitor specific customer sensors or devices in four separate windows.

- **Data History:**  
  The monitoring windows display changes in data over the last 15 minutes, 30 minutes, the last day, the last two days, or up to one month.

- **Full-Screen Chart Analysis:**  
  Click on a monitoring window to resize it to full-screen for clearer chart analysis.

- **InfluxDB Integration:**  
  Set up your InfluxDB server and use it with the software.

## Installation

### Step 1: Install Dependencies

In this tutorial, I am using VSCode:

- Clone the repository using the following command:
  ```bash
  git clone https://github.com/Ali-khajavi/Monitoring-kivy.git
* Select the project folder in VsCode
* Ensure that you already installed python 3.10 or latest version
* then create python vertual invirment using the command:  (Recommended)
* then install the requirements.txt file using the command:
  
