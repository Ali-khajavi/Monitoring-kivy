# Monitoring Kivy

**A Python/Kivy desktop dashboard for managing customers and monitoring IoT/IIoT sensor data stored in InfluxDB.**

Monitoring Kivy brings customer records, sensor registration, and historical sensor visualization into one desktop interface. Assign sensors to customers, search for a customer, and investigate time-series readings across **four chart panels**. Each panel can display a selected sensor over a configurable historical time range.

> **Project status:** Source-based desktop application. An automated installer or a verified PyInstaller build specification is not included in the repository. A running InfluxDB instance containing appropriately tagged sensor readings is required for live charts.

## Features

- **Customer management:** Register customers with name, email, phone, city, address, and notes; browse, search by name, view details, and delete records.
- **Sensor management:** Associate multiple sensors with a customer; add a sensor code, type, and description, and edit or remove existing sensors.
- **Supported sensor categories in the interface:** Voltmeter, flowmeter, temperature, and ammeter (called `ampermeter` in the code).
- **Four monitoring panels:** Choose sensors from the selected customer's list and render historical data as line charts.
- **Historical ranges:** 30 minutes, 1 hour, 3 hours, 6 hours, 12 hours, 1 day, 2 days, 7 days, or 30 days.
- **Expanded chart view:** Click a rendered chart to view a larger version in a popup.
- **InfluxDB settings screen:** Save a server URL, API token, organization, and bucket; restart the application after changing settings.
- **Local Excel-backed registry:** Customer and sensor metadata is maintained in an `.xlsx` workbook, independently of the time-series measurements stored in InfluxDB.

## Technology stack

| Component | Role |
| --- | --- |
| Python | Application logic |
| Kivy and KV language | Desktop interface and navigation |
| InfluxDB Python client | Queries historical sensor readings |
| Matplotlib + Kivy Garden Matplotlib | Interactive application chart rendering |
| pandas | Converts query results into tabular time/value data |
| openpyxl | Reads and updates the customer/sensor Excel workbook |

Dependencies are listed in [`requirements.txt`](requirements.txt).

## How it works

The application has four screens:

1. **Main menu** — Navigate to customer setup, monitoring, or server settings.
2. **Customer setup** — Register and search customers, inspect details, and maintain their sensor codes/types/descriptions.
3. **Monitoring** — Select a customer and then a sensor and historical time range for one of four chart channels. The app queries InfluxDB and draws a time-series chart; click a chart for an enlarged popup.
4. **Settings** — Change the InfluxDB connection information or reset the settings to the application's bundled defaults.

### Data flow

```text
Customer and sensor metadata                 Sensor measurements
      customers_data.xlsx                          InfluxDB
              |                                       |
         ExcelHandler                       InfluxDBClient / Flux
              |                                       |
        Kivy customer UI                      pandas DataFrame
              |                                       |
              +---------- MonitoringScreen -----------+
                                  |
                        Matplotlib / Kivy
                                  |
                         Four chart panels
```

**Important distinction:** The application registers sensor identifiers locally, but it **does not collect readings directly from hardware** or upload sensor readings into InfluxDB. Another device, agent, or service must write the measurements to InfluxDB.

## Getting started

### Prerequisites

- Python **3.10 or newer** is a reasonable starting point; exact version compatibility has not been formally tested here.
- A desktop environment capable of running Kivy.
- An accessible **InfluxDB 2.x-compatible** server, organization, bucket, and API token with query permission.
- A data producer that writes sensor measurements into that InfluxDB bucket.

### 1. Clone the repository

```bash
git clone https://github.com/Ali-khajavi/Monitoring-kivy.git
cd Monitoring-kivy
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Kivy may require platform-specific system dependencies. See the [official Kivy installation guide](https://kivy.org/doc/stable/gettingstarted/installation.html) if installation fails.

### 4. Configure InfluxDB

Edit `config.ini` in the project root using **your own** credentials:

```ini
[Settings]
influxdb_token = YOUR_INFLUXDB_API_TOKEN
organization = YOUR_ORGANIZATION
bucket = YOUR_BUCKET
server_address = http://localhost:8086
```

Alternatively, update these fields in the **Settings** screen and restart the app. The settings are loaded when the monitoring module is imported, so changes are not reliably applied to an already-running session.

**Security:** Never commit real API tokens to version control. The repository's current `config.ini` and `secrets_server.py` contain an apparent preconfigured credential; **revoke/rotate that token before using this project**, remove credentials from the source and Git history, and use a local, untracked configuration file or environment variables in future development. The existing settings UI also displays token values in diagnostic output/popups; avoid using sensitive production credentials until this behavior is fixed.

### 5. Launch the application

From the repository root:

```bash
python main.py
```

Run from the project directory because the code resolves KV files, assets, `config.ini`, and `customers_data.xlsx` relative to the working directory in development.

## InfluxDB data requirements

The current query implementation in `monitoring_screen.py` uses Flux and filters on a tag/column named `DEVICE`:

```flux
from(bucket: "YOUR_BUCKET")
  |> range(start: -1h)
  |> filter(fn: (r) => r.DEVICE == "YOUR_SENSOR_CODE")
```

For charts to work:

- Your InfluxDB bucket must contain time-series points with a `DEVICE` tag matching a sensor code registered in the customer UI.
- The points need timestamps and numeric values. The application plots the returned record times and values.
- The configured token, organization, bucket, and URL must be valid and reachable.
- If your bucket contains multiple fields or measurements with the same `DEVICE` tag, the query may return mixed series, because the code currently does not filter on `_measurement` or `_field`. Customize the query if you need a specific signal.

**Example point (illustrative line protocol):**

```text
sensor_reading,DEVICE=TEMP-001 value=23.7
```

The measurement name and numeric field shown here are examples; the current chart query does not require these specific names.

## Using the application

### Manage customers and sensors

1. Open **Customer Setup** from the main menu.
2. Fill in the new-customer form and register the customer.
3. Select a customer in the list (use the search field to filter by name).
4. Choose a sensor category, enter its **sensor code** and optional description, and save it.
5. Click a listed sensor to edit its code/description or delete it.

Sensor codes should correspond exactly to the `DEVICE` tag values written to InfluxDB. The application stores the sensor records but does **not currently enforce global uniqueness** of codes.

### Explore sensor readings

1. Open **Monitoring** and select a customer.
2. Choose one of that customer's sensor codes in a chart channel.
3. Select a historical range for that channel.
4. The application retrieves readings from InfluxDB and plots them as a line chart.
5. Click an existing chart to open its larger popup view. Repeat for up to four channels.

There is no verified continuous live-refresh scheduler in the current source; charts are generated in response to UI selections and queries.

## Project structure

```text
Monitoring-kivy/
├── main.py                   # App entry point and screen manager
├── customer_setup_screen.py  # Customer and sensor management UI logic
├── monitoring_screen.py      # InfluxDB queries and four-panel plotting
├── settings_screen.py        # Server configuration UI logic
├── first_menu_screen.py      # Main menu logic
├── excel_handler.py          # Excel customer/sensor data persistence
├── secrets_server.py         # Configuration loading/saving and defaults
├── config.ini                # Local InfluxDB connection settings (sensitive)
├── customers_data.xlsx       # Excel-based customer and sensor registry
├── requirements.txt          # Python dependencies
├── kv/                       # Kivy UI layouts (one per screen)
│   ├── first_menu.kv
│   ├── customer_setup.kv
│   ├── monitoring.kv
│   └── settings.kv
├── assets/                   # Images, labels, icons, and other UI assets
├── LICENSE                   # Apache License 2.0
└── README.md
```

### Local data format

`excel_handler.py` uses a `Customers` worksheet with the following columns:

| Columns | Data |
| --- | --- |
| A–G | First name, last name, email, phone, city, description, address |
| H | Sensor codes |
| I | Sensor types |
| J | Sensor descriptions |

Multiple sensors are stored as **semicolon-separated values** in columns H–J. These columns must stay aligned. The implementation identifies customers by a `last_name;first_name` string, so customers who share the same name may be ambiguous.

## Current limitations and troubleshooting

- **Charts show no data:** Check InfluxDB connectivity, bucket/organization permissions, the selected time range, and an exact match between the registered sensor code and the `DEVICE` tag.
- **Connection settings appear unchanged:** Restart the application after saving them.
- **Excel file cannot be loaded or updated:** Keep `customers_data.xlsx` in the project root and make sure it is writable. If modifying the workbook manually, preserve the `Customers` sheet and expected columns.
- **Application fails to start:** Confirm you launched it from the project root, installed `requirements.txt`, and that the expected assets and KV files are present.
- **No automatic installer:** The source contains some PyInstaller resource-path handling, but no ready-to-use `.spec` file or tested build recipe. Packaging also requires ensuring that assets, KV files, and writable user data are handled correctly.
- **Settings and data are stored in the project directory:** The current design is not ideal for read-only or one-file packaged installations; move writable config/workbook files to a user data directory before distributing binaries.
- **Prototype caveats:** Some chart-selection state is shared between channels, data validation is limited, and errors during InfluxDB queries may prevent charts from updating. This project is best treated as a starting point for further development rather than a production-ready monitoring platform.

## Future improvements

- Remove checked-in credentials and support environment-based configuration.
- Add input validation and stable customer/sensor identifiers.
- Add explicit InfluxDB measurement/field selection and stronger query error handling.
- Improve per-channel state independence and add optional scheduled refresh.
- Store user-editable data outside the application bundle.
- Add automated tests and a tested desktop packaging workflow.

## License

Licensed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE).

## Author

Created by [Ali Khajavi](https://github.com/Ali-khajavi). Contributions and issue reports are welcome through this repository.
